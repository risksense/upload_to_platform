""" *******************************************************************************************************************
|
|  Name        : __connectors.py
|  Module      : risksense_api
|  Description : A class to be used for interacting with connectors on the RiskSense Platform.
|  Copyright   : (c) RiskSense, Inc.
|  License     : Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

import json
from ...__subject import Subject
from ..._api_request_handler import *


class Connectors(Subject):

    """ Connectors class """

    class Type:
        """ Connectors.Type class """
        NESSUS = 'NESSUS'
        QUALYS_VULN = 'QUALYS_VULNERABILITY'
        QUALYS_ASSET = 'QUALYS_ASSET'
        NEXPOSE = 'NEXPOSE'
        TENEBLE_SEC_CENTER = 'TENEBLE_SECURITY_CENTER'

    class ScheduleFreq:
        """ Connectors.ScheduleFreq class """
        DAILY = "DAILY"
        WEEKLY = "WEEKLY"
        MONTHLY = "MONTHLY"

    def __init__(self, profile):

        """
        Initialization of Connectors object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """

        Subject.__init__(self, profile, Subject.CONNECTOR)

    def get_list(self, page_num=0, page_size=150, client_id=None):

        """
        Get a list of connectors associated with the client.

        :param page_num:    The page number of results to be returned.
        :type  page_num:    int

        :param page_size:   The number of results to return per page.
        :type  page_size:   int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises PageSizeError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "?size=" + str(page_size) + "&page=" + str(page_num)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def create(self, conn_name, conn_type, conn_url, schedule_freq, network_id,
               username_or_access_key, password_or_secret_key, auto_urba=True, client_id=None, **kwargs):

        """
        Create a new Nessus connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_type:       The connector type. (Valid options are: Connectors.Type.NESSUS, Connectors.Type.NEXPOSE,
                                                                        Connectors.Type.QUALYS_VULN, Connectors.Type.QUALYS_ASSET,
                                                                        Connectors.Type.TENEBLE_SEC_CENTER)
        :type  conn_type:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username_or_access_key:      The username to use for connector authentication.
        :type  username_or_access_key:      str

        :param password_or_secret_key:      The password to use for connector authentication.
        :type  password_or_secret_key:      str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        ssl_cert = kwargs.get('ssl_cert', None)
        hour_of_day = kwargs.get('hour_of_day', None)
        day_of_week = kwargs.get('day_of_week', None)
        day_of_month = kwargs.get('day_of_month', None)

        if conn_type == Connectors.Type.NESSUS:

            attributes = {
                "accessKey": username_or_access_key,
                "secretKey": password_or_secret_key
            }

        else:
            attributes = {
                "username": username_or_access_key,
                "password": password_or_secret_key
            }

        body = {
            "type": conn_type,
            "name": conn_name,
            "connection": {
                "url": conn_url
            },
            "networkId": network_id,
            "attributes": attributes,
            "autoUrba": auto_urba
        }

        if ssl_cert is not None:
            body['connection'].update(sslCertificates=ssl_cert)

        if schedule_freq == Connectors.ScheduleFreq.DAILY:

            if hour_of_day is None:
                hour_of_day = 12

            connector_schedule = {
                "type": schedule_freq,
                "hourOfDay": hour_of_day
            }

        elif schedule_freq == Connectors.ScheduleFreq.WEEKLY:

            if day_of_week is None:
                day_of_week = 1

            if hour_of_day is None:
                hour_of_day = 12

            connector_schedule = {
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "dayOfWeek": day_of_week
            }

        elif schedule_freq == Connectors.ScheduleFreq.MONTHLY:

            if day_of_month is None:
                day_of_month = 1

            if hour_of_day is None:
                hour_of_day = 12

            connector_schedule = {
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "dayOfMonth": day_of_month
            }

        else:
            raise ValueError("Schedule freq. should be DAILY, WEEKLY, or MONTHLY.")

        body.update(schedule=connector_schedule)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def create_nessus(self, conn_name, conn_url, schedule_freq, network_id,
                      access_key, secret_key, auto_urba=True, client_id=None, **kwargs):

        """
        Create a new Nessus connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param access_key:      The username to use for connector authentication.
        :type  access_key:      str

        :param secret_key:      The password to use for connector authentication.
        :type  secret_key:      str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create(conn_name, Connectors.Type.NESSUS, conn_url, schedule_freq, network_id,
                                       access_key, secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed, StatusCodeError, MaxRetryError, ValueError):
            raise

        return connector_id

    def create_qualys_vuln(self, conn_name, conn_url, schedule_freq, network_id,
                           username, password, auto_urba=True, client_id=None, **kwargs):

        """
        Create a new Qualys Vulnerability connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create(conn_name, Connectors.Type.QUALYS_VULN, conn_url, schedule_freq,
                                       network_id, username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed, StatusCodeError, MaxRetryError, ValueError):
            raise

        return connector_id

    def create_qualys_asset(self, conn_name, conn_url, schedule_freq, network_id,
                            username, password, auto_urba=True, client_id=None, **kwargs):

        """
        Create a new Qualys Asset connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create(conn_name, Connectors.Type.QUALYS_ASSET, conn_url, schedule_freq,
                                       network_id, username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed, StatusCodeError, MaxRetryError, ValueError):
            raise

        return connector_id

    def create_nexpose(self, conn_name, conn_url, schedule_freq, network_id,
                       username, password, auto_urba=True, client_id=None, **kwargs):

        """
        Create a new Nexpose connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create(conn_name, Connectors.Type.NEXPOSE, conn_url, schedule_freq, network_id,
                                       username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed, StatusCodeError, MaxRetryError, ValueError):
            raise

        return connector_id

    def create_teneble(self, conn_name, conn_url, schedule_freq, network_id,
                       username, password, auto_urba=True, client_id=None, **kwargs):

        """
        Create a new Teneble Security Center connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create(conn_name, Connectors.Type.TENEBLE_SEC_CENTER, conn_url, schedule_freq,
                                       network_id, username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed, StatusCodeError, MaxRetryError, ValueError):
            raise

        return connector_id

    def get_connector_detail(self, connector_id, client_id=None):

        """
        Get the details associated with a specific connector.

        :param connector_id:    The connector ID.
        :type  connector_id:    int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(connector_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def update(self, connector_id, conn_type, conn_name, conn_url, network_id, schedule_freq,
               username_or_access_key, password_or_secret_key, auto_urba=True, client_id=None, **kwargs):

        """
        Update an existing connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_type:               Type of Connector (Valid options are: Connectors.Type.NESSUS,
                                                                              Connectors.Type.NEXPOSE,
                                                                              Connectors.Type.QUALYS_VULN,
                                                                              Connectors.Type.QUALYS_ASSET,
                                                                              Connectors.Type.TENEBLE_SEC_CENTER)
        :type  conn_type:               str

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:   Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:   bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        connector_schedule = None

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(connector_id))

        hour_of_day = kwargs.get('hour_of_day', None)
        day_of_week = kwargs.get('day_of_week', None)
        day_of_month = kwargs.get('day_of_month', None)

        if schedule_freq == Connectors.ScheduleFreq.DAILY:

            if hour_of_day is None:
                hour_of_day = 12

            connector_schedule = {
                "type": schedule_freq,
                "hourOfDay": hour_of_day
            }

        elif schedule_freq == Connectors.ScheduleFreq.WEEKLY:

            if day_of_week is None:
                day_of_week = 1

            if hour_of_day is None:
                hour_of_day = 12

            connector_schedule = {
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "dayOfWeek": day_of_week
            }

        elif schedule_freq == Connectors.ScheduleFreq.MONTHLY:

            if day_of_month is None:
                day_of_month = 1

            if hour_of_day is None:
                hour_of_day = 12

            connector_schedule = {
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "dayOfMonth": day_of_month
            }

        if conn_type == Connectors.Type.NESSUS:
            attributes = {
                "accessKey": username_or_access_key,
                "secretKey": password_or_secret_key
            }

        else:
            attributes = {
                "username": username_or_access_key,
                "password": password_or_secret_key
            }

        body = {
            "type": conn_type,
            "name": conn_name,
            "connection": {
                "url": conn_url
            },
            "schedule": connector_schedule,
            "networkId": network_id,
            "attributes": attributes,
            "autoUrba": auto_urba
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        returned_id = jsonified_response['id']

        return returned_id

    def update_nessus_connector(self, connector_id, conn_name, conn_url, network_id, schedule_freq,
                                username_or_access_key, password_or_secret_key, auto_urba=True, client_id=None, **kwargs):

        """
        Update an existing Nessus connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:   Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:   bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.NESSUS, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return returned_id

    def update_qualys_vuln_connector(self, connector_id, conn_name, conn_url, network_id, schedule_freq,
                                     username_or_access_key, password_or_secret_key, auto_urba=True, client_id=None, **kwargs):

        """
        Update an existing QUALYS VULN connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:               Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:               bool

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.QUALYS_VULN, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return returned_id

    def update_qualys_asset_connector(self, connector_id, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba=True, client_id=None, **kwargs):

        """
        Update an existing QUALYS ASSET connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:               Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:               bool

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.QUALYS_ASSET, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return returned_id

    def update_nexpose_connector(self, connector_id, conn_name, conn_url, network_id, schedule_freq,
                                 username_or_access_key, password_or_secret_key, auto_urba=True, client_id=None, **kwargs):

        """
        Update an existing NEXPOSE connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:   Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:   bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.NEXPOSE, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return returned_id

    def update_teneble_connector(self, connector_id, conn_name, conn_url, network_id, schedule_freq,
                                 username_or_access_key, password_or_secret_key, auto_urba=True, client_id=None, **kwargs):

        """
        Update an existing TENEBLE SECURITY CENTER connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:               Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:               bool

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.TENEBLE_SEC_CENTER, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        return returned_id

    def delete(self, connector_id, delete_tag=True, client_id=None):

        """
        Delete a connector.

        :param connector_id:    The connector ID.
        :type  connector_id:    int

        :param delete_tag:      Force delete tag associated with connector?
        :type  delete_tag:      bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Indicator reflecting whether or not the operation was successful.
        :rtype:     bool

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(connector_id))

        body = {
            "deleteTag": delete_tag
        }

        try:
            self.request_handler.make_request(ApiRequestHandler.DELETE, url, body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        success = True

        return success

    def get_jobs(self, connector_id, page_num=0, page_size=150, client_id=None):

        """
        Get the jobs associated with a connector.

        :param connector_id:    The connector ID.
        :type  connector_id:    int

        :param page_num:        The page number of results to be returned.
        :type  page_num:        int

        :param page_size:       The number of results to return per page.
        :type page_size:        int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises PageSizeError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/job".format(str(connector_id))

        params = {'page': page_num, 'size': page_size}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def update_schedule(self, connector_id, schedule_freq, enabled, client_id=None, **kwargs):

        """
        Update the schedule of an existing Connector.

        :param connector_id:    Connector ID
        :type  connector_id:    int

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param enabled:         Enable connector?
        :type  enabled:         bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword hour_of_day:   The time the connector should run. Req. for DAILY, WEEKLY, and MONTHLY. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Req. for WEEKLY. Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Req. for MONTHLY. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        hour_of_day = kwargs.get('hour_of_day', None)
        day_of_week = kwargs.get('day_of_week', None)
        day_of_month = kwargs.get('day_of_month', None)

        url = self.api_base_url.format(str(client_id)) + "/{}/schedule".format(str(connector_id))

        body = {
            "type": schedule_freq,
            "enabled": enabled
        }

        if schedule_freq == Connectors.ScheduleFreq.DAILY:

            if hour_of_day is None:
                raise ValueError("hour_of_day is required for a DAILY connector schedule.")

            body.update(hourOfDay=hour_of_day)

        elif schedule_freq == Connectors.ScheduleFreq.WEEKLY:

            if day_of_week is None and hour_of_day is None:
                raise ValueError("hour_of_day and day_of_week are required for a WEEKLY connector schedule.")

            if day_of_week is None:
                raise ValueError("day_of_week is required for a WEEKLY connector schedule.")

            if hour_of_day is None:
                raise ValueError("hour_of_day is required for a WEEKLY connector schedule.")

            body.update(hourOfDay=hour_of_day)
            body.update(dayOfWeek=day_of_week)

        elif schedule_freq == Connectors.ScheduleFreq.MONTHLY:

            if day_of_month is None and hour_of_day is None:
                raise ValueError("day_of_month and day_of_week are required for a WEEKLY connector schedule.")

            if day_of_month is None:
                raise ValueError("day_of_month is required for a WEEKLY connector schedule.")

            if hour_of_day is None:
                raise ValueError("hour_of_day is required for a WEEKLY connector schedule.")

            body.update(hourOfDay=hour_of_day)
            body.update(dayOfMonth=day_of_month)

        else:
            raise ValueError("schedule_freq should be one of DAILY, WEEKLY, or MONTHLY")

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        returned_id = jsonified_response['id']

        return returned_id

    # Future: Add support for ticket connectors (SNOW, JIRA, etc.).


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
