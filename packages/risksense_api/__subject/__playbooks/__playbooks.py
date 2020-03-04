""" *******************************************************************************************************************
|
|  Name        :  __playbooks.py
|  Description :  Playbooks
|  Project     :  risksense_api
|  Copyright   :  2020 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
import time
import concurrent.futures
import progressbar
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *


class Playbooks(Subject):

    """ Playbooks class """

    def __init__(self, profile):

        """
        Initialization of Playbooks object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """
        Subject.__init__(self, profile, Subject.PLAYBOOK)

    def create(self, name, description, schedule_freq, client_id=None, **kwargs):

        """

        :param name:            Name
        :type  name:            str

        :param description:     Description
        :type  description:     str

        :param schedule_freq:   Schedule Frequency (ScheduleFreq.DAILY, ScheduleFreq.WEEKLY, ScheduleFreq.MONTHLY)
        :type  schedule_freq:   str

        :param client_id:       Client ID
        :type  client_id:       int

        :keyword hour_of_day:   Hour of the day   (int)
        :keyword day_of_week:   Day of the week   (int)
        :keyword day_of_month:  Day of the month  (int)

        :return:    Playbook UUID
        :rtype:     str
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/supported-inputs"

        hour_of_day = kwargs.get("hour_of_day", None)
        day_of_week = kwargs.get("day_of_week", None)
        day_of_month = kwargs.get("day_of_month", None)

        body = {
            "name": name,
            "description": description,
            "schedule": {
                "type": schedule_freq
            }
        }

        if schedule_freq == ScheduleFreq.DAILY:
            if hour_of_day is None:
                raise ValueError("hour_of_day is required for a DAILY connector schedule.")
            body['schedule'].update(hourOfDay=hour_of_day)

        elif schedule_freq == ScheduleFreq.WEEKLY:
            if day_of_week is None and hour_of_day is None:
                raise ValueError("hour_of_day and day_of_week are required for a WEEKLY connector schedule.")
            if day_of_week is None:
                raise ValueError("day_of_week is required for a WEEKLY connector schedule.")
            if hour_of_day is None:
                raise ValueError("hour_of_day is required for a WEEKLY connector schedule.")
            body['schedule'].update(hourOfDay=hour_of_day)
            body['schedule'].update(dayOfWeek=day_of_week)

        elif schedule_freq == ScheduleFreq.MONTHLY:
            if day_of_month is None and hour_of_day is None:
                raise ValueError("day_of_month and day_of_week are required for a WEEKLY connector schedule.")
            if day_of_month is None:
                raise ValueError("day_of_month is required for a WEEKLY connector schedule.")
            if hour_of_day is None:
                raise ValueError("hour_of_day is required for a WEEKLY connector schedule.")
            body['schedule'].update(hourOfDay=hour_of_day)
            body['schedule'].update(dayOfMonth=day_of_month)

        else:
            raise ValueError("schedule_freq should be one of DAILY, WEEKLY, or MONTHLY")

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        new_playbook_uuid = jsonified_response['uuid']

        return new_playbook_uuid

    def get_supported_inputs(self, client_id=None):

        """
        Get a list of supported playbook inputs.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    List of supported playbook inputs
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_supported_actions(self, client_id=None):

        """
        Get a list of supported playbook actions.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    List of supported playbook actions
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/supported-actions"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_supported_frequencies(self, client_id=None):

        """
        Get a list of supported playbook frequencies.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    List of supported playbook frequencies
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/supported-frequencies"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_supported_outputs(self, client_id=None):

        """
        Get a list of supported playbook outputs.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    List of supported playbook outputs
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/supported-outputs"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_subject_supported_actions(self, client_id=None):

        """
        Get the mapping of subject to the subject's list of available actions

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Mappings of supported playbook subject actions
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/subject-supported-actions"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_playbooks_single_page(self, page_size=1000, page_num=0, sort_dir=SortDirection.ASC, client_id=None):

        """
        Fetch all available playbooks in a client

        :param page_size:   Page Size
        :type  page_size:   int

        :param page_num:    Page Number
        :type  page_num:    int

        :param sort_dir:    Sort Direction
        :type  sort_dir:    str

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Available Playbooks
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/fetch"

        params = {
            "size": page_size,
            "page": page_num,
            "sort": sort_dir
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_all_playbooks(self, client_id=None):

        """
        Get all playbooks for a client.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    All Playbooks for a client
        :rtype:     list
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/fetch"

        try:
            num_pages = self._get_page_info_for_fetch(url, page_size=1000)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        page_range = range(0, num_pages)

        try:
            playbooks = self._fetch_in_bulk(self.get_playbooks_single_page, page_range=page_range, client_id=client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return playbooks

    def get_specific_playbook(self, playbook_uuid, client_id=None):

        """
        Fetch a specific playbook by UUID.

        :param playbook_uuid:   Playbook UUID
        :type  playbook_uuid:   str

        :param client_id:       Client ID
        :type  client_id:       int

        :return:    Playbook
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/fetch/{}".format(playbook_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_specific_playbook_rule(self, playbook_rule_uuid, client_id=None):

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/rule/{}".format(playbook_rule_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_playbook_rules_single_page(self, playbook_uuid, page_size=1000, page_num=0,
                                       sort_dir=SortDirection.ASC, client_id=None):

        """
        Get rules for a playbook

        :param playbook_uuid:   Playbook UUID
        :type  playbook_uuid:   str

        :param page_size:       Page Size
        :type  page_size:       int

        :param page_num:        Page Number
        :type  page_num:        int

        :param sort_dir:        Sort Direction
        :type  sort_dir:        str

        :param client_id:       Client ID
        :type  client_id:       int

        :return:    Playbook Rules
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/rules".format(playbook_uuid)

        params = {
            "size": page_size,
            "page": page_num,
            "sort": sort_dir
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_playbook_rules(self, playbook_uuid, client_id=None):

        """
        Get all rules for a specific playbook.

        :param playbook_uuid:   Playbook UUID
        :type  playbook_uuid:   str

        :param client_id:       Client ID
        :type  client_id:       int

        :return:    List of all rules found for specified playbook
        :rtype:     list
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/rules".format(playbook_uuid)

        try:
            num_pages = self._get_page_info_for_fetch(url, page_size=1000)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        page_range = range(0, num_pages)

        try:
            rules = self._fetch_in_bulk(self.get_playbook_rules_single_page, playbook_uuid=playbook_uuid,
                                        page_range=page_range, client_id=client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return rules

    def get_playbook_details(self, playbook_uuid, client_id=None):

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(playbook_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def run_playbook(self, playbook_uuid, client_id=None):

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/run".format(playbook_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    ##### BEGIN PRIVATE FUNCTIONS #####################################################################################

    def _get_page_info_for_fetch(self, url, page_size):

        """
        Get number of available pages for fetch.

        :param url:         URL of endpoint
        :type  url:         str

        :param page_size:   page size
        :type  page_size:   int

        :return:    Total number of available pages
        :rtype:     int
        """

        params = {
            "size": page_size
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        total_pages = jsonified_response['totalPages']

        return total_pages

    def _fetch_in_bulk(self, func_name, page_range, **func_args):

        """
        Threaded fetch of playbook info, supporting multiple threads.
        Combines all results in a single list and returns.

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
                try:
                    data = future.result()
                except PageSizeError:
                    raise
                except (RequestFailed, StatusCodeError, MaxRetryError):
                    continue

                if 'content' in data:
                    items = data['content']
                    for item in items:
                        all_results.append(item)

                if self.profile.use_prog_bar:
                    prog_bar.update(counter)
                    time.sleep(0.1)
                    counter += 1

        if self.profile.use_prog_bar:
            prog_bar.finish()

        return all_results


"""
   Copyright 2020 RiskSense, Inc.

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
