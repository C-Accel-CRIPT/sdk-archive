import json
from logging import getLogger

import requests

from cript.storage_clients.exceptions import FileDownloadError, FileUploadError

logger = getLogger(__name__)


class AmazonS3Client:
    def __init__(self, api):
        self.api = api
        self.session = api.session
        self.url = api.url

    def single_file_upload(self, file_uid, node):
        """
        Performs a single file upload to AWS S3.
        :param file_uid: UID of the `File` node object.
        :param node: The `File` node object.
        """
        # Generate signed URL for uploading
        payload = {
            "action": "upload",
            "file_uid": file_uid,
            "file_checksum": node.checksum,
        }
        response = self.session.post(url=f"{self.url}/s3-signed-url/", data=json.dumps(payload))

        # Upload file
        if response.status_code == 200:
            logger.info(f"Upload of file {file_uid} to AWS S3 in progress.")
            url = json.loads(response.content)
            files = {"file": open(node.source, "rb")}
            response = requests.put(url=url, files=files)
            if response.status_code != 200:
                raise FileUploadError
        else:
            raise FileUploadError

    def multipart_file_upload(self, file_uid, node):
        """
        Performs a multipart file upload to AWS S3.
        :param file_uid: UID of the File node.
        :param node: The `File` node object.
        """
        chunk_size = 500 * 1024**2

        # Create multipart upload and get upload ID
        payload = {
            "action": "create",
            "file_uid": file_uid,
            "file_checksum": node.checksum,
        }
        response = self.session.post(
            url=f"{self.url}/s3-multipart-upload/",
            data=json.dumps(payload),
        )
        upload_id = json.loads(response.content)["UploadId"]

        # Upload file in chunks
        logger.info(f"Upload of file {file_uid} to AWS S3 in progress.")
        parts = []
        with open(node.source, "rb") as local_file:
            while True:
                file_data = local_file.read(chunk_size)
                if not file_data:
                    break

                # Generate signed URL for uploading
                data = {
                    "action": "upload",
                    "file_uid": file_uid,
                    "file_checksum": node.checksum,
                    "upload_id": upload_id,
                    "part_number": len(parts) + 1,
                }
                response = self.session.post(
                    url=f"{self.url}/s3-signed-url/", data=json.dumps(data)
                )

                # Upload file chunk
                if response.status_code == 200:
                    signed_url = json.loads(response.content)
                    response = requests.put(url=signed_url, data=file_data)
                    if response.status_code == 200:
                        etag = response.headers["ETag"]
                        parts.append({"ETag": etag, "PartNumber": len(parts) + 1})
                    else:
                        raise FileUploadError
                else:
                    raise FileUploadError

        # Complete multipart upload
        data = {
            "action": "complete",
            "file_uid": file_uid,
            "upload_id": upload_id,
            "parts": parts,
        }
        response = self.session.post(
            url=f"{self.url}/s3-multipart-upload/",
            data=json.dumps(data),
        )
        if response.status_code != 200:
            raise FileUploadError
