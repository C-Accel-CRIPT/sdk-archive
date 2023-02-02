def auto_assign_group(group, parent):
    """
    Decide whether to inherit the group from a node's parent.
    e.g., Experiment could inherit the group of it's parent Collection.

    :param group: Current value of the node's group field.
    :param parent: The parent node of the relevant node.
    :return: The `Group` object that will be assigned to the node.
    :rtype: cript.data_model.nodes.Group
    """
    if parent and not group:
        return parent.group
    return group


def set_node_attributes(node, obj_json):
    """
    Set node attributes using data from an API response.

    :param obj_json: The JSON representation of the node object.
    """
    for json_key, json_value in obj_json.items():
        setattr(node, json_key, json_value)


def create_node(node_class, obj_json):
    """
    Create a node with JSON returned from the API.

    :param node_class: The class of the node to be created.
    :param obj_json: The JSON representation of the node object.
    :return: The created node.
    :rtype: cript.nodes.Base
    """
    # Pop common attributes
    url = obj_json.pop("url")
    uid = obj_json.pop("uid")
    created_at = obj_json.pop("created_at")
    updated_at = obj_json.pop("updated_at")

    # Pop these keys out from api returned JSON for compatibility with Python SDK
    if node_class.node_name == "File":
        obj_json.pop("data_dictionary", None)
        obj_json.pop("data", None)

    # pop unused key for Python SDK, but used in web SDK
    obj_json.pop("can_edit", None)

    # Create node
    node = node_class(**obj_json)

    # Replace common attributes
    node.url = url
    node.uid = uid
    node.created_at = created_at
    node.updated_at = updated_at

    return node


def get_data_model_class(key: str):
    """
    Get the correct data model class associated with a given key.

    :param key: The key string indicating the class.
    :return: The correct class.
    :rtype: cript.nodes.Base
    """
    from cript import DATA_MODEL_CLASSES

    for cls in DATA_MODEL_CLASSES:
        # Use node name
        if cls.node_name.lower() == key.replace("_", "").lower():
            return cls
        # Use alternative names
        if hasattr(cls, "alt_names"):
            for alt_name in cls.alt_names:
                if alt_name == key:
                    return cls
    return None
