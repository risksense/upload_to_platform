"""
*********************************************************************

Name        : api_request_handler.py
Module      : api_request_handler
Description : RiskSense API Request Handler
Copyright   : (c) RiskSense, Inc.
License     : Apache-2.0

*********************************************************************
"""

import json
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class ApiRequestHandler:

    def __init__(self, api_key, user_agent=None, max_retries=5):

        """
        Initialize ApiRequestHandler class.

        :param api_key:             RiskSense Platform API key
        :type  api_key:             str

        :param user_agent:          User-Agent
        :type  user_agent:          str

        :param max_retries:         maximum number of retries for a request
        :type  max_retries:         int
        """

        self.api_key = api_key
        self.user_agent = user_agent
        self.max_retries = max_retries

        self.__retry_counter = 0

    def make_request(self, http_method, url, body=None, files=None):

        """

        :param http_method:      HTTP method to use for request (GET or POST)
        :type  http_method:      str

        :param url:             URL for API endpoint
        :type  url:             str

        :param body:            Body to be used in API request (if required)
        :type  body:            dict

        :param files:           Files to pass to API
        :type  files:           dict

        :return:    The requests module API response object is returned if  request is successfully sent.
                    A None is returned invalid HTTP method provided.
                    If max retries are reached, an exception is raised.
        """

        header = {
            "User-Agent": self.user_agent,
            "x-api-key": self.api_key,
            "content-type": "application/json"
        }

        #  If request is a GET...
        if http_method.lower() == "get":
            try:
                response = self.__requests_retry_session().get(url, headers=header)
            except requests.exceptions.RequestException:
                raise
            except Exception:
                raise

        #  If request is a POST...
        elif http_method.lower() == "post":

            #  If there are files involved for uploading...
            if files is not None:
                header.pop('content-type', None)
                try:
                    response = self.__requests_retry_session().post(url, headers=header, files=files)
                except requests.exceptions.RequestException:
                    raise
                except Exception:
                    raise

            #  If there aren't files involved for uploading, send a regular post request.
            else:
                try:
                    response = self.__requests_retry_session().post(url, headers=header, data=json.dumps(body))
                except requests.exceptions.RequestException:
                    raise
                except Exception:
                    raise

        #  If request is not a GET or a POST, exit and ask for a supported http method
        else:
            print(f"Unsupported HTTP method provided: {http_method}")
            print("Please provide a supported HTTP method (GET or POST)")
            exit(1)

        return response

    def __requests_retry_session(self, backoff_factor=0.5, status_forcelist=(429, 502, 503), session=None):
        session = session or requests.Session()
        retry = Retry(
            total=self.max_retries,
            read=self.max_retries,
            connect=self.max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    @staticmethod
    def valid_response(response, success_code):

        """
        Check to see if API response is valid, and has contains the proper success code.

        :param response:        Response object from Requests Module
        :type  response:        object

        :param success_code:    Expected success status code
        :type  success_code:    int

        :return:    True/False indicating whether or not response is valid.
        :rtype:     bool
        """

        if response is not None and response.status_code == success_code:
            return True

        else:
            return False
