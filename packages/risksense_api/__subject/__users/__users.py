""" *******************************************************************************************************************
|
|  Name        :  __users.py
|  Module      :  risksense_api
|  Description :  A class to be used for getting information about RiskSense platform users.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

import json
from ..__exports import ExportFileType
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *


class Users(Subject):

    """ Users Class """

    def __init__(self, profile):

        """
        Initialization of Users object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """

        self.subject_name = "user"
        Subject.__init__(self, profile, self.subject_name)
        self.api_base_url = self.profile.platform_url + "/api/v1/"

    def get_my_profile(self):

        """
        Get the profile for the user that owns the API key being used.

        :return:    A dictionary containing the user's profile.
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        url = self.api_base_url + "user/profile"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        user_profile = jsonified_response

        return user_profile

    def disallow_tokens(self, user_id):

        """
        Disallow use of tokens for a user.

        :param user_id:     The ID of the user to be disallowed from token use.
        :type  user_id:     int

        :return:    True/False indicating success or failure of submission of the operation.
        :rtype:     bool

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        url = self.api_base_url + "user/" + str(user_id) + "/tokenAllowed"

        body = {
            "allowed": False
        }

        try:
            self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            success = True
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return success

    def allow_tokens(self, user_id):

        """
        Allow use of tokens for a user.

        :param user_id:     The ID of the user to be allowed token use.
        :type  user_id:     int

        :return:    True/False indicating success or failure of submission of the operation.
        :rtype:     bool

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        url = self.api_base_url + "user/" + str(user_id) + "/tokenAllowed"

        body = {
            "allowed": True
        }

        try:
            self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            success = True
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return success

    def export(self, search_filters, file_name, file_type=ExportFileType.CSV, comment="", client_id=None):

        """
        Initiates an export job on the platform for user(s) based on the
        provided filter(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param file_name:       The name to be used for the exported file.
        :type  file_name:       str

        :param file_type:       File type to export.  ExportFileType.CSV, ExportFileType.XML, or ExportFileType.XLSX
        :type  file_type:       str

        :param comment:         Any comments to include with the export.
        :type  comment:         str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID returned
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        func_args = locals()
        func_args.pop('self')

        if client_id is None:
            func_args['client_id'] = self._use_default_client_id()[1]

        try:
            export_id = self._export(self.subject_name, **func_args)
        except (RequestFailed, StatusCodeError, MaxRetryError, ValueError):
            raise

        return export_id

    def get_single_search_page(self, search_filters, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns users based on the provided filter(s) and other parameters.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param page_num:        Page number of results to be returned.
        :type  page_num:        int

        :param page_size:       Number of results to be returned per page.
        :type  page_size:       int

        :param sort_field:      Name of field to sort results on.
        :type  sort_field:      SortField attribute

        :param sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Paginated JSON response from the platform.

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises PageSizeError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "client/{}/user/search".format(str(client_id))

        body = {
            "filters": search_filters,
            "projection": Projection.BASIC,
            "sort": [
                {
                    "field": sort_field,
                    "direction": sort_dir
                }
            ],
            "page": page_num,
            "size": page_size
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def search(self, search_filters, page_size=150, sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns users based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      Name of field to sort results on.
        :type  sort_field:      SortField attribute

        :param sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A list containing all hosts returned by the search using the filter provided.
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises PageSizeError:
        """

        func_args = locals()
        func_args.pop('self')
        all_results = []

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        try:
            page_info = self._get_page_info(self.subject_name, search_filters, page_size=page_size, client_id=client_id)
            num_pages = page_info[1]
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
            raise

        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
            raise

        return all_results

    def get_user_info(self, user_id=None, client_id=None):

        """
        Get info for a specific user.  If user_id is not specified, the info for the requesting user is returned.

        :param user_id:     User ID
        :type  user_id:     int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    User information.
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        params = {}

        url = self.api_base_url + "client/{}/user".format(str(client_id))

        if user_id is not None:
            params.update({"userId": user_id})

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def create(self, username, first_name, last_name, email_address, phone_num,
               read_only, group_ids, client_id=None, **kwargs):

        """
        Create a new user.

        :param username:        Username
        :type  username:        str

        :param first_name:      First Name
        :type  first_name:      str

        :param last_name:       Last Name
        :type  last_name:       str

        :param email_address:   E-mail address
        :type  email_address:   str

        :param phone_num:       Phone Number
        :type  phone_num:       str

        :param read_only:       Read Only
        :type  read_only:       bool

        :param group_ids:       Group IDs to assign user to
        :type  group_ids:       list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword use_saml:      Is a SAML user?             (bool)
        :keyword saml_attr_1:   SAML Attribute 1            (str)
        :keyword saml_attr_2:   SAML Attribute 2            (str)
        :keyword exp_date:      Expiration Date YYYY-MM-DD  (str)

        :return:    job ID
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "client/{}/user".format(str(client_id))

        use_saml = kwargs.get("use_saml", None)
        saml_attr_1 = kwargs.get("saml_attr_l", None)
        saml_attr_2 = kwargs.get("saml_attr_2", None)
        exp_date = kwargs.get("exp_date", None)

        body = {
            "username": username,
            "firstName": first_name,
            "lastName": last_name,
            "email": email_address,
            "phone": phone_num,
            "groupIds": group_ids,
            "readOnly": read_only,
            "useSamlAuthentication": use_saml,
            "samlAttribute1": saml_attr_1,
            "samlAttribute2": saml_attr_2,
            "expirationDate": exp_date
        }

        body = self._strip_nones_from_dict(body)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def update_user_role(self, search_filter, role, client_id=None):

        """
        Update user role.

        :param search_filter:   Filter to identify users to be updated
        :type  search_filter:   list

        :param role:            User role
        :type  role:            str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Job ID
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "client/{}/user/userRole/update".format(str(client_id))

        body = {
            "filterRequest": {
                "filters": search_filter
            },
            "role": role
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def update_user(self, user_uuid, client_id=None, **kwargs):

        """
        Update a user.

        :param user_uuid:   User UUID
        :type  user_uuid:   str

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword username:      Username                    (str)
        :keyword first_name:    First Name                  (str)
        :keyword last_name:     Last Name                   (str)
        :keyword email:         Email                       (str)
        :keyword phone:         Phone Num.                  (str)
        :keyword group_ids:     Group IDs                   (list)
        :keyword read_only:     Read-Only                   (bool)
        :keyword use_saml:      Use SAML?                   (bool)
        :keyword saml_attr_1:   SAML Attribute 1            (str)
        :keyword saml_attr_2:   SAML Attribute 2            (str)
        :keyword exp_date:      Expiration Date YYYY-MM-DD  (str)

        :return:    Job ID
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "client/{}/user/{}".format(str(client_id), user_uuid)

        username = kwargs.get("username", None)
        first_name = kwargs.get("firstName", None)
        last_name = kwargs.get("lastName", None)
        email_address = kwargs.get("email", None)
        phone_num = kwargs.get("phone", None)
        group_ids = kwargs.get("group_ids", None)
        read_only = kwargs.get("read_only", None)
        use_saml = kwargs.get("use_saml", None)
        saml_attr_1 = kwargs.get("saml_attr_l", None)
        saml_attr_2 = kwargs.get("saml_attr_2", None)
        exp_date = kwargs.get("exp_date", None)

        body = {
            "username": username,
            "firstName": first_name,
            "lastName": last_name,
            "email": email_address,
            "phone": phone_num,
            "groupIds": group_ids,
            "readOnly": read_only,
            "useSamlAuthentication": use_saml,
            "samlAttribute1": saml_attr_1,
            "samlAttribute2": saml_attr_2,
            "expirationDate": exp_date
        }

        body = self._strip_nones_from_dict(body)

        if body == {}:
            raise ValueError("No new valid user properties provided.")

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def send_welcome_email(self, search_filter, client_id=None):

        """
        Send welcome e-mail to users identified by the search filter(s) provided.

        :param search_filter:   Search filter(s)
        :type  search_filter:   list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Job ID
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "client/{}/user/sendWelcomeEmail".format(str(client_id))

        body = {
            "filterRequest": {
                "filters": search_filter
            }
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def get_model(self, client_id=None):

        """
        Get available projections and models for Users.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Users projections and models are returned.
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._model(self.subject_name, client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return response

    def suggest(self, search_filter_1, search_filter_2, client_id=None):

        """
        Suggest values for filter fields.

        :param search_filter_1:     Search Filter 1
        :type  search_filter_1:     list

        :param search_filter_2:     Search Filter 2
        :type  search_filter_2:     list

        :param client_id:           Client ID
        :type  client_id:           int

        :return:    Value suggestions
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._suggest(self.subject_name, search_filter_1, search_filter_2, client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return response


"""
   Copyright 2019 RiskSense, Inc.
   
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at:
   
   http://www.apache.org/licenses/LICENSE-2.0
   
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
