import enum
import json

import requests


class StatusCode(enum.Enum):
    ok = 200
    created = 201
    accepted = 202
    no_content = 204
    bad_request = 400
    unathorized = 401
    forbidden = 403
    not_found = 404
    method_not_allowed = 405
    conflict = 409
    unsupported_media_type = 415
    too_many_requests = 429
    internal_server_error = 500


class ZenodoHandler:
    BASE_URL = "https://sandbox.zenodo.org/api/deposit/depositions"

    def __init__(self, access_token, proxies=None):
        self.token = access_token
        self.proxies = proxies

    def deposition_list(self):
        """
        List all depositions for the currently authenticated user.

        - Url: https://sandbox.zenodo.org/api/deposit/depositions
        - Method: GET
        """
        url = "{}?access_token={}".format(self.BASE_URL, self.token)

        return requests.get(url, proxies=self.proxies)

    def deposition_create(self):
        """
        Create a new deposition resource.

        - Url: https://sandbox.zenodo.org/api/deposit/depositions
        - Method: POST

        : param deposition_id: Deposition identifier
        """
        url = "{}?access_token={}".format(self.BASE_URL, self.token)
        headers = {"Content-Type": "application/json"}

        return requests.post(url, data="{}", headers=headers,
                             proxies=self.proxies)

    def deposition_retrieve(self, deposition_id):
        """
        Retrieve a single deposition resource.

        - Url: https://sandbox.zenodo.org/api/deposit/depositions/:id
        - Method: GET

        :param deposition_id: Deposition identifier
        """
        url = "{}/{}?access_token={}".format(self.BASE_URL, deposition_id,
                                             self.token)
        return requests.get(url, proxies=self.proxies)

    def deposition_update(self, deposition_id, data):
        """
        Update an existing deposition resource.

        - URL: https://sandbox.zenodo.org/api/deposit/depositions/:id
        - Method: PUT

        :param deposition_id: Deposition identifier
        :param data: Data to upload
        """
        url = "{}/{}?access_token={}".format(self.BASE_URL, deposition_id,
                                             self.token)
        headers = {"Content-Type": "application/json"}
        return requests.put(url, data=data, headers=headers,
                            proxies=self.proxies)

    def deposition_delete(self, deposition_id):
        """
        Delete an existing deposition resource.

        - URL: https://sandbox.zenodo.org/api/deposit/depositions/:id
        - Method: DELETE

        :param deposition_id: Deposition identifier
        """
        url = "{}/{}?access_token={}".format(self.BASE_URL, deposition_id,
                                             self.token)
        return requests.delete(url, proxies=self.proxies)

    def deposition_files_list(self, deposition_id):
        """
        List all deposition files for a given deposition.

        - URL: https://sandbox.zenodo.org/api/deposit/depositions/:id/files
        - Method: GET

        :param deposition_id: Deposition identifier
        """
        url = "{}/{}/files?access_token={}".format(self.BASE_URL, deposition_id,
                                                   self.token)
        return requests.get(url, proxies=self.proxies)

    def deposition_files_create(self, deposition_id, target_name, file_path):
        """
        Upload a new file.

        - URL: https://sandbox.zenodo.org/api/deposit/depositions/:id/files
        - Methods: POST

        :param deposition_id: Deposition identifier
        :param target_name: Name of the file once uploaded
        :param file_path: Path of local file to be uploaded
        """
        url = "{}/{}/files?access_token={}".format(self.BASE_URL, deposition_id,
                                                   self.token)
        data = {'filename': target_name}
        files = {'file': open(file_path, 'rb')}
        return requests.post(url, data=data, files=files, proxies=self.proxies)

    def deposition_files_sort(self, deposition_id, file_ids):
        """
        Sort the files for a deposition. By default, the first file is show

        - URL: https://sandbox.zenodo.org/api/deposit/depositions/:id/files
        - Method: PUT

        :param deposition_id: Deposition identifier
        :param file_ids: List of ids of the files in the deposition
        """
        url = "{}/{}/files?access_token={}".format(self.BASE_URL, deposition_id,
                                                   self.token)
        headers = {"Content-Type": "application/json"}
        data = json.dumps({'id': file_id for file_id in file_ids})
        return requests.put(url, data=data, headers=headers,
                            proxies=self.proxies)

    def depositions_files_retrieve(self, deposition_id, file_id):
        """
        Retrieve a single deposition file.

        - URL:
        https://sandbox.zenodo.org/api/deposit/depositions/:id/files/:file_id
        - Method: GET

        :param deposition_id: Deposition identifier
        :param file_id: Deposition file identifier
        """
        url = "{}/{}/files/{}?access_token={}".format(self.BASE_URL,
                                                      deposition_id, file_id,
                                                      self.token)
        return requests.get(url, proxies=self.proxies)

    def depositions_files_update(self, deposition_id, file_id, target_name):
        """
        Update a deposition file resource. Currently the only use is renaming an
        already uploaded file. If you want to to replace the actual file, please
        delete the file and uploada new file.

        - URL:
        https://sandbox.zenodo.org/api/deposit/depositions/:id/files/:file_id
        - Method: GET

        :param deposition_id: Deposition identifier
        :param file_id: Deposition file identifier
        :param target_name: Name of the file once uploaded
        """
        url = "{}/{}/files/{}?access_token={}".format(self.BASE_URL,
                                                      deposition_id, file_id,
                                                      self.token)
        headers = {"Content-Type": "application/json"}
        data = json.dumps({"filename", target_name})

        return requests.put(url, data=data, headers=headers,
                            proxies=self.proxies)

    def depositions_files_delete(self, deposition_id, file_id):
        """
        Delete an existing deposition file resource. Note, only deposition files
        for unpublished depositions may be deleted.

        - URL:
        https://sandbox.zenodo.org/api/deposit/depositions/:id/files/:file_id
        - Method: DELETE

        :param deposition_id: Deposition identifier
        :param file_id: Deposition file id
        """
        url = "{}/{}/files/{}?access_token={}".format(self.BASE_URL,
                                                      deposition_id, file_id,
                                                      self.token)
        return requests.delete(url, proxies=self.proxies)

    def deposition_actions_publish(self, deposition_id):
        """
        Publish a deposition. Note, once a deposition is published, you can
        no longer delete it.

        - URL:
        https://sandbox.zenodo.org/api/deposit/depositions/:id/actions/publish
        - Method: POST

        :param deposition_id: Deposition identifier.
        """
        url = "{}/{}/actions/publish?access_token={}".format(self.BASE_URL,
                                                             deposition_id,
                                                             self.token)
        return requests.post(url, proxies=self.proxies)
