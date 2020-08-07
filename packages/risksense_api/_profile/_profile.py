""" *******************************************************************************************************************
|
|  Name        :  _profile.py
|  Module      :  risksense_api
|  Description :  A class for the creation of a user profile for interacting with the RiskSense Platform via the API.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0
|
******************************************************************************************************************* """


class Profile:

    """ Profile class """

    def __init__(self, platform_url, api_key, num_thread_workers=10, **kwargs):

        """
        Initialization of Platform object.  If any attributes are set to empty strings, ValueError is raised.

        :param platform_url:            URL of the platform
        :type  platform_url:            str

        :param api_key:                 API Key to be used to communicate with the platform
        :type  api_key:                 str

        :param num_thread_workers:     Number of thread workers for threaded functions
        :type  num_thread_workers:     int

        :raises:    ValueError
        """

        self.platform_url = platform_url.rstrip('/')
        self.api_key = api_key
        self.default_client_id = None

        self.num_thread_workers = num_thread_workers
        self.use_prog_bar = kwargs.get("use_prog_bar", False)

        self.proxy = None

        if self.platform_url == '':
            raise ValueError("No platform URL provided.")

        if self.api_key == '':
            raise ValueError("No API key provided.")

    def update_num_threads(self, new_thread_num):

        """
        Update the number of threads to be used

        :param new_thread_num:  New number of threads
        :type  new_thread_num:  int

        :raises ValueError
        """
        if 1 > new_thread_num > 15:
            raise ValueError("Number of threads should be between 1 and 15.")
        self.num_thread_workers = new_thread_num

    def add_proxy(self, proxy):

        """
        Add proxy to profile.

        :param proxy:   Proxy settings
        :type  proxy:   dict
        """

        self.proxy = proxy

    def remove_proxy(self):

        """
        Remove proxy from profile.
        """

        self.proxy = None


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
