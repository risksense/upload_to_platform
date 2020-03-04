""" *******************************************************************************************************************
|
|  Name        :  _search_filter.py
|  Description :  SearchFilter
|  Project     :  risksense_api
|  Copyright   :  2020 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """


class SearchFilter:
    """ SearchFilter class """

    class Operator:
        """ Operator Class """

        EXACT = "EXACT"
        IN = "IN"
        LIKE = "LIKE"
        WILDCARD = "WILDCARD"
        RANGE = "RANGE"
        GREATER = "GREATER"
        LESSER = "LESSER"
        CIDR = "CIDR"

    class Parameter:
        """ Parameter Class """

        def __init__(self, field_name, operator, value, exclusive=False):
            """
            Initialize Parameter

            :param field_name:  Field Name
            :type  field_name:  str

            :param operator:    Operator
            :type  operator:    str

            :param value:       Value
            :type  value:       various

            :param exclusive:   Exclude matching results?
            :type  exclusive:   bool
            """

            self.field_name = field_name
            self.operator = operator
            self.exclusive = exclusive
            self.value = value

    def __init__(self):
        """ Initialize SearchFilter class """
        self.parameters = []

    def __repr__(self):
        return repr(self.parameters)

    def add_parameter(self, parameter):

        """
        Add a parameter to the search filter list.

        :param parameter:   Parameter
        :type parameter:    Parameter
        """

        self.parameters.append(parameter.__dict__)

    def pop_parameter(self, index=0):

        """
        Pop a parameter from the search filter list.

        :param index:   Index of parameter to pop
        :type index:    int
        """

        self.parameters.pop(index=index)


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
