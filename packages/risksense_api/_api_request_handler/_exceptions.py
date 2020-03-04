""" *******************************************************************************************************************
|
|  Name        :  _exceptions.py
|  Description :  Api Request Handler Exceptions
|  Project     :  risksense_api
|  Copyright   :  2019 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """



class RequestFailed(Exception):
    """ Custom Exception class for failed requests"""


class StatusCodeError(RequestFailed):
    """ Extension of RequestFailed class for Request Status Code errors"""


class MaxRetryError(RequestFailed):
    """ Extension of RequestFailed class for Maximum Retry errors"""



class PageSizeError(RequestFailed):
    """ Extension of RequestFailed class for Maximum Page Size errors"""



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
