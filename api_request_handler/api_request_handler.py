"""
******************************************************************

Name        : api_request_handler.py
Module      : api_request_handler
Description : RiskSense API Request Handler
Copyright   : (c) RiskSense, Inc.
License     : Apache-2.0

******************************************************************
"""

import json
import time
import requests


class ApiRequestHandler:

    def __init__(self, api_key, user_agent=None, max_retries=5, retry_wait_time=1):

        """
        Initialize ApiRequestHandler

        :param api_key:             RiskSense Platform API key
        :type  api_key:             str

        :param user_agent:          User-Agent
        :type  user_agent:          str

        :param max_retries:         maximum number of retries for a request
        :type  max_retries:         int

        :param retry_wait_time:     Time to wait (in seconds) when 503 error encountered.
        :type  retry_wait_time:     int
        """

        self.api_key = api_key
        self.retry_counter = 0
        self.user_agent = user_agent
        self.max_retries = max_retries
        self.retry_wait_time = retry_wait_time

    def make_api_request(self, method, url, body=None, files=None, retry=False):

        """

        :param method:      HTTP method to use for request (GET or POST)
        :type  method:      str

        :param url:         URL for API endpoint
        :type  url:         str

        :param body:        Body to be used in API request (if required)
        :type  body:        dict

        :param files:       Files to pass to API
        :type  files:       dict

        :param retry:       Indicate whether this is a retry attempt
        :type  retry:       bool


        :return:    The requests module API response object if successfully sent.
                    A None is returned if max retries reached or invalid HTTP method provided.
        """

        if retry is True:
            self.increment_retry_counter()

        if self.retry_counter == self.max_retries:
            print(f"Max number of retries ({self.max_retries}) reached...")
            return None

        header = {
            "User-Agent": self.user_agent,
            "x-api-key": self.api_key,
            "content-type": "application/json"
        }

        if method.lower() == "get":

            response = requests.get(url, headers=header)

        elif method.lower() == "post":

            response = requests.post(url, headers=header, data=json.dumps(body), files=files)

        else:
            print(f"Unsupported method provided: {method}")
            print("Please provide a supported HTTP method (GET or POST)")
            return None

        if response and response.status_code == 503:

            time.sleep(self.retry_wait_time)
            print(f"503 error returned, retrying (this was attempt number {self.retry_counter + 1})...")
            new_response = self.make_api_request(method, url, body, files, retry=True)

            return new_response

        self.reset_retry_counter()

        return response

    def reset_retry_counter(self):

        self.retry_counter = 0

    def increment_retry_counter(self):

        self.retry_counter += 1
