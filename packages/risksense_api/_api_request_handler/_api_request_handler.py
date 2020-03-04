""" *******************************************************************************************************************
|
|  Name         :  _api_request_handler.py
|  Module       :  api_request_handler
|  Description  :  RiskSense API Request Handler
|  Copyright    :  (c) RiskSense, Inc.
|  License      :  Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from ..__version__ import __version__
from ._exceptions import *


USER_AGENT = "risksense_api/" + __version__


class ApiRequestHandler:

    """ API Request Handler for the RiskSense Platform """

    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"

    def __init__(self, api_key, user_agent=USER_AGENT, max_retries=5):

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

        if user_agent is None:
            self.user_agent = 'rs_api_request_handler'
        else:
            self.user_agent = user_agent

        self.max_retries = max_retries

        self.__retry_session = self.__requests_retry_session()

        # Define some messaging
        self._unsuccessful_status_code_msg = "The request has failed, returning an unsuccessful status code ({})."
        self._max_retries_message = "Maximum number (" + str(self.max_retries) + ") of retries exceeded for:"
        self._generic_failure_message = "The request has failed:"

    def make_request(self, http_method, url, params=None, body=None, files=None):

        """
        Makes a request.

        :param http_method:     HTTP method to use for request (ApiRequestHandler.GET, ApiRequestHandler.POST,
                                                                ApiRequestHandler.PUT, ApiRequestHandler.DELETE)
        :type  http_method:     str

        :param url:             URL for API endpoint
        :type  url:             str

        :param params:          Parameters to be inserted into the URL
        :type  params:          dict

        :param body:            Body to be used in API request (if required)
        :type  body:            dict

        :param files:           Files to pass to API
        :type  files:           dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises PageSizeError:
        :raises ValueError:

        :return:    Request Response
        :rtype:     Response
        """

        header = {
            "User-Agent": self.user_agent,
            "x-api-key": self.api_key,
            "accept": "application/json"
        }

        if self._method_has_body(http_method):
            header.update({"content-type": "application/json"})

        #  If request is a GET...
        if http_method == ApiRequestHandler.GET:
            try:
                response = self._get(url, header=header, params=params)
            except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
                raise

        #  If request is a POST...
        elif http_method == ApiRequestHandler.POST:
            try:
                response = self._post(url, header=header, files=files, body=body)
            except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
                raise

        #  If request is a PUT...
        elif http_method == ApiRequestHandler.PUT:
            try:
                response = self._put(url, header=header, files=files, body=body)
            except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
                raise

        #  If request is a DELETE...
        elif http_method == ApiRequestHandler.DELETE:
            try:
                response = self._delete(url, header=header, body=body)
            except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
                raise

        else:
            raise ValueError(f"Unsupported HTTP method provided: {http_method}. Please provide a "
                             f"supported HTTP method (ApiRequestHandler.GET, ApiRequestHandler.POST, "
                             f"ApiRequestHandler.PUT, or ApiRequestHandler.DELETE)")

        return response

    def __requests_retry_session(self, backoff_factor=0.5, status_forcelist=(429, 502, 503)):

        """
        Create a Requests session that uses automatic retries.

        :param backoff_factor:      Backoff factor used to calculate time between retries.
        :type  backoff_factor:      float

        :param status_forcelist:    A tuple containing the response status codes that should trigger a retry.
        :type  status_forcelist:    tuple

        :return:    Requests Session
        :rtype:     Request
        """

        session = requests.Session()

        retry = Retry(
            total=self.max_retries,
            read=self.max_retries,
            connect=self.max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            method_whitelist=frozenset([ApiRequestHandler.GET, ApiRequestHandler.POST,
                                        ApiRequestHandler.PUT, ApiRequestHandler.DELETE])
        )

        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        return session

    def _request_and_validate(self, req_func, **func_params):

        """
        Send request and validate the response.

        :param req_func:        Request Function
        :type  req_func:        function

        :param func_params:     Function Parameters
        :type  func_params:     dict

        :return:    Response
        :rtype:     Response

        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises PageSizeError:
        :raises RequestFailed:
        """

        try:
            response = req_func(**func_params)
            try:
                self.__valid_response(response)
            except AssertionError:
                if self.__check_for_page_size_error(response):
                    raise PageSizeError("Maximum page size must be less than or equal to 1000.")
                error_message = self._get_status_code_error(response)
                raise StatusCodeError(error_message)
        except requests.exceptions.RetryError:
            raise MaxRetryError(self._max_retries_message + " {}".format(func_params['url']))
        except Exception as ex:
            raise RequestFailed(self._generic_failure_message + " " + str(ex))

        return response

    def _get(self, url, header, params):

        """
        GET

        :param url:     Endpoint URL
        :type  url:     str

        :param header:  Header
        :type  header:  dict

        :param params:  Params
        :type  params:  dict

        :return:    Request Response
        :rtype:     Response

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        func_params = {'url': url, 'headers': header, 'params': params}

        try:
            response = self._request_and_validate(self.__retry_session.get, **func_params)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return response

    def _post(self, url, header, body, files):

        """
        POST

        :param url:     Endpoint URL
        :type  url:     str

        :param header:  Header
        :type  header:  dict

        :param body:    Body
        :type  body:    dict

        :param files:   Files
        :type  files:   dict

        :return:    Request Response
        :rtype:     Response

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        #  If there are files involved for uploading...
        if files is not None:
            header.pop('content-type', None)
            header.pop('accept', None)
            func_params = {'url': url, 'headers': header, 'files': files}
        #  If there aren't files involved for uploading, send a regular POST request.
        else:
            func_params = {'url': url, 'headers': header, 'json': body}

        try:
            response = self._request_and_validate(self.__retry_session.post, **func_params)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return response

    def _put(self, url, header, body, files):

        """
        PUT

        :param url:     Endpoint URL
        :type  url:     str

        :param header:  Header
        :type  header:  dict

        :param body:    Body
        :type  body:    dict

        :param files:   Files
        :type  files:   dict

        :return:    Request Response
        :rtype:     Response

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        #  If there are files involved for uploading...
        if files is not None:
            header.pop('content-type', None)
            header.pop('accept', None)
            func_params = {'url': url, 'headers': header, 'files': files}
        #  If there aren't files involved for uploading, send a regular PUT request.
        else:
            func_params = {'url': url, 'headers': header, 'json': body}

        try:
            response = self._request_and_validate(self.__retry_session.put, **func_params)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return response

    def _delete(self, url, header, body):

        """
        DELETE

        :param url:     Endpoint URL
        :type  url:     str

        :param header:  Header
        :type  header:  dict

        :param body:    Body
        :type  body:    dict

        :return:    Request Response
        :rtype:     Response

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        func_params = {'url': url, 'headers': header, 'json': body}

        try:
            response = self._request_and_validate(self.__retry_session.delete, **func_params)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return response

    @staticmethod
    def __valid_response(response_to_validate):

        """
        Check to see if API response contains a success code.

        :param response_to_validate:    Response object from Requests Module
        :type  response_to_validate:    Requests Response Object
        """

        assert 200 <= response_to_validate.status_code <= 299

    @staticmethod
    def __check_for_page_size_error(response):

        """

        :param response:
        :type  response:

        :return:
        """

        page_size_error = False

        page_size_error_message = "must be less than or equal to 1000"

        if response.status_code == 400 and page_size_error_message in response.text:
            page_size_error = True

        return page_size_error

    @staticmethod
    def _get_status_code_error(response):

        """
        Build some messaging for an unsuccessful status code.

        :param response:   Response object from Requests Module
        :type  response:   Requests Response Object
        """

        exception_string = "The status code returned did not indicate success.\n"
        exception_string += "Response Status Code: {}\n".format(response.status_code)
        if response.text:
            exception_string += "Response Text: {}\n".format(response.text)

        return exception_string


    @staticmethod
    def _method_has_body(method):

        """
        Determine whether the HTTP method has a body.

        :param method:      The HTTP method
        :type  method:      str

        :return: Whether the method has a body
        :rtype: bool
        """

        return method.upper() not in ['GET', 'OPTIONS', 'HEAD', 'TRACE', 'DELETE']


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