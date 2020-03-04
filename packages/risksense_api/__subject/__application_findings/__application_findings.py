""" *******************************************************************************************************************
|
|  Name        :  __application_findings.py
|  Module      :  risksense_api
|  Description :  A class to be used for searching for and updating Application Findings on the RiskSense Platform.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
import datetime
from ..__exports import ExportFileType
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *


class ApplicationFindings(Subject):

    """ ApplicationFindings Class """

    def __init__(self, profile):

        """
        Initialization of ApplicationFindings object.

        :param profile:     Profile Object
        :type  profile:     _profile
        """

        Subject.__init__(self, profile, Subject.APPLICATION_FINDING)

    def get_single_search_page(self, search_filters, projection=Projection.BASIC, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns application findings based on the provided filter(s) and other parameters.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param projection:      The projection to use for API call.  Projection.BASIC or Projection.DETAIL
        :type  projection:      Projection attribute

        :param page_num:        Page number of results to be returned.
        :type  page_num:        int

        :param page_size:       Number of results to be returned per page.
        :type  page_size:       int

        :param sort_field:      Name of field to sort results on.
        :type  sort_field:      SortField attribute

        :param sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC.
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The paginated JSON response from the platform is returned.
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
            response = self._get_single_search_page(Subject.APPLICATION_FINDING, **func_args)
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
            raise

        return response

    def search(self, search_filters, projection=Projection.BASIC, page_size=150,
               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns application findings based on the provided filter(s) and other parameters.
        Rather than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param projection:      Projection to be used in API request.  Projection.BASIC or Projection.DETAIL
        :type  projection:      Projection attribute

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      The field to be used for sorting results returned.
        :type  sort_field:      SortField attribute

        :param sort_dir:        The direction of sorting to be used. SortDirection.ASC or SortDirection.DESC
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A list containing all application findings returned by the search using the filter provided.
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
            page_info = self._get_page_info(Subject.APPLICATION_FINDING, search_filters,
                                            page_size=page_size, client_id=client_id)
            num_pages = page_info[1]
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
            raise

        page_range = range(0, num_pages)

        try:
            all_results = self._search(Subject.APPLICATION_FINDING, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
            raise

        return all_results

    def get_count(self, search_filters, client_id=None):

        """
        Gets a count of application findings identified using the provided filter(s).

        :param client_id:       Client ID
        :type  client_id:       int

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The number of application findings identified is returned.

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            page_info = self._get_page_info(Subject.APPLICATION_FINDING, search_filters, client_id=client_id)
            count = page_info[0]
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return count

    def add_tag(self, search_filters, tag_id, client_id=None):

        """
        Add a tag to application findings.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param tag_id:          The tag ID to apply.
        :type  tag_id:          int

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

        try:
            job_id = self._tag(search_filters, tag_id, client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return job_id

    def remove_tag(self, search_filters, tag_id, client_id=None):

        """
        Remove a tag to application findings.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param tag_id:          The tag ID to remove.
        :type  tag_id:          int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID in the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            job_id = self._tag(search_filters, tag_id, client_id, is_remove=True)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return job_id

    def assign(self, search_filters, user_ids, client_id=None):

        """
        Assign user(s) to application findings.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param user_ids:        A list of user IDs.
        :type  user_ids:        list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID in the platform is returned.
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
        Assign user(s) from application findings.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param user_ids:        A list of user IDs.
        :type  user_ids:        list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID in the platform is returned.
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

    def export(self, search_filters, file_name, file_type=ExportFileType.CSV, comment="", client_id=None):

        """
        Initiates an export job on the platform for application finding(s) based on the
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

        :return:    The job ID in the platform from is returned.
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
            export_id = self._export(Subject.APPLICATION_FINDING, **func_args)
        except (RequestFailed, StatusCodeError, MaxRetryError, ValueError):
            raise

        return export_id

    def update_due_date(self, search_filters, due_date, client_id=None):

        """
        Update the due date for remediation of an application finding.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param due_date:        The due date to assign.  Must be in "YYYY-MM-DD" format.
        :type  due_date:        str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID in the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update-due-date"

        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "dueDate": due_date
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def add_note(self, search_filters, note, client_id=None):

        """
        Add a note to application finding(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param note:            A note to assign to the application findings.
        :type  note:            str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID in the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/note"

        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "note": note
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def request_acceptance(self, filter_request, description, reason, compensating_controls,
                           expiration_date=None, attachment=None, client_id=None):

        """
        Request acceptance for applicationFindings as defined in the filter_request parameter.

        :param filter_request:          A list of dictionaries containing filter parameters.
        :type  filter_request:          list

        :param description:             A description of the request.
        :type  description:             str

        :param reason:                  A reason for the request.
        :type  reason:                  str

        :param compensating_controls:   A description of compensating controls applied to this finding.
        :type  compensating_controls:   str

        :param expiration_date:         An expiration date.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:         str

        :param attachment:              A path to a file to be uploaded and attached to the request.
        :type  attachment:              str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    The job ID within the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/acceptance/request"

        body = {
            "filterRequest": filter_request,
            "description": description,
            "reason": reason,
            "compensatingControls": compensating_controls,
            "files": attachment,
            "expirationDate": expiration_date
        }

        body = self._strip_nones_from_dict(body)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def request_false_positive(self, filter_request, description, reason, compensating_controls=None,
                               expiration_date=None, attachment=None, client_id=None):

        """
        Request false positive for applicationFindings as defined in the filter_request parameter.

        :param filter_request:          A list of dictionaries containing filter parameters.
        :type  filter_request:          list

        :param description:             A description of the request.
        :type  description:             str

        :param reason:                  A reason for the request.
        :type  reason:                  str

        :param compensating_controls:   A description of compensating controls applied to this finding.
        :type  compensating_controls:   str

        :param expiration_date:         An expiration date.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:         str

        :param attachment:              A path to a file to be uploaded and attached to the request.
        :type  attachment:              str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    The job ID within the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/falsePositive/request"

        body = {
            "filterRequest": filter_request,
            "description": description,
            "reason": reason,
            "files": attachment,
            "compensatingControls": compensating_controls,
            "expirationDate": expiration_date
        }

        body = self._strip_nones_from_dict(body)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def request_remediation(self, filter_request, description, reason, compensating_controls=None,
                            expiration_date=None, attachment=None, client_id=None):

        """
        Request remediation for applicationFindings as defined in the filter_request parameter.

        :param filter_request:          A list of dictionaries containing filter parameters.
        :type  filter_request:          list

        :param description:             A description of the request.
        :type  description:             str

        :param reason:                  A reason for the request.
        :type  reason:                  str

        :param compensating_controls:   A description of compensating controls applied to this finding.
        :type  compensating_controls:   str

        :param expiration_date:         An expiration date.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:         str

        :param attachment:              A path to a file to be uploaded and attached to the request.
        :type  attachment:              str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    The job ID within the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/remediation/request"

        body = {
            "filterRequest": filter_request,
            "description": description,
            "reason": reason,
            "files": attachment,
            "compensatingControls": compensating_controls,
            "expirationDate": expiration_date
        }

        body = self._strip_nones_from_dict(body)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def request_severity_change(self, filter_request, description, reason, severity, compensating_controls=None,
                                expiration_date=None, attachment=None, client_id=None):

        """
        Request remediation for applicationFindings as defined in the filter_request parameter.

        :param filter_request:          A list of dictionaries containing filter parameters.
        :type  filter_request:          list

        :param description:             A description of the request.
        :type  description:             str

        :param reason:                  A reason for the request.
        :type  reason:                  str

        :param severity:                The new severity for the host finding(s)
        :type  severity:                str

        :param compensating_controls:   A description of compensating controls applied to this finding.
        :type  compensating_controls:   str

        :param expiration_date:         An expiration date.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:         str

        :param attachment:              A path to a file to be uploaded and attached to the request.
        :type  attachment:              str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    The job ID within the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/severityChange/request"

        body = {
            "filterRequest": filter_request,
            "description": description,
            "reason": reason,
            "severity": severity,
            "files": attachment,
            "compensatingControls": compensating_controls,
            "expirationDate": expiration_date
        }

        body = self._strip_nones_from_dict(body)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def reject_acceptance(self, filter_request, description, client_id=None):

        """
        Reject an acceptance request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rejection.
        :type  description:         str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/acceptance/reject"

        body = {
            "filterRequest": {
                "filters": filter_request,
                "projection": Projection.BASIC,
                "sort": [
                    {
                        "field": SortField.ID,
                        "direction": SortDirection.ASC
                    }
                ],
                "page": 0,
                "size": 20
            },
            "description": description
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def reject_false_positive(self, filter_request, description, client_id=None):

        """
        Reject a false positive request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rejection.
        :type  description:         str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/falsePositive/reject"

        body = {
            "filterRequest": {
                "filters": filter_request,
                "projection": Projection.BASIC,
                "sort": [
                    {
                        "field": SortField.ID,
                        "direction": SortDirection.ASC
                    }
                ],
                "page": 0,
                "size": 20
            },
            "description": description
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def reject_remediation(self, filter_request, description, client_id=None):

        """
        Reject a remediation request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rejection.
        :type  description:         str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/remediation/reject"

        body = {
            "filterRequest": {
                "filters": filter_request,
                "projection": Projection.BASIC,
                "sort": [
                    {
                        "field": SortField.ID,
                        "direction": SortDirection.ASC
                    }
                ],
                "page": 0,
                "size": 20
            },
            "description": description
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def reject_severity_change(self, filter_request, description, client_id=None):

        """
        Reject a severity change request.

        param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rejection.
        :type  description:         str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/severityChange/reject"

        body = {
            "filterRequest": {
                "filters": filter_request,
                "projection": Projection.BASIC,
                "sort": [
                    {
                        "field": SortField.ID,
                        "direction": SortDirection.ASC
                    }
                ],
                "page": 0,
                "size": 20
            },
            "description": description
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def rework_acceptance(self, filter_request, description, client_id=None):

        """
        Request a rework of an acceptance.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rework.
        :type  description:         str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/acceptance/rework"

        body = {
            "filterRequest": {
                "filters": filter_request,
                "projection": Projection.BASIC,
                "sort": [
                    {
                        "field": SortField.ID,
                        "direction": SortDirection.ASC
                    }
                ],
                "page": 0,
                "size": 20
            },
            "description": description
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def rework_false_positive(self, filter_request, description, client_id=None):

        """
        Request a rework of a false positive.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rework.
        :type  description:         str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/falsePositive/rework"

        body = {
            "filterRequest": {
                "filters": filter_request,
                "projection": Projection.BASIC,
                "sort": [
                    {
                        "field": SortField.ID,
                        "direction": SortDirection.ASC
                    }
                ],
                "page": 0,
                "size": 20
            },
            "description": description
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def rework_remediation(self, filter_request, description, client_id=None):

        """
        Request a rework of a remediation.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rework.
        :type  description:         str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/remediation/rework"

        body = {
            "filterRequest": {
                "filters": filter_request,
                "projection": Projection.BASIC,
                "sort": [
                    {
                        "field": SortField.ID,
                        "direction": SortDirection.ASC
                    }
                ],
                "page": 0,
                "size": 20
            },
            "description": description
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def rework_severity_change(self, filter_request, description, client_id=None):

        """
        Request a rework of a severity change.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rework.
        :type  description:         str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/severityChange/rework"

        body = {
            "filterRequest": {
                "filters": filter_request,
                "projection": Projection.BASIC,
                "sort": [
                    {
                        "field": SortField.ID,
                        "direction": SortDirection.ASC
                    }
                ],
                "page": 0,
                "size": 20
            },
            "description": description
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def approve_acceptance(self, filter_request, override_exp_date=False,
                           expiration_date=(datetime.date.today() + datetime.timedelta(days=14)), client_id=None):

        """
        Approve a acceptance request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param override_exp_date:   True/False indicating whether or not an expiration date should be overridden.
        :type  override_exp_date:   bool

        :param expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:     str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/acceptance/approve"

        body = {
            "filterRequest": {
                "filters": filter_request,
                "projection": Projection.BASIC,
                "sort": [
                    {
                        "field": SortField.ID,
                        "direction": SortDirection.ASC
                    }
                ],
                "page": 0,
                "size": 20
            },
            "expirationDate": expiration_date,
            "overrideExpDate": override_exp_date
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def approve_false_positive(self, filter_request, override_exp_date=False,
                               expiration_date=(datetime.date.today() + datetime.timedelta(days=14)), client_id=None):

        """
        Approve a false positive change request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param override_exp_date:   True/False indicating whether or not an expiration date should be overridden.
        :type  override_exp_date:   bool

        :param expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:     str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/falsePositive/approve"

        body = {
            "filterRequest": {
                "filters": filter_request,
                "projection": Projection.BASIC,
                "sort": [
                    {
                        "field": SortField.ID,
                        "direction": SortDirection.ASC
                    }
                ],
                "page": 0,
                "size": 20
            },
            "expirationDate": expiration_date,
            "overrideExpDate": override_exp_date
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def approve_remediation(self, filter_request, override_exp_date=False,
                            expiration_date=(datetime.date.today() + datetime.timedelta(days=14)), client_id=None):

        """
        Approve a remediation request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param override_exp_date:   True/False indicating whether or not an expiration date should be overridden.
        :type  override_exp_date:   bool

        :param expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:     str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/remediation/approve"

        body = {
            "filterRequest": {
                "filters": filter_request,
                "projection": Projection.BASIC,
                "sort": [
                    {
                        "field": SortField.ID,
                        "direction": SortDirection.ASC
                    }
                ],
                "page": 0,
                "size": 20
            },
            "expirationDate": expiration_date,
            "overrideExpDate": override_exp_date
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def approve_severity_change(self, filter_request, override_exp_date=False,
                                expiration_date=(datetime.date.today() + datetime.timedelta(days=14)), client_id=None):

        """
        Approve a severity change request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param override_exp_date:   True/False indicating whether or not an expiration date should be overridden.
        :type  override_exp_date:   bool

        :param expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:     str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/severityChange/approve"

        body = {
            "filterRequest": {
                "filters": filter_request,
                "projection": Projection.BASIC,
                "sort": [
                    {
                        "field": SortField.ID,
                        "direction": SortDirection.ASC
                    }
                ],
                "page": 0,
                "size": 20
            },
            "expirationDate": expiration_date,
            "overrideExpDate": override_exp_date
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def delete(self, search_filters, client_id=None):

        """
        Delete application findings based on filter(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

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
        job_id = jsonified_response['id']

        return job_id

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
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            fields_list = self._filter_fields(Subject.APPLICATION_FINDING, client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return fields_list

    def get_model(self, client_id=None):

        """
        Get available projections and models for Application Findings.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Application Finding projections and models are returned.
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._model(Subject.APPLICATION_FINDING, client_id)
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
            response = self._suggest(Subject.APPLICATION_FINDING, search_filter_1, search_filter_2, client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return response

    ##### BEGIN PRIVATE FUNCTIONS #####################################################

    def _tag(self, search_filters, tag_id, client_id, is_remove=False):

        """
        Add/Remove a tag to application findings.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param tag_id:          The tag ID to apply.
        :type  tag_id:          int

        :param client_id:       Client ID.
        :type  client_id:       int

        :param is_remove:       remove tag?
        :type  is_remove:       bool

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/tag"

        body = {
            "tagId": tag_id,
            "isRemove": is_remove,
            "filterRequest": {
                "filters": search_filters
            }
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id


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
