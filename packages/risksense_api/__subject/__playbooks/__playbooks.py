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
        self.subject_name = "playbook"
        Subject.__init__(self, profile, self.subject_name)

    def get_supported_inputs(self, client_id=None):

        """
        Get a list of supported playbook inputs.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Supported inputs
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/supported-inputs"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        supported_inputs = json.loads(raw_response.text)

        return supported_inputs

    def get_supported_actions(self, client_id=None):

        """
        Get a list of supported playbook actions.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Supported actions
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

        supported_actions = json.loads(raw_response.text)

        return supported_actions

    def get_supported_frequencies(self, client_id=None):

        """
        Get a list of supported playbook frequencies.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Supported frequencies
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

        supported_frequencies = json.loads(raw_response.text)

        return supported_frequencies

    def get_supported_outputs(self, client_id=None):

        """
        Get a list of supported playbook outputs.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Supported outputs
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

        supported_outputs = json.loads(raw_response.text)

        return supported_outputs

    def get_subject_supported_actions(self, client_id=None):

        """
        Get a list of subject-supported playbook actions.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Subject-supported actions
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

        supported_actions = json.loads(raw_response.text)

        return supported_actions

    def get_playbooks_single_page(self, page_size=1000, page_num=0, sort_dir=SortDirection.ASC, client_id=None):

        """
        Fetch a single page of playbooks from client

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
        :raises PageSizeError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if page_size > 1000:
            raise PageSizeError("Page size must be <= 1000")

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

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/fetch"

        try:
            num_pages = self._get_playbook_page_info(url, page_size=1000)
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

    def get_single_page_playbook_rules(self, playbook_uuid, page_num=0, page_size=1000, sort_dir=SortDirection.ASC, client_id=None):

        """
        Get a single page of rules for a specific playbook

        :param playbook_uuid:   Playbook UUID
        :type  playbook_uuid:   str

        :param page_num:        Page number to retrieve
        :type  page_num:        int

        :param page_size:       Number of items per page to return
        :type  page_size:       int

        :param sort_dir:        Sort Direction
        :type  sort_dir:        str

        :param client_id:       Client ID
        :type  client_id:       int

        :return:    Playbook rules
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises PageSizeError:
        """

        if page_size > 1000:
            raise PageSizeError("Page Size must be <= 1000")

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        params = {
            "size": page_size,
            "page": page_num,
            "sort": sort_dir
        }

        url = self.api_base_url.format(str(client_id)) + "/{}/rules".format(playbook_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_all_rules_for_playbook(self, playbook_uuid, sort_dir=SortDirection.ASC, client_id=None):

        """
        Get a single page of rules for a specific playbook

        :param playbook_uuid:   Playbook UUID
        :type  playbook_uuid:   str

        :param sort_dir:        Sort Direction
        :type  sort_dir:        str

        :param client_id:       Client ID
        :type  client_id:       int

        :return:    All playbook rules
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/rules".format(playbook_uuid)

        page_size = 1000

        try:
            num_pages = self._get_playbook_page_info(url, page_size)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        page_range = range(0, num_pages)

        search_func_params = {
            "playbook_uuid": playbook_uuid,
            "page_size": page_size,
            "sort_dir": sort_dir,
            "client_id": client_id
        }

        try:
            all_rules = self._fetch_in_bulk(self.get_single_page_playbook_rules, page_range, **search_func_params)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return all_rules

    def add_rule(self, playbook_uuid, rule_name, rule_desc, rule_input, rule_action_type,
                 rule_action, rule_output_type, rule_output, client_id=None):

        """
        Add a rule to a playbook.

        :param playbook_uuid:       Playbook UUID
        :type  playbook_uuid:       str

        :param rule_name:           Rule Name
        :type  rule_name:           str

        :param rule_desc:           Rule Description
        :type  rule_desc:           str

        :param rule_input:          Rule Input
        :type  rule_input:          str

        :param rule_action_type:    Rule Action Type
        :type  rule_action_type:    str

        :param rule_action:         Rule action to take
        :type  rule_action:         dict

        :param rule_output_type:    Rule output type
        :type  rule_output_type:    str

        :param rule_output:         Rule output
        :type  rule_output:         dict

        :param client_id:           Client ID
        :type  client_id:           int

        :return:    List containing dict of rule details.
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/rule".format(playbook_uuid)

        body = {
            "name": rule_name,
            "description": rule_desc,
            "input": rule_input,
            "actionType": rule_action_type,
            "action": rule_action,
            "outputType": rule_output_type,
            "output": rule_output
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def add_rule_with_file(self, playbook_uuid, rule_name, rule_desc, rule_input, rule_action_type,
                           rule_action, rule_output_type, rule_output, file_name, file_path, client_id=None):

        """
        Add a rule to a playbook with a file.

        :param playbook_uuid:       Playbook UUID
        :type  playbook_uuid:       str

        :param rule_name:           Rule Name
        :type  rule_name:           str

        :param rule_desc:           Rule Description
        :type  rule_desc:           str

        :param rule_input:          Rule Input
        :type  rule_input:          str

        :param rule_action_type:    Rule Action Type
        :type  rule_action_type:    str

        :param rule_action:         Rule action to take
        :type  rule_action:         dict

        :param rule_output_type:    Rule output type
        :type  rule_output_type:    str

        :param rule_output:         Rule output
        :type  rule_output:         dict

        :param file_name:           Name to use for file you are uploading
        :type  file_name:           str

        :param file_path:           Path to file to be uploaded
        :type  file_path:           str

        :param client_id:           Client ID
        :type  client_id:           int

        :return:    List containing dict of rule details.
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises FileNotFoundError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/rule/with-files".format(playbook_uuid)

        rule = {
            "name": rule_name,
            "description": rule_desc,
            "input": rule_input,
            "actionType": rule_action_type,
            "action": rule_action,
            "outputType": rule_output_type,
            "output": rule_output
        }

        serialized_rule = json.dumps(rule)

        try:
            body = {
                "playbookUuid": playbook_uuid,
                "files": (file_name, open(file_path, 'rb')),
                "serializedPlaybookRule": serialized_rule
            }
        except FileNotFoundError:
            raise

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response



    def create(self, name, description, schedule_freq, hour_of_day, client_id=None, **kwargs):

        """
        Create a new playbook

        :param name:            Name
        :type  name:            str

        :param description:     Description
        :type  description:     str

        :param schedule_freq:   Schedule Frequency (ScheduleFreq.DAILY, ScheduleFreq.WEEKLY,
                                                    ScheduleFreq.MONTHLY, 'DISABLED')
        :type  schedule_freq:   str

        :param client_id:       Client ID
        :type  client_id:       int

        :param hour_of_day:     Hour of the day
        :type  hour_of_day:     int

        :keyword day_of_week:   Day of the week   (int)
        :keyword day_of_month:  Day of the month  (int)

        :return:    Playbook UUID
        :rtype:     str

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        day_of_week = kwargs.get("day_of_week", None)
        day_of_month = kwargs.get("day_of_month", None)

        body = {
            "name": name,
            "description": description,
            "schedule": {
                "type": schedule_freq,
                "hourOfDay": hour_of_day
            }
        }

        try:
            supported_freqs = self.get_supported_frequencies(client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        if schedule_freq not in supported_freqs:
            raise ValueError(f"schedule_freq should be one of {schedule_freq}")

        elif schedule_freq == ScheduleFreq.WEEKLY:
            if day_of_week < 1 or day_of_week > 7:
                raise ValueError("valid day_of_week (1-7) is required for a WEEKLY connector schedule.")
            body['schedule'].update(dayOfWeek=day_of_week)

        elif schedule_freq == ScheduleFreq.MONTHLY:
            if day_of_month < 1 or day_of_month > 31:
                raise ValueError("valid day_of_month (1-31) is required for a MONTHLY connector schedule.")
            body['schedule'].update(dayOfMonth=day_of_month)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        new_playbook_uuid = jsonified_response['uuid']

        return new_playbook_uuid

    def update(self, playbook_uuid, name, description, schedule_freq, hour_of_day, client_id=None, **kwargs):

        """
        Update a playbook

        :param playbook_uuid:   Playbook UUID
        :type  playbook_uuid:   str

        :param name:            Name
        :type  name:            str

        :param description:     Description
        :type  description:     str

        :param schedule_freq:   Schedule Frequency (ScheduleFreq.DAILY, ScheduleFreq.WEEKLY,
                                                    ScheduleFreq.MONTHLY, 'DISABLED')
        :type  schedule_freq:   str

        :param client_id:       Client ID
        :type  client_id:       int

        :param hour_of_day:     Hour of the day
        :type  hour_of_day:     int

        :keyword day_of_week:   Day of the week   (int)
        :keyword day_of_month:  Day of the month  (int)

        :return:    Playbook UUID
        :rtype:     str

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(playbook_uuid)

        day_of_week = kwargs.get("day_of_week", None)
        day_of_month = kwargs.get("day_of_month", None)

        body = {
            "name": name,
            "description": description,
            "schedule": {
                "type": schedule_freq,
                "hourOfDay": hour_of_day
            }
        }

        try:
            supported_freqs = self.get_supported_frequencies(client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        if schedule_freq not in supported_freqs:
            raise ValueError(f"schedule_freq should be one of {schedule_freq}")

        elif schedule_freq == ScheduleFreq.WEEKLY:
            if day_of_week < 1 or day_of_week > 7:
                raise ValueError("valid day_of_week (1-7) is required for a WEEKLY connector schedule.")
            body['schedule'].update(dayOfWeek=day_of_week)

        elif schedule_freq == ScheduleFreq.MONTHLY:
            if day_of_month < 1 or day_of_month > 31:
                raise ValueError("valid day_of_month (1-31) is required for a MONTHLY connector schedule.")
            body['schedule'].update(dayOfMonth=day_of_month)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def delete(self, playbook_uuid, client_id=None):

        """
        Delete a playbook.

        :param playbook_uuid:   playbook UUID
        :type  playbook_uuid:   str

        :param client_id:       client ID
        :type  client_id:       int

        :return:    true/false indicating successful deletion
        :rtype:     bool

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        deleted = False

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(playbook_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
            if raw_response.status_code == 204:
                deleted = True
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return deleted

    def get_playbook_details(self, playbook_uuid, client_id=None):

        """
        Get the details for a specific playbook

        :param playbook_uuid:   playbook UUID
        :type  playbook_uuid:   str

        :param client_id:       client ID
        :type  client_id:       int

        :return:    Playbook details
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(playbook_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def rule_reorder(self, playbook_uuid, rule_uuids, client_id=None):

        """
        Reorder playbook rules for an already existing playbook

        :param playbook_uuid:   UUID for playbook to be reordered
        :type  playbook_uuid:   str

        :param rule_uuids:      A list of rule UUIDs (strings), in the order desired
        :type  rule_uuids:      list

        :param client_id:       Client ID
        :type  client_id:       int

        :return:    List of reordered rule definitions
        :rtype:     list

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/rule-reorder".format(playbook_uuid)

        if type(rule_uuids) is not list:
            raise ValueError(f"rule_uuids should be a list of strings.")

        body = {
            "ruleUuids": rule_uuids
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def update_rule(self, rule_uuid, playbook_name, playbook_desc, playbook_input, playbook_action_type,
                    playbook_action, playbook_output_type, playbook_output, client_id=None):

        """
        Update an existing playbook rule

        :param rule_uuid:               UUID for rule to be updated
        :type  rule_uuid:               str

        :param playbook_name:           Playbook name
        :type  playbook_name:           str

        :param playbook_desc:           Playbook description
        :type  playbook_desc:           str

        :param playbook_input:          Playbook Input
        :type  playbook_input:          str

        :param playbook_action_type:    Playbook action type
        :type  playbook_action_type:    str

        :param playbook_action:         Playbook action
        :type  playbook_action:         dict

        :param playbook_output_type:    Playbook output type
        :type  playbook_output_type:    str

        :param playbook_output:         Playbook output
        :type  playbook_output:         dict

        :param client_id:               Client ID
        :type  client_id:               str

        :return:    Indication of success
        :rtype:     bool

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/rule/{}".format(rule_uuid)

        try:
            supported_inputs = self.get_supported_inputs(client_id)
        except (RequestFailed, MaxRetryError, StatusCodeError):
            raise

        try:
            supported_action_types = self.get_supported_actions(client_id)
        except (RequestFailed, MaxRetryError, StatusCodeError):
            raise

        try:
            supported_output_types = self.get_supported_outputs(client_id)
        except (RequestFailed, MaxRetryError, StatusCodeError):
            raise

        if playbook_input not in supported_inputs:
            raise ValueError(f"playbook_input must be one of {supported_inputs}")

        if playbook_action_type not in supported_action_types:
            raise ValueError(f"playbook_action_type must be one of {supported_action_types}")

        if playbook_output_type not in supported_output_types:
            raise ValueError(f"playbook_output_type must be one of {supported_action_types}")

        body = {
            "name": playbook_name,
            "description": playbook_desc,
            "input": playbook_input,
            "actionType": playbook_action_type,
            "action": playbook_action,
            "outputType": playbook_output_type,
            "output": playbook_output
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
            if raw_response.status_code == 200:
                return True
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

    def delete_playbook_rule(self, rule_uuid, client_id=None):

        """
        Delete an existing playbook rule.

        :param rule_uuid:   Rule UUID
        :type  rule_uuid:   str

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Indication of success
        :rtype:     bool

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/rule/{}".format(rule_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
            if raw_response.status_code == 204:
                return True
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

    def get_specific_playbook_rule(self, rule_uuid, client_id=None):

        """
        Get details for a specific playbook rule.

        :param rule_uuid:   Playbook rule UUID
        :type  rule_uuid:   str

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Playbook rule details
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/rule/{}".format(rule_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def delete_file_from_rule(self, rule_uuid, file_uuid, client_id=None):

        """
        Delete a file from a playbook rule

        :param rule_uuid:   Playbook rule UUID
        :type  rule_uuid:   str

        :param file_uuid:   File UUID
        :type  file_uuid:   str

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Indicator of deletion success
        :rtype:     bool

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/rule/{}/file/{}".format(rule_uuid, file_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
            if raw_response.status_code == 204:
                return True
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

    def download_file_from_rule(self, rule_uuid, file_uuid, file_destination, client_id=None):

        """
        Download a file from an existing playbook rule.

        :param rule_uuid:           Rule UUID
        :type  rule_uuid:           str

        :param file_uuid:           File UUID
        :type  file_uuid:           str

        :param file_destination:    File destination path
        :type  file_destination:    str

        :param client_id:           Client ID
        :type  client_id:           int

        :return:    Indicator of download success
        :rtype:     bool

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises FileNotFoundError:
        :raises FileExistsError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/rule/{}/file/{}".format(rule_uuid, file_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        try:
            open(file_destination, "wb").write(raw_response.content)
            success = True
        except (FileNotFoundError, FileExistsError):
            raise

        return success

    def attach_file_to_rule(self, rule_uuid, file_name, file_path, client_id=None):

        """
        Attach a file to an existing rule.

        :param rule_uuid:   Playbook rule UUID
        :type  rule_uuid:   str

        :param file_name:   Name for uploaded file
        :type  file_name:   str

        :param file_path:   Path to file to be uploaded
        :type  file_path:   str

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    JSONified response from platform
        :rtype:     dict
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/rule/{}/file".format(rule_uuid)

        upload_file = {'file': (file_name, open(file_path, 'rb'))}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=upload_file)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise
        except FileNotFoundError:
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response


    def toggle_enabled(self, playbook_uuids, enabled, client_id=None):

        """
        Enable/Disable playbooks.

        :param playbook_uuids:  A list of Playbook UUIDs to enable/disable
        :type  playbook_uuids:  list

        :param enabled:         Enable playbooks?
        :type  enabled:         bool

        :param client_id:       Client ID
        :type  client_id:       int

        :return:    JSON response from platform
        :rtype:     dict
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/toggle-enabled"

        body = {
            "playbookUuids": playbook_uuids,
            "enabled": enabled
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def run_playbook(self, playbook_uuid, client_id=None):

        """
        Run a playbook.

        :param playbook_uuid:   Playbook UUID
        :type  playbook_uuid:   str

        :param client_id:       Client ID
        :type  client_id:       int

        :return:    JSON response from platform
        :rtype:     dict
        """

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

    def _get_playbook_page_info(self, url, page_size):

        """
        Get number of available pages for fetch.

        :param url:         URL of endpoint
        :type  url:         str

        :param page_size:   page size
        :type  page_size:   int

        :return:    Total number of available pages
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
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
