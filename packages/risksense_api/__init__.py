""" *******************************************************************************************************************
|
|  Name        :  __init__.py
|  Module      :  risksense_api
|  Description :  A python module for interacting with the RiskSense API.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __copyright__, __author__, __author_email__
from .__version__ import __license__

from .__subject.__tags import TagType
from .__subject.__filters import FilterSubject
from .__subject.__exports import ExportFileType

from ._params import *
from ._search_filter import *

from .risksense_api import RiskSenseApi
from ._api_request_handler import *


__all__ = [
    'TagType',
    'FilterSubject',
    'ExportFileType',
    'Projection',
    'SortField',
    'SortDirection',
    'SearchFilter',
    'RiskSenseApi',
    'RequestFailed',
    'StatusCodeError',
    'MaxRetryError',
    'PageSizeError'
]


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
