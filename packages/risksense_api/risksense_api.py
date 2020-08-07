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

    def __init__(self, platform_url, api_key, proxy_host=None, proxy_port=3128,
                 proxy_user=None, proxy_password=None, **kwargs):

        """
        Initialize RiskSenseApi

        :param platform_url:    Platform URL
        :type  platform_url:    str

        :param api_key:         API Key
        :type  api_key:         str

        :param proxy_host:      Proxy host, if applicable
        :type  proxy_host:      str

        :param proxy_port:      Proxy port, if applicable
        :type  proxy_port:      int

        :param proxy_user:      Proxy username, if applicable
        :type  proxy_user:      str

        :param proxy_password:  Proxy password, if applicable
        :param proxy_password:  str

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        self.__profile_name = "RiskSenseApi_v{}".format(__version__)
        self.__platform_url = platform_url
        self.__api_key = api_key

        # Proxy settings, if applicable
        self.__proxy_host = proxy_host
        self.__proxy_port = proxy_port
        self.__proxy_user = proxy_user
        self.__proxy_password = proxy_password

        self.__use_prog_bar = kwargs.get("use_prog_bar", False)

        try:
            self.__profile = Profile(self.__platform_url, self.__api_key, use_prog_bar=self.__use_prog_bar)
        except ValueError:
            raise

        #  Instantiate all subject classes
        self._instantiate_subjects()

        # Set proxy, if applicable.
        if self.__proxy_host is not None:
            # The user must want to use a proxy...
            if type(self.__proxy_port) != int:
                raise ValueError("Proxy port must be an integer.")

            try:
                if self.__proxy_user is None:
                    self.set_proxy(self.__proxy_host, self.__proxy_port)
                else:
                    self.set_proxy(self.__proxy_host, self.__proxy_port, True, self.__proxy_user, self.__proxy_password)
            except ValueError:
                raise

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

        # If submitted client_id is not an integer, raise an exception
        if not isinstance(client_id, int):
            raise ValueError("Client ID MUST be an integer.")

        self.__profile.default_client_id = client_id

    def get_default_client_id(self):
        """
        Get the current default client ID

        :return:    Default Client ID
        :rtype:     int
        """
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
        Update the number of threads to be used in multithreaded operations

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
        
        self.available_subjects = {
            "Application Findings": self.application_findings,
            "Application Unique Findings": self.application_unique_findings,
            "Applications": self.applications,
            "Application URL": self.application_url,
            "Assessments": self.assessments,
            "Attachments": self.attachments,
            "Clients": self.clients,
            "Connectors": self.connectors,
            "Exports": self.exports,
            "Filters": self.filters,
            "Groups": self.groups,
            "Host Findings": self.host_findings,
            "Host Unique Findings": self.host_unique_findings,
            "Hosts": self.hosts,
            "Networks": self.networks,
            "Playbooks": self.playbooks,
            "ROSA": self.rosa,
            "Tags": self.tags,
            "Uploads": self.uploads,
            "Users": self.users
        }

    def set_proxy(self, proxy_host, proxy_port, auth=False, user=None, password=None):

        """
        Set an https proxy for requests. No current support for SOCKS.

        :param proxy_host:      Proxy host (IP address or hostname)
        :type  proxy_host:      str

        :param proxy_port:      Proxy port
        :type  proxy_port:      int

        :param auth:            Use proxy authorization?
        :type  auth:            bool

        :param user:            Proxy username
        :type  user:            str

        :param password:        Proxy password
        :type  password:        str

        :raises ValueError:
        """

        if proxy_host == "":
            raise ValueError("No proxy host provided.")

        if auth is True:
            if user is None:
                raise ValueError("Error adding proxy.  Auth is set to true, but user provided.")
            if password is None:
                raise ValueError("Error adding proxy.  Auth is set to true, but no password provided.")

            auth_pair = "{}:{}".format(user, password)

            proxy = {
                'https': 'https://{}@{}:{}'.format(auth_pair, proxy_host, str(proxy_port))
            }

        else:
            proxy = {
                'https': 'https://{}:{}'.format(proxy_host, str(proxy_port))
            }

        self.__profile.add_proxy(proxy)
        self._instantiate_subjects()

    def remove_proxy(self):

        """
        Remove any set proxy
        """
        self.__profile.remove_proxy()
        self._instantiate_subjects()

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
