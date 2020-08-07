""" *******************************************************************************************************************
|
|  Name        :  __tags.py
|  Module      :  risksense_api
|  Description :  A class to be used for searching for and updating tags on the RiskSense Platform.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

import json
from ..__exports import ExportFileType
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *


class TagType:
    """ TagType class and attributes"""

    COMPLIANCE = 'COMPLIANCE'
    LOCATION = 'LOCATION'
    CUSTOM = 'CUSTOM'
    REMEDIATION = 'REMEDIATION'
    PEOPLE = 'PEOPLE'
    PROJECT = 'PROJECT'
    SCANNER = 'SCANNER'
    CMDB = 'CMDB'


class Tags(Subject):

    """ Tags class """

    def __init__(self, profile):

        """
        Initialization of Tags object.

        :param profile:     Profile Object
        :type  profile:     _profile
        """

        self.subject_name = "tag"
        Subject.__init__(self, profile, self.subject_name)

    def create(self, tag_type, name, desc, owner, color="#648d9f", locked=False, propagate=True, client_id=None):

        """
        Create a new tag for the client.

        :param tag_type:    Type of tag to be created. (TagType.COMPLIANCE,
                                                        TagType.LOCATION,
                                                        TagType.CUSTOM,
                                                        TagType.REMEDIATION,
                                                        TagType.PEOPLE,
                                                        TagType.PROJECT,
                                                        TagType.SCANNER,
                                                        TagType.CMDB)
        :type  tag_type:    TagType attribute

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param propagate    Propagate tag to all findings?
        :type  propagate:   bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        list_of_tag_types = [
            TagType.COMPLIANCE,
            TagType.LOCATION,
            TagType.CUSTOM,
            TagType.REMEDIATION,
            TagType.PEOPLE,
            TagType.PROJECT,
            TagType.SCANNER,
            TagType.CMDB
        ]

        tag_type = tag_type.upper()
        if tag_type not in list_of_tag_types:
            raise ValueError(f"Tag Type provided ({tag_type}) is not supported.")

        url = self.api_base_url.format(str(client_id))

        body = {
            "fields": [
                {
                    "uid": "TAG_TYPE",
                    "value": tag_type
                },
                {
                    "uid": "NAME",
                    "value": name
                },
                {
                    "uid": "DESCRIPTION",
                    "value": desc
                },
                {
                    "uid": "OWNER",
                    "value": owner
                },
                {
                    "uid": "COLOR",
                    "value": color
                },
                {
                    "uid": "LOCKED",
                    "value": locked
                },
                {
                    "uid": "PROPAGATE_TO_ALL_FINDINGS",
                    "value": propagate
                }
            ]
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        new_tag_id = jsonified_response['id']

        return new_tag_id

    def create_compliance_tag(self, name, desc, owner, color="#648d9f", locked=False, client_id=None):

        """
        Create a new COMPLIANCE tag.

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            tag_id = self.create(TagType.COMPLIANCE, name, desc, owner, color, locked, client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError, ValueError):
            raise
        return tag_id

    def create_location_tag(self, name, desc, owner, color="#648d9f", locked=False, client_id=None):

        """
        Create a new LOCATION tag.

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            tag_id = self.create(TagType.LOCATION, name, desc, owner, color, locked, client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError, ValueError):
            raise
        return tag_id

    def create_custom_tag(self, name, desc, owner, color="#648d9f", locked=False, client_id=None):

        """
        Create a new CUSTOM tag.

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    Tag ID
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            tag_id = self.create(TagType.CUSTOM, name, desc, owner, color, locked, client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError, ValueError):
            raise
        return tag_id

    def create_remediation_tag(self, name, desc, owner, color="#648d9f", locked=False, client_id=None):

        """
        Create a new REMEDIATION tag.

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            tag_id = self.create(TagType.REMEDIATION, name, desc, owner, color, locked, client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError, ValueError):
            raise
        return tag_id

    def create_people_tag(self, name, desc, owner, color="#648d9f", locked=False, client_id=None):

        """
        Create a new PEOPLE tag.

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            tag_id = self.create(TagType.PEOPLE, name, desc, owner, color, locked, client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError, ValueError):
            raise
        return tag_id

    def create_project_tag(self, name, desc, owner, color="#648d9f", locked=False, client_id=None):

        """
        Create a new PROJECT tag.

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            tag_id = self.create(TagType.PROJECT, name, desc, owner, color, locked, client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError, ValueError):
            raise
        return tag_id

    def create_scanner_tag(self, name, desc, owner, color="#648d9f", locked=False, client_id=None):

        """
        Create a new SCANNER tag.

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            tag_id = self.create(TagType.SCANNER, name, desc, owner, color, locked, client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError, ValueError):
            raise
        return tag_id

    def create_cmdb_tag(self, name, desc, owner, color="#648d9f", locked=False, client_id=None):

        """
        Create a new CMDB tag.

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            tag_id = self.create(TagType.CMDB, name, desc, owner, color, locked, client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError, ValueError):
            raise
        return tag_id

    def update(self, tag_id, tag_type, name, desc, owner, color, locked, propagate=True, client_id=None):

        """
        Update an existing tag.

        :param tag_id:      The tag ID to be updated.
        :type  tag_id:      int

        :param tag_type:    The type of tag.
        :type  tag_type:    str

        :param name:        The name of the tag.
        :type  name:        str

        :param desc:        A description for the tag.
        :type  desc:        str

        :param owner:       The owner(s) of the tag, represented by user IDs, delimited by commas.  Ex: "1234,567,890"
        :type  owner:       str

        :param color:       The color for the tag.  A hex value.
        :type  color:       str

        :param locked:      Whether or not the tag should be locked.
        :type  locked       bool

        :param propagate    Propagate tag to all findings?
        :type propagate:    bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The job ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        list_of_tag_types = [
            TagType.COMPLIANCE,
            TagType.LOCATION,
            TagType.CUSTOM,
            TagType.REMEDIATION,
            TagType.PEOPLE,
            TagType.PROJECT,
            TagType.SCANNER,
            TagType.CMDB
        ]

        if tag_type not in list_of_tag_types:
            raise ValueError("Invalid tag type")

        body = {
            "fields": [
                {
                    "uid": "TAG_TYPE",
                    "value": tag_type
                },
                {
                    "uid": "NAME",
                    "value": name
                },
                {
                    "uid": "DESCRIPTION",
                    "value": desc
                },
                {
                    "uid": "OWNER",
                    "value": owner
                },
                {
                    "uid": "COLOR",
                    "value": color
                },
                {
                    "uid": "LOCKED",
                    "value": locked
                },
                {
                    "uid": "PROPAGATE_TO_ALL_FINDINGS",
                    "value": propagate
                }
            ]
        }

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(tag_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        response_id = jsonified_response['id']

        return response_id

    def delete(self, tag_id, force_delete=True, client_id=None):

        """
        Delete a tag.

        :param tag_id:          Tag ID to delete.
        :type  tag_id:          int

        :param force_delete:    Indicates whether or not deletion should be forced.
        :type  force_delete:    bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:  Boolean reflecting the indication from the platform as to whether
                  or not the deletion was successful.

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        body = {
            "forceDeleteTicket": force_delete
        }

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(tag_id))

        try:
            self.request_handler.make_request(ApiRequestHandler.DELETE, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        success = True

        return success

    def get_history(self, tag_id, page_num, page_size, client_id=None):

        """
        Get the history for a tag.

        :param tag_id:      Tag ID
        :type  tag_id:      int

        :param page_num:    Page number to retrieve.
        :type  page_num:    int

        :param page_size:   Number of items to be returned per page
        :type  page_size:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    A paginated JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises PageSizeError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/history".format(str(tag_id))

        paginated_url = url + "?size=" + str(page_size) + "&page=" + str(page_num)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, paginated_url)
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_single_search_page(self, search_filters, projection=Projection.BASIC, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns tags based on the provided filter(s) and other parameters.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param page_num:        Page number of results to be returned.
        :type  page_num:        int

        :param page_size:       Number of results to be returned per page.
        :type  page_size:       int

        :param projection:      Projection to use for query.  Default is "basic"
        :type  projection:      Projection attribute

        :param sort_field:      Name of field to sort results on.
        :type  sort_field:      SortField attribute

        :param sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A paginated JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises PageSizeError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/search"

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


    def search(self, search_filters, projection=Projection.BASIC, page_size=150,
               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns tags based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param projection:      Projection to be used in API request.  "basic" or "detail"
        :type  projection:      Projection attribute

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      Name of field to sort results on.
        :type  sort_field:      SortField attribute

        :param sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC
        :type sort_dir:         SortDirection attribute

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

    def export(self, search_filters, file_name, file_type=ExportFileType.CSV, comment="", client_id=None):

        """
        Initiates an export job on the platform for tag(s) based on the
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

        :return:    The job ID from the platform is returned.
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

    def lock_tag(self, tag_id, client_id=None):

        """
        Lock an existing tag.

        :param tag_id:      The tag ID to be locked.
        :type  tag_id:      int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The tag ID
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(tag_id))

        body = {
            "fields": [
                {
                    'uid': 'LOCKED',
                    'value': True
                }
            ]
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        response_id = jsonified_response['id']

        return response_id

    def unlock_tag(self, tag_id, client_id=None):

        """
        Unlock an existing tag.

        :param tag_id:      The tag ID to be unlocked.
        :type  tag_id:      int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The tag ID
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(tag_id))

        body = {
            "fields": [
                {
                    'uid': 'LOCKED',
                    'value': False
                }
            ]
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        response_id = jsonified_response['id']

        return response_id

    def get_model(self, client_id=None):

        """
        Get available projections and models for Tags.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Tags projections and models are returned.
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
