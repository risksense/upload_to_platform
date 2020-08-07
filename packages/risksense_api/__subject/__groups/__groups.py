""" *******************************************************************************************************************
|
|  Name        :  __groups.py
|  Module      :  risksense_api
|  Description :  A class to be used for searching for and updating groups on the RiskSense Platform.
|  Copyright   : (c) RiskSense, Inc.
|  License     : Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

import json
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *


class Groups(Subject):

    """ Groups Class """

    def __init__(self, profile):

        """
        Initialization of Groups object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """

        self.subject_name = "group"
        Subject.__init__(self, profile, self.subject_name)

    def get_single_search_page(self, search_filters, projection=Projection.BASIC, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns groups based on the provided filter(s) and other parameters.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param projection:      Projection to use
        :type  projection:      str

        :param page_num:        The page number of results to be returned.
        :type  page_num:        int

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      The field to be used for sorting the results returned.
        :type  sort_field       SortField attribute

        :param sort_dir:        The direction of sorting to be used. (SortDirection.ASC or SortDirection.DESC)
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises PageSizeError:
        """

        func_args = locals()
        func_args.pop('self')

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        try:
            response = self._get_single_search_page(self.subject_name, **func_args)
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
            raise

        return response


    def search(self, search_filters, projection=Projection.BASIC, page_size=150,
               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns groups based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param projection:      Projection to use
        :type  projection:      str

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      The field to be used for sorting the results returned.
        :type  sort_field       SortField attribute

        :param sort_dir:        The direction of sorting to be used. (SortDirection.ASC or SortDirection.DESC)
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A list containing all host findings returned by the search using the filter provided.
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

    def create(self, name, client_id=None):

        """
        Creates a new group.

        :param name:                The name to be used for the new group.
        :type  name:                str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The new group ID is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        body = {
            "name": name
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        new_group_id = jsonified_response['id']

        return new_group_id

    def delete(self, search_filters, client_id=None):

        """
        Deletes groups as specified in search_filters.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A list of dicts containing name/assetCriticality of deleted groups is returned.
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/delete"

        body = {
            "filterRequest": {
                "filters": search_filters
            }
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        deleted_groups = jsonified_response['projections']['fields']

        return deleted_groups

    def update_single_group(self, group_id, client_id=None, **kwargs):

        """
        Updates a group name and/or asset criticality.

        :param group_id:    The group ID.
        :type  group_id:    int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  The new name.  (str)
        :keyword asset_criticality:     The new asset criticality.  (int)

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        name = kwargs.get('name', None)
        asset_criticality = kwargs.get('asset_criticality', None)

        url = self.api_base_url.format(str(client_id)) + "/" + str(group_id)

        body = {}

        if name is not None:
            body.update(name=name)

        if asset_criticality is not None:
            body.update(assetCriticality=asset_criticality)

        if body == {}:
            raise ValueError("Body is empty. Please provide name and/or asset_criticality")

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def update_multiple_groups(self, search_filters, new_asset_criticality, client_id=None):

        """
        Updates the default asset criticality of multiple groups, based on the specified filter(s).

        :param search_filters:          A list of dictionaries containing filter parameters.
        :type  search_filters:          list

        :param new_asset_criticality:   Reflects the default criticality of Hosts in the groups.
        :type  new_asset_criticality:   integer

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    The job ID is returned
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        body = {
            "assetCriticality": new_asset_criticality,
            "filterRequest": {
                "filters": search_filters
            }
        }

        url = self.api_base_url.format(str(client_id)) + "/update"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def assign(self, search_filters, user_ids, client_id=None):

        """
        Assign group(s) to user IDs, based on specified filter(s)

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param user_ids:        A list of user IDs.
        :type  user_ids:        list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/assign"

        body = {
            "filters": search_filters,
            "userIds": user_ids
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def unassign(self, search_filters, user_ids, client_id=None):

        """
        Unassign group(s) from user IDs, based on specified filter(s)

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param user_ids:        A list of user IDs.
        :type  user_ids:        list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/unassign"

        body = {
            "filters": search_filters,
            "userIds": user_ids
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
        Get available projections and models for Groups.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Group projections and models are returned.
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