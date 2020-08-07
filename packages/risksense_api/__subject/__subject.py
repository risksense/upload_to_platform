""" *******************************************************************************************************************
|
|  Name        :  __subject.py
|  Description :  Subject
|  Project     :  risksense_api
|  Copyright   :  2019 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
import time
import concurrent.futures
import progressbar
from .._params import *
from .._api_request_handler import *


class Subject:

    """ Subject class """

    def __init__(self, profile, subject_name=""):

        """ Initialize Subject class """

        self.profile = profile
        self.subject_name = subject_name
        self.request_handler = ApiRequestHandler(self.profile.api_key, proxy=self.profile.proxy)
        self.api_base_url = self.profile.platform_url + "/api/v1/client/{}/" + subject_name

    def bulk_filtered_op(self, func_name, list_of_filters, client_id, **func_args):

        """
        A wrapper for repeating functions that require use of a filter to ID assets/findings to be operated on.  This
        function runs these operations in a threaded fashion.

        :param func_name:           Name of the function that should be repeated
        :type  func_name:           function

        :param list_of_filters:     list of lists of all of the filters that should be cycled through when repeating the function
        :type  list_of_filters:     list

        :param client_id:           Client ID
        :type  client_id:           int

        :param func_args:           Args required by the function to be repeated
        :type  func_name:           dict

        :return:    Job IDs
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        job_ids = []
        filter_count = len(list_of_filters)

        if self.profile.use_prog_bar:
            prog_bar = progressbar.ProgressBar(max_value=filter_count)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.profile.num_thread_workers) as executor:
            counter = 1
            future_to_filter = {executor.submit(func_name, filter_x, client_id=client_id,
                                                **func_args): filter_x for filter_x in list_of_filters}

            for future in concurrent.futures.as_completed(future_to_filter):
                try:
                    data = future.result()
                except (RequestFailed, StatusCodeError, MaxRetryError):
                    continue

                if 'id' in data:
                    job_ids.append(data['id'])

                if self.profile.use_prog_bar:
                    prog_bar.update(counter)
                    time.sleep(0.1)
                    counter += 1

        if self.profile.use_prog_bar:
            prog_bar.finish()

        return job_ids

    def bulk_op(self, func_name, list_of_args, client_id):

        """
        A wrapper for repeating functions.  This function runs these operations in a threaded fashion.

        :param func_name:           Name of the function that should be repeated
        :type  func_name:           function

        :param list_of_args:        list of dicts containing all of the args that should be cycled through
                                    when repeating the function
        :type  list_of_args:        list

        :param client_id:           Client ID
        :type  client_id:           int

        :return:    Job IDs
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        job_ids = []
        num_to_process = len(list_of_args)

        if self.profile.use_prog_bar:
            prog_bar = progressbar.ProgressBar(max_value=num_to_process)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.profile.num_workers) as executor:
            counter = 1
            future_to_process = {executor.submit(func_name, client_id=client_id, **func_args): func_args for func_args in list_of_args}

            for future in concurrent.futures.as_completed(future_to_process):
                try:
                    data = future.result()
                except (RequestFailed, StatusCodeError, MaxRetryError):
                    continue

                if 'id' in data:
                    job_ids.append(data['id'])

                if self.profile.use_prog_bar:
                    prog_bar.update(counter)
                    time.sleep(0.1)
                    counter += 1

        if self.profile.use_prog_bar:
            prog_bar.finish()

        return job_ids

    def get_filter_fields(self, client_id=None):

        """
        Get a list of available application finding filter fields.

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    A list of available filters is returned.
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError;
        """

        # Occurs if: the Subject base class itself is instantiated (which is not intended usage of Subject class); a
        # child class of Subject doesn't set its subject_name or overrides its initial subject name.
        if not self.subject_name:
            raise ValueError("The subject's name must be set in order to retrieve its filter field data.")

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            fields_list = self._filter_fields(self.subject_name, client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return fields_list

    def _export(self, subject_name, **kwargs):

        """
        Initiate export for given subject, based on provided filter

        :param subject_name:    Subject name
        :type  subject_name:    str

        :keyword search_filters:    list    List of filters to use
        :keyword file_type:         str     File Type (CSV, XML, XLSX)
        :keyword comment:           str     Comment
        :keyword file_name:         str     File name
        :keyword client_id:         int     Client ID

        :return:    Export ID
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        search_filters = kwargs.get('search_filters')
        file_type = kwargs.get('file_type')
        comment = kwargs.get('comment')
        file_name = kwargs.get('file_name')
        client_id = kwargs.get('client_id')

        if file_type not in ["CSV", "XML", "XLSX"]:
            raise ValueError("Invalid file type. Type must be CSV, XML, or XLSX")

        url = self.profile.platform_url + "/api/v1/client/{}/{}/export".format(str(client_id), subject_name)

        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "fileType": file_type,
            "comment": comment,
            "fileName": file_name
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        export_id = jsonified_response['id']

        return export_id

    def _filter_fields(self, subject_name, client_id):

        """
        Get a list of available filter fields for the given subject.

        :param subject_name:    Subject Name
        :type  subject_name:    str

        :param client_id:       Client ID
        :type  client_id:       int

        :return:    A list of available filters is returned.
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        url = self.profile.platform_url + "/api/v1/client/{}/{}/filter".format(str(client_id), subject_name)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        available_filters = jsonified_response

        return available_filters


    def _model(self, subject_name, client_id):

        """
        Get a subject's available projections and models.

        :param subject_name:    Subject Name
        :type  subject_name:    str

        :param client_id:       Client ID
        :type  client_id:       int

        :return:    The subject's projections and models are returned.
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        url = self.profile.platform_url + "/api/v1/client/{}/{}/model".format(str(client_id), subject_name)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def _suggest(self, subject_name, search_filter_1, search_filter_2, client_id):

        """
        Suggest values for filter fields.

        :param subject_name:        Subject Name
        :type  subject_name:        str

        :param search_filter_1:     Search Filter 1
        :type  search_filter_1:     list

        :param search_filter_2:     Search Filter 2
        :type  search_filter_2:     list

        :param client_id:           Client ID
        :type  client_id:           int

        :return:    Suggestion Response
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        url = self.profile.platform_url + "/api/v1/client/{}/{}/suggest".format(str(client_id), subject_name)

        body = {
            "filters": search_filter_1,
            "filter": search_filter_2
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def _add_group(self, subject_name, search_filter, group_ids, client_id):

        """
        Add hosts or applications to a group

        :param subject_name:    Subject Name
        :type  subject_name:    str

        :param search_filter:   Search Filter
        :type  search_filter:   list

        :param group_ids:       List of group IDs to add
        :type  group_ids:       list

        :param client_id:       Client ID
        :type  client_id:       int

        :return:    Job ID
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        url = self.profile.platform_url + "/api/v1/client/{}/{}/add-group".format(str(client_id), subject_name)

        body = {
            "filterRequest": {
                "filters": search_filter
            },
            "targetGroupIds": group_ids
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def _remove_group(self, subject_name, search_filter, group_ids, client_id):

        """
        Remove hosts or applications from a group

        :param subject_name:    Subject Name
        :type  subject_name:    str

        :param search_filter:   Search Filter
        :type  search_filter:   list

        :param group_ids:       List of group IDs to remove
        :type  group_ids:       list

        :param client_id:       Client ID
        :type  client_id:       int

        :return:    Job ID
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        url = self.profile.platform_url + "/api/v1/client/{}/{}/remove-group".format(str(client_id), subject_name)

        body = {
            "filterRequest": {
                "filters": search_filter
            },
            "targetGroupIds": group_ids
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def _get_single_search_page(self, subject_name, **func_args):

        """
        Search and return a single page of search results.

        :param subject_name:    Subject
        :type subject_name:     str

        :param func_args:       args to be passed to search function
        :type  func_args:       dict

        :return:    The JSONified response from the platform

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises PageSizeError:
        """

        search_filters = func_args.get('search_filters')
        projection = func_args.get('projection', 'basic')
        page_num = func_args.get('page_num')
        page_size = func_args.get('page_size')
        sort_field = func_args.get('sort_field')
        sort_dir = func_args.get('sort_dir')
        client_id = func_args.get('client_id')

        url = self.profile.platform_url + "/api/v1/client/{}/{}/search".format(str(client_id), subject_name)

        body = {
            "filters": search_filters,
            "projection": projection,
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

    def _search(self, subject, func_name, page_range, **func_args):

        """
        Threaded search, supporting multiple threads.  Combines all results in a single list and returns.

        :param subject:     Subject
        :type  subject:     str

        :param func_name:   Search function name
        :type  func_name:   function

        :param page_range:  Page range
        :type  page_range:  range

        :param func_args:   args to be passed to search function
        :type  func_args:   dict

        :return:    List of all results returned by search function
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises PageSizeError:
        """
        all_results = []
        if 'page_num' in func_args:
            func_args = func_args.pop('page_num')

        if self.profile.use_prog_bar:
            try:
                max_val = (max(page_range) + 1)
            except ValueError:
                max_val = 1

            prog_bar = progressbar.ProgressBar(max_value=max_val)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.profile.num_thread_workers) as executor:
            counter = 1
            future_to_page = {executor.submit(func_name, page_num=page, **func_args): page for page in page_range}

            for future in concurrent.futures.as_completed(future_to_page):
                # page = future_to_page[future]
                try:
                    data = future.result()
                except PageSizeError:
                    raise
                except (RequestFailed, StatusCodeError, MaxRetryError):
                    continue

                if '_embedded' in data:
                    if 'projection' in func_args and subject == "group":
                        if func_args['projection'] == Projection.DETAIL:
                            items = data['_embedded'][subject + 'Details']
                    else:
                        items = data['_embedded'][subject + 's']
                    for item in items:
                        all_results.append(item)

                if self.profile.use_prog_bar:
                    prog_bar.update(counter)
                    time.sleep(0.1)
                    counter += 1

        if self.profile.use_prog_bar:
            prog_bar.finish()

        sort_field = func_args['sort_field']
        sort_dir = func_args['sort_dir']

        sort_reversal = True

        # Sort the results
        if sort_dir != SortDirection.DESC:
            sort_reversal = False

        sorted_results = sorted(all_results, key=lambda k: k[sort_field], reverse=sort_reversal)

        return sorted_results

    def _get_page_info(self, subject_name, search_filters, page_size=150, client_id=None):

        """
        Gets page info (total count, num of pages) for a search.

        :param subject_name:        Subject Name
        :type  subject_name:        str

        :param search_filters:      Search Filters
        :type  search_filters:      list

        :param page_size:           Page Size
        :type  page_size:           int

        :param client_id:           Client ID
        :type  client_id:           int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises PageSizeError:
        """

        func_args = locals()
        func_args.pop('self')

        if client_id is None:
            func_args['client_id'] = self._use_default_client_id()[1]

        try:
            response = self._get_single_search_page(sort_dir=SortDirection.DESC, sort_field=SortField.ID, **func_args)
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
            raise

        count = response['page']['totalElements']
        num_pages = response['page']['totalPages']

        return count, num_pages

    def _use_default_client_id(self):

        """
        Return default client ID twice.

        :return:    default client ID (twice)
        :rtype:     tuple
        """

        return self.profile.default_client_id, self.profile.default_client_id

    @staticmethod
    def _strip_nones_from_dict(body_to_strip):

        """
        Strip values from dict that are equal to None

        :param body_to_strip:   Body
        :type  body_to_strip:   dict

        :return:    Cleaned up dict
        :rtype:     dict
        """

        clean_dict = {}
        for item in body_to_strip:
            if body_to_strip[item] is not None:
                clean_dict.update({item: body_to_strip[item]})
        return clean_dict


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
