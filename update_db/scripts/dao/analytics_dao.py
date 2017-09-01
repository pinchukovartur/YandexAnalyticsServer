from MySQLdb import *

""" Class to Create Connection Analytics DB and method of management"""


# ---------------------------------------------------------------------
# Program by Pinchukov Artur
#
# Version     Data      Info
#  1.0     11.08.2017
# ---------------------------------------------------------------------

class AnalyticsDB:
    """ The method init class and create connection with DB"""

    def __init__(self, user, password, host):
        self.connection = connect(user=user,
                                  passwd=password,
                                  host=host,
                                  db="analytics")
        self.connection.set_character_set('utf8')

    """ The method return list row with events"""

    def get_all_events(self):
        query = "SELECT * FROM analytics.events"
        self.connection.query(query)
        result = self.connection.store_result()
        list_row = list(result.fetch_row(result.num_rows()))
        return list_row

    def check_db_valid(self, date):
        if str(date) == "0000-00-00 00:00:00":
            return "0001-01-01 00:00:00"
        else:
            return date

    """ The method add event in DB"""

    def insert_events(self, event):
        query = "INSERT INTO analytics.events (android_id,app_package_name,app_version_name,appmetrica_device_id," \
                "city,connection_type,country_iso_code,device_locale,device_manufacturer,device_model,device_type," \
                "event_datetime,event_json,event_name,event_receive_datetime,event_receive_timestamp,event_timestamp," \
                "google_aid,ios_ifa,ios_ifv,mcc,mnc,operator_name,os_name,os_version) VALUES (%s, %s,%s, %s,%s, %s,%s," \
                " %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)"
        try:
            self.connection.cursor().execute(query, (
                event["android_id"], event["app_package_name"], event["app_version_name"],
                event["appmetrica_device_id"],
                event["city"], event["connection_type"], event["country_iso_code"], event["device_locale"],
                event["device_manufacturer"], event["device_model"], event["device_type"], self.check_db_valid(event["event_datetime"]),
                event["event_json"], event["event_name"], self.check_db_valid(event["event_receive_datetime"]),
                event["event_receive_timestamp"],
                event["event_timestamp"], event["google_aid"], event["ios_ifa"], event["ios_ifv"], event["mcc"],
                event["mnc"], event["operator_name"], event["os_name"], event["os_version"]))
            self.connection.commit()

        except MySQLError as error_str:
            print(error_str)
            print(event)
            f = open("err.txt", "a")
            f.write(str(error_str))
            f.close()
            self.connection.rollback()

    """ The method add error in DB"""

    def insert_error(self, error):
        query = "INSERT INTO analytics.errors (android_id,app_package_name,app_version_name,appmetrica_device_id," \
                "city,connection_type,country_iso_code,device_locale,device_manufacturer,device_model,device_type," \
                "error_datetime,error,error_id,error_receive_datetime,error_receive_timestamp,error_timestamp," \
                "google_aid,ios_ifa,ios_ifv,mcc,mnc,operator_name,os_name,os_version) VALUES (%s, %s,%s, %s,%s, %s,%s," \
                " %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)"
        try:
            self.connection.cursor().execute(query, (
                error["android_id"], error["app_package_name"], error["app_version_name"],
                error["appmetrica_device_id"],
                error["city"], error["connection_type"], error["country_iso_code"], error["device_locale"],
                error["device_manufacturer"], error["device_model"], error["device_type"], self.check_db_valid(error["error_datetime"]),
                error["error"], error["error_id"], self.check_db_valid(error["error_receive_datetime"]),
                error["error_receive_timestamp"],
                error["error_timestamp"], error["google_aid"], error["ios_ifa"], error["ios_ifv"], error["mcc"],
                error["mnc"], error["operator_name"], error["os_name"], error["os_version"]))

            self.connection.commit()

        except MySQLError as error_str:
            print(error_str)
            f = open("err.txt", "a")
            f.write(str(error_str))
            f.close()
            self.connection.rollback()

    """ The method add installations in DB"""

    def insert_installation(self, install):
        query = "INSERT INTO analytics.installations (" \
                "android_id,app_package_name,app_version_name,appmetrica_device_id, city,connection_type," \
                "country_iso_code,device_locale,device_manufacturer,device_model,device_type, match_type," \
                "is_reinstallation,install_receive_timestamp,install_timestamp,install_ipv6, install_datetime,install_receive_datetime," \
                "click_datetime,click_ipv6,click_id,click_user_agent,click_url_parameters,click_timestamp," \
                "google_aid,ios_ifa,ios_ifv,mcc,mnc,operator_name,os_name,os_version,tracking_id," \
                "tracker_name,publisher_name,publisher_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            self.connection.cursor().execute(query, (
                install["android_id"], install["app_package_name"], install["app_version_name"],
                install["appmetrica_device_id"], install["city"], install["connection_type"],
                install["country_iso_code"], install["device_locale"], install["device_manufacturer"],
                install["device_model"], install["device_type"], install["match_type"],
                install["is_reinstallation"], install["install_receive_timestamp"], install["install_timestamp"],
                install["install_ipv6"], self.check_db_valid(install["install_datetime"]), self.check_db_valid(install["install_receive_datetime"]),
                self.check_db_valid(install["click_datetime"]), install["click_ipv6"], install["click_id"],
                install["click_user_agent"], install["click_url_parameters"], install["click_timestamp"],
                install["google_aid"], install["ios_ifa"], install["ios_ifv"],
                install["mcc"], install["mnc"], install["operator_name"],
                install["os_name"], install["os_version"],
                install["tracking_id"], install["tracker_name"], install["publisher_name"],
                install["publisher_id"]))

            self.connection.commit()

        except MySQLError as error_str:
            print(error_str)
            f = open("err.txt", "a")
            f.write(str(error_str))
            f.close()
            self.connection.rollback()

    """ The method add crashes in DB"""

    def insert_crashes(self, crash):
        query = "INSERT INTO analytics.crashes (" \
                "android_id,app_package_name,app_version_name," \
                "appmetrica_device_id, city,connection_type," \
                "country_iso_code,crash,crash_datetime," \
                "crash_group_id,crash_id,crash_receive_datetime," \
                "crash_receive_timestamp,crash_timestamp,device_locale," \
                "device_manufacturer,device_model,device_type," \
                "google_aid,ios_ifa,ios_ifv," \
                "mcc,mnc,operator_name," \
                "os_name,os_version,windows_aid" \
                ") VALUES" \
                " (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            self.connection.cursor().execute(query, (
                crash["android_id"], crash["app_package_name"], crash["app_version_name"],
                crash["appmetrica_device_id"], crash["city"], crash["connection_type"],
                crash["country_iso_code"], crash["crash"], self.check_db_valid(crash["crash_datetime"]),
                crash["crash_group_id"], crash["crash_id"], self.check_db_valid(crash["crash_receive_datetime"]),
                crash["crash_receive_timestamp"], crash["crash_timestamp"], crash["device_locale"],
                crash["device_manufacturer"], crash["device_model"], crash["device_type"],
                crash["google_aid"], crash["ios_ifa"],
                crash["ios_ifv"], crash["mcc"], crash["mnc"],
                crash["operator_name"], crash["os_name"], crash["os_version"],
                crash["windows_aid"]))

            self.connection.commit()
        except MySQLError as error_str:
            print(error_str)
            f = open("err.txt", "a")
            f.write(str(error_str))
            f.close()
            self.connection.rollback()
    """ The method return max value datetime events"""

    def get_max_event_datetime(self):
        query = "SELECT max(events.event_datetime) FROM analytics.events;"
        self.connection.query(query)
        result = self.connection.store_result()
        data = list(result.fetch_row(result.num_rows()))[0][0]
        if data is not None:
            return str(data)
        else:
            return "2012-01-01 00:00:00"

    """ The method return max value datetime installations"""

    def get_max_installation_datetime(self):
        query = "SELECT max(installations.install_datetime) FROM analytics.installations;"
        self.connection.query(query)
        result = self.connection.store_result()
        data = list(result.fetch_row(result.num_rows()))[0][0]
        if data is not None:
            return str(data)
        else:
            return "2012-01-01 00:00:00"

    """ The method return max value datetime errors"""

    def get_max_errors_datetime(self):
        query = "SELECT max(errors.error_datetime) FROM analytics.errors;"
        self.connection.query(query)
        result = self.connection.store_result()
        data = list(result.fetch_row(result.num_rows()))[0][0]
        if data is not None:
            return str(data)
        else:
            return "2012-01-01 00:00:00"

    """ The method return max value datetime crashes"""

    def get_max_crashes_datetime(self):
        query = "SELECT max(crashes.crash_datetime) FROM analytics.crashes;"
        self.connection.query(query)
        result = self.connection.store_result()
        data = list(result.fetch_row(result.num_rows()))[0][0]
        if data is not None:
            return str(data)
        else:
            return "2012-01-01 00:00:00"
