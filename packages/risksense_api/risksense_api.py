""" *******************************************************************************************************************
|
|  Name        :  risksense_api.py
|  Description :  Simplify interaction with the RiskSense API
|  Project     :  risksense_api
|  Copyright   :  2020 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

from .__version__ import __version__
from ._profile import *
from ._api_request_handler import *

from .__subject.__application_findings import ApplicationFindings
from .__subject.__application_unique_findings import ApplicationUniqueFindings
from .__subject.__applications import Applications
from .__subject.__application_urls import ApplicationUrls
from .__subject.__assessments import Assessments
from .__subject.__attachments import Attachments
from .__subject.__clients import Clients
from .__subject.__connectors import Connectors
from .__subject.__exports import Exports
from .__subject.__filters import Filters
from .__subject.__groups import Groups
from .__subject.__host_findings import HostFindings
from .__subject.__host_unique_findings import HostUniqueFindings
from .__subject.__hosts import Hosts
from .__subject.__networks import Networks
from .__subject.__playbooks import Playbooks
from .__subject.__rosa import Rosa
from .__subject.__tags import Tags
from .__subject.__uploads import Uploads
from .__subject.__users import Users


class RiskSenseApi:

    """ RiskSense API """

    def __init__(self, platform_url, api_key, **kwargs):

        """
        Initialize RiskSenseApi

        :param platform_url:    Platform URL
        :type  platform_url:    str

        :param api_key:         API Key
        :type  api_key:         str

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        self.__profile_name = "RiskSenseApi_v{}".format(__version__)
        self.__platform_url = platform_url
        self.__api_key = api_key

        try:
            self.__profile = Profile(self.__platform_url, self.__api_key, use_prog_bar=kwargs.get("use_prog_bar", False))
        except ValueError:
            raise

        #  Instantiate all subject classes
        self._instantiate_subjects()

        #  Fetch your user's clients and add them all to a list
        try:
            client_search_response = self.clients.get_clients(page_size=1000)
            self.my_clients = client_search_response['_embedded']['clients']
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
            raise

        #  If user is single-client, automatically set the default client ID
        if len(self.my_clients) == 1:
            self.set_default_client_id(self.my_clients[0]['id'])

    def set_default_client_id(self, client_id):

        """
        Set a default client ID.

        :param client_id:   Client ID
        :type  client_id:   int

        :raises ValueError:
        """

        if not isinstance(client_id, int):
            raise ValueError("Client ID MUST be an integer.")

        self.__profile.default_client_id = client_id

    def get_default_client_id(self):
        return self.__profile.default_client_id

    def refresh_my_clients(self):

        """
        Refresh my client list.  Re-queries the platform for a list of clients
        and re-stores those found to self.my_clients

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        try:
            client_search_response = self.clients.get_clients(page_size=1000)
            self.my_clients = client_search_response['_embedded']['clients']
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

    def update_num_threads(self, new_thread_num):

        """
        Update the number of threads to be used

        :param new_thread_num:  New number of threads
        :type  new_thread_num:  int

        :raises ValueError
        """

        try:
            self.__profile.update_num_threads(new_thread_num)
        except ValueError:
            raise

        #  Re-instantiate all subject classes
        self._instantiate_subjects()

    def _instantiate_subjects(self):

        """
        Instantiates all subjects
        """

        self.application_findings = ApplicationFindings(self.__profile)
        self.application_unique_findings = ApplicationUniqueFindings(self.__profile)
        self.applications = Applications(self.__profile)
        self.application_url = ApplicationUrls(self.__profile)
        self.assessments = Assessments(self.__profile)
        self.attachments = Attachments(self.__profile)
        self.clients = Clients(self.__profile)
        self.connectors = Connectors(self.__profile)
        self.exports = Exports(self.__profile)
        self.filters = Filters(self.__profile)
        self.groups = Groups(self.__profile)
        self.host_findings = HostFindings(self.__profile)
        self.host_unique_findings = HostUniqueFindings(self.__profile)
        self.hosts = Hosts(self.__profile)
        self.networks = Networks(self.__profile)
        self.playbooks = Playbooks(self.__profile)
        self.rosa = Rosa(self.__profile)
        self.tags = Tags(self.__profile)
        self.uploads = Uploads(self.__profile)
        self.users = Users(self.__profile)

    def __str__(self):
        return self.__profile_name


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
