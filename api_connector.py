"""
CRIPT REST API Connector
"""
import os
import requests
import json
from typing import Union
from getpass import getpass

from beartype import beartype
from beartype.typing import Type
from pprint import pprint

from . import node_classes
from .nodes import Base
from .errors import (
    APIAuthError,
    APIRefreshError,
    APISaveError,
    APIDeleteError,
    APISearchError,
    APIGetError,
)


class API:
    @beartype
    def __init__(self, url: str, token: str = None):
        """
        Establishes a session with the CRIPT API.

        :param url: The API endpoint URL.
        """
        self.url = url.rstrip("/")
        self.session = requests.Session()
        if token is None:
            token = getpass("API Token: ")

        self.session.headers = {
            "Authorization": token,
            "Content-Type": "application/json",
        }

        # Test API authentication
        response = self.session.get(self.url)
        if response.status_code == 401:
            raise APIAuthError(response.json()["detail"])

        # Print success message
        print(f"\nConnection to the API was successful!\n")

    def __repr__(self):
        return f"Connected to {self.url}"

    def __str__(self):
        return f"Connected to {self.url}"

    @beartype
    def refresh(self, node: Base):
        """
        Overwrite a node's attributes with the latest values from the DB.

        :param node: The node to refresh.
        """
        if hasattr(node, "url"):
            if node.url:
                response = self.session.get(node.url)
                self._set_node_attributes(node, response.json())
                self._generate_nodes(node)
            else:
                raise APIRefreshError(
                    "Before you can refresh a node, you must either save it or define it's URL."
                )
        else:
            raise APIRefreshError(
                f"{node.node_name} is a secondary node, thus cannot be refreshed."
            )

    @beartype
    def save(self, node: Base):
        """
        Create or update a node in the DB.

        :param node: The node to be saved.
        """
        if node.node_type == "primary":
            if node.url:
                # Update an existing object via PUT
                response = self.session.put(url=node.url, data=node._to_json())
            else:
                # Create a new object via POST
                response = self.session.post(
                    url=f"{self.url}/{node.slug}/", data=node._to_json()
                )
            if response.status_code in (200, 201):
                if node.slug == "file":
                    self._upload_file(response.json()["id"], node.source)
                self._set_node_attributes(node, response.json())
                self._generate_nodes(node)

                # Update signed URL for File nodes
                if node.slug == "file":
                    self.refresh(node)

                print(f"{node.node_name} node has been saved to the database.")
            else:
                pprint(response.json())
        else:
            raise APISaveError(
                f"The save() method cannot be called on secondary nodes such as {node.node_name}"
            )

    def _set_node_attributes(self, node, response_json):
        """
        Set node attributes using data from an API response.

        :param node: The node you want to set attributes for.
        :param response: The response from an API call.
        """
        for json_key, json_value in response_json.items():
            setattr(node, json_key, json_value)

    def _upload_file(self, file_id, file_path):
        """ "
        Generate a signed URL then upload the file to S3.

        :param node: ID of the File node.
        """
        if file_path and os.path.exists(file_path):
            # Generate signed URL for uploading
            data = {"action": "upload", "file_id": file_id}
            response = self.session.post(
                url=f"{self.url}/signed-url/", data=json.dumps(data)
            )

            # Upload file
            if response.status_code == 200:
                print("\nUpload in progress ...\n")
                url = json.loads(response.content)
                files = {"file": open(file_path, "rb")}
                response = requests.put(url=url, files=files)

                if response.status_code != 200:
                    raise APISaveError(f"Unable to upload the file: {response.content}")
            else:
                pprint(response.content)

    def delete(self, node: Base):
        """
        Delete a node locally and in the DB.

        :param node: The node to be deleted.
        :return: Response message.
        """
        if node.node_type == "primary":
            if node.url:
                response = self.session.delete(url=node.url)
                if response.status_code == 204:
                    print(f"{node.node_name} node has been deleted from the database.")
                    # Reset fields to indicate the object has been deleted from DB
                    node.url = None
                    node.created_at = None
                    node.updated_at = None
                else:
                    pprint(response.json())
            else:
                raise APIDeleteError(
                    f"This {node.node_name} node doest not exist in the database."
                )
        else:
            raise APIDeleteError(
                f"The delete() method cannot be called on secondary nodes such as {node.node_name}"
            )

    @beartype
    def search(self, node_class: Type[Base], query: dict = None):
        """
        Send a query to the API and print the results.

        :param node: The node type you want to search.
        :param query: A dictionary defining the query parameters.
        :return: The JSON response of the query.
        """
        if node_class.node_type == "secondary":
            raise APISearchError(
                f"{node_class.node_name} is a secondary node, thus cannot be searched."
            )
        if isinstance(query, dict):
            query_slug = self._generate_query_slug(query)
            response = self.session.get(f"{self.url}/{node_class.slug}/?{query_slug}")
        elif query is None:
            response = self.session.get(f"{self.url}/{node_class.slug}/")
        else:
            raise APISearchError(f"'{query}' is not a valid query.")

        return response.json()

    def _generate_query_slug(self, query):
        """Generate the query URL slug."""
        slug = ""
        for key in query:
            slug += f"{key}={query[key]}&"
        return slug

    @beartype
    def get(self, obj: Union[str, Type[Base]], query: dict = None, counter: int = 0):
        """
        Get the JSON for a node and use it to generated a local node object.

        :param url: The API URL of the node.
        :param counter: Cross-method recursion counter.
        :return: The generated node object.
        """
        # Fetch node from a URL, if defined
        if isinstance(obj, str):
            url = obj
            if self.url not in url:
                raise APIGetError("Please enter a valid node URL.")

            # Define node class from URL slug
            node_slug = url.rstrip("/").rsplit("/")[-2]
            node_class = self._define_node_class(node_slug)

            response = self.session.get(url)
            if response.status_code == 200:
                response_json = response.json()
            else:
                raise APIGetError(
                    f"The specified {node_class.node_name} node was not found."
                )

        # Fetch node from search query, if defined
        elif issubclass(obj, Base) and query:
            node_class = obj
            search_json = self.search(node_class=node_class, query=query)
            count = search_json["count"]
            if count < 1:
                raise APIGetError("Your query did not match any existing nodes.")
            elif count > 1:
                raise APIGetError("Your query mathced more than one node.")
            else:
                response_json = search_json["results"][0]
        else:
            raise APIGetError(
                f"Please enter a node URL or a node class with a search query."
            )

        # Return the local node object if it already exists
        local_node = self._get_local_primary_node(response_json["url"])
        if local_node:
            return local_node
        else:
            # Pop then add after node is created
            created_at = response_json.pop("created_at", None)
            updated_at = response_json.pop("updated_at", None)

            node = node_class(**response_json)
            node.created_at = created_at
            node.updated_at = updated_at

            if counter > 0:
                counter += 1
            self._generate_nodes(node, counter=counter)

            return node

    def _generate_nodes(self, node: Base, counter: int = 0):
        """
        Generate nested node objects within a given node.

        :param node: The parent node.
        :param counter: Cross method recursion counter.
        """
        # Limit recursion to one level
        if counter > 1:
            return

        node_dict = node.__dict__
        for key, value in node_dict.items():
            # Skip the url field
            if key == "url":
                continue
            # Generate primary nodes
            if isinstance(value, str) and self.url in value:
                # Check if node already exists in memory
                local_node = self._get_local_primary_node(value)
                if local_node:
                    node_dict[key] = local_node
                else:
                    try:
                        node_dict[key] = self.get(value, counter=counter + 1)
                    except APIGetError:
                        # Leave the URL if node is not viewable
                        pass
            # Generate secondary nodes
            elif isinstance(value, dict):
                node_class = self._define_node_class(key)
                secondary_node = node_class(**value[i])
                node_dict[key] = secondary_node
                self._generate_nodes(secondary_node, counter=counter + 1)
            # Handle lists
            elif isinstance(value, list):
                for i in range(len(value)):
                    # Generate primary nodes
                    if isinstance(value[i], str) and self.url in value[i]:
                        # Check if node already exists in memory
                        local_node = self._get_local_primary_node(value[i])
                        if local_node:
                            value[i] = local_node
                        else:
                            try:
                                value[i] = self.get(value[i], counter=counter + 1)
                            except APIGetError:
                                # Leave the URL if node is not viewable
                                pass
                    # Generate secondary nodes
                    elif isinstance(value[i], dict):
                        node_class = self._define_node_class(key)
                        secondary_node = node_class(**value[i])
                        value[i] = secondary_node
                        self._generate_nodes(secondary_node, counter=counter + 1)

    def _define_node_class(self, key: str):
        """
        Find the correct class associated with a given key.

        :param key: The key used to find the correct class.
        :return: The correct node class.
        """
        for node_cls in node_classes:
            # Use node slug
            if hasattr(node_cls, "slug") and node_cls.slug == key:
                return node_cls
            # Use node list name (e.g., properties)
            if hasattr(node_cls, "list_name") and node_cls.list_name == key:
                return node_cls
        return None

    def _get_local_primary_node(self, url: str):
        """
        Use a URL to get a primary node object stored in memory.

        :param url: The URL to match against existing node objects.
        :return: The matching object or None.
        """
        for instance in Base.__refs__:
            if hasattr(instance, "url") and url == instance.url:
                return instance
        return None
