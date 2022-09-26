#!/usr/bin/python3

import collections
import functools
import json
import logging
import os
import re
import urllib.parse
from collections import OrderedDict

import urllib3

from py_core.handlerLogger import logger
from py_core.libConfParser.parserJSON import ParserJSON
from py_core.libRequests.libRequest import HTTPRequest

urllib3.disable_warnings()


def get_odata_ids(data, key="Members"):
    rets = []
    d_items = data.get(key)
    if d_items:
        for d_item in d_items:
            for k, v in d_item.items():
                rets.append(v)
    return rets


class ParserCaseConf(collections.UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def case_id(self):
        if self.data:
            return self.data.get("caseID", None)

    @property
    def method(self):
        if self.data:
            return self.data.get("method", None)

    @property
    def uri(self):
        if self.data:
            return self.data.get("URI", None)

    def get_standard_list(self):
        if self.data:
            return self.data.get("standardList", None)

    def set_standard_list(self, std_list):
        if self.data:
            self.data["standardList"] = std_list

    standard_list = property(get_standard_list, set_standard_list)

    def get_exclude_list(self):
        if self.data:
            return self.data.get("excludeList", None)

    def set_exclude_list(self, data):
        if self.data:
            self.data["excludeList"] = data

    exclude_list = property(get_exclude_list, set_exclude_list)

    @property
    def resp_group(self):
        if self.data:
            return self.data.get("resp_group", None)

    def get_expected_sensor_count(self):
        if self.data:
            return self.data.get("expected_sensor_count", None)

    def set_expected_sensor_count(self, count):
        if self.data:
            self.data["expected_sensor_count"] = count

    expected_sensor_count = property(get_expected_sensor_count, set_expected_sensor_count)


class ParserSensor(collections.UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info(f"Sensor data: {json.dumps(self.data, indent=4)}")

    @property
    def odata_id(self):
        return self.data.get('@odata.id', None)

    @property
    def odata_type(self):
        return self.data.get('@odata.type', None)

    @property
    def id(self):
        return self.data.get('Id', None)

    @property
    def desc(self):
        return self.data.get('Description', None)

    @property
    def name(self):
        return self.data.get("Name", None)

    @property
    def member_id(self):
        return self.data.get('MemberId', None)

    @property
    def status(self):
        return self.data.get("Status", None)

    @property
    def health(self):
        return self.status.get('Health')

    @property
    def is_healthy(self):
        if re.findall("OK", self.health, re.I):
            return True


class ParserFirmware(ParserSensor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def version(self):
        return self.data.get('Version')


class ParserRedfishSEL(ParserSensor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def message_id(self):
        return self.data.get('MessageId')

    @property
    def created(self):
        return self.data.get('Created')


class ParserAuth(collections.UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # logger.info(f"Auth data: {json.dumps(self.data, indent=4)}")

    @property
    def username(self):
        return self.data.get('username')

    @property
    def password(self):
        return self.data.get('password')

    @property
    def bmc_ip(self):
        return self.data.get('BMCIP')


class MiBMCRedfishBase(object):
    test_result = OrderedDict()
    current_case = None
    test_passed = True
    obj_req = HTTPRequest(verify=False)

    _token = None
    _case_conf = None
    _obj_conf = None
    _auth = None
    log_level = logging.INFO

    def __init__(self, conf_fpn, auto=False, *args, **kwargs):
        self.conf_fpn = conf_fpn
        self._auto = auto

        logger.setLevel(self.log_level)
        if "log_level" in kwargs:
            log_level = kwargs.get("log_level")
            if log_level in (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL):
                logger.setLevel(log_level)
            elif isinstance(log_level, int) and 0 < log_level < 50:
                logger.setLevel(log_level)
            else:
                logger.critical(f"Wrong log level is set")

        logger.debug(f"The configuration file we are using is: {self.conf_fpn}")

        self.obj_confs = ParserJSON(self.conf_fpn)
        pass

    def __del__(self):
        if self.current_case:
            # super().__del__()
            logger.info(f"Test result:{json.dumps(self.test_result, indent=4)}")
            if self.test_passed:
                logger.info(f"Over All Test Passed: {self.test_passed}")
            else:
                logger.error(f"Over All Test Passed: {self.test_passed}")

    def get_auto(self):
        return self._auto

    def set_auto(self, auto):
        self._auto = auto

    auto = property(get_auto, set_auto)

    @property
    def auth_group(self):
        return self.obj_confs.get_group("auth_group", "auth")

    @property
    def auth(self):
        return self.obj_confs.get_group(self.auth_group, {})

    @property
    def obj_auth(self):
        return ParserAuth(self.auth)

    @property
    def base_url(self):
        return f"https://{self.obj_auth.bmc_ip}"

    @property
    def current_url(self):
        url = urllib.parse.urljoin(self.base_url, self.obj_conf.uri)
        return url

    def get_token(self):
        if not self._token:
            data = {
                'username': self.obj_auth.username,
                'password': self.obj_auth.password
            }
            headers = {
                'Content-Type': 'application/json'
            }
            url = urllib.parse.urljoin(self.base_url, "login")
            # resp = requests.post(url=url, data=json.dumps(data), headers=headers, verify=False)
            self.obj_req.send(method='post', url=url, data=json.dumps(data), headers=headers, verify=False)
            self._token = self.obj_req.resp_body.get("token", None)
        return self._token

    def set_token(self, token):
        self._token = token

    token = property(get_token, set_token)

    @property
    def headers(self):
        headers = {
            "X-Auth-Token": self.token
        }
        return headers

    def get_case_conf(self):
        return self.obj_confs.get_group(self.current_case, None)

    def set_case_conf(self, conf):
        self.obj_confs.data_all[self.current_case] = conf

    case_conf = property(get_case_conf, set_case_conf)

    @property
    def obj_conf(self):
        if not self._obj_conf:
            self._obj_conf = ParserCaseConf(self.case_conf)
        return self._obj_conf

    def handle_case_result(self, passed, msg=None):
        if passed is True:
            if msg:
                logger.info(msg)
        else:
            self.test_result[self.current_case]['passed'] = passed
            self.test_passed = passed
            logger.error(msg)

        if msg:
            self.test_result[self.current_case]['msg'].append(msg)


def init_case(case):
    def deco(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            self.current_case = case
            self._obj_conf = None       # set this to be None at the beginning of each case, so the case conf data will be loaded.

            if case not in self.test_result:
                self.test_result[case] = OrderedDict()
                self.test_result[case]['passed'] = True
                self.test_result[case]['msg'] = []
                logger.info(f"=====================================================================================")
                logger.info(f"We are working on case #{self.obj_conf.case_id}, {self.current_case}")
                logger.info(f"Case configuration: {json.dumps(self.obj_conf.data, indent=4)}")

            ret = func(self, *args, **kwargs)
            if self.auto:
                self.obj_confs.data_all[case].update(self.obj_conf.data)    # update test conf when auto sense
            pass
            return ret
        return wrapper
    return deco


class MiBMCRedfish(MiBMCRedfishBase):
    VERSION = 1.5

    def __init__(self, conf_fpn='miBMCRedfish.json', *args, **kwargs):
        super().__init__(conf_fpn, *args, **kwargs)

    @init_case("testThermalSensor")
    def test_thermal_sensor(self):
        self.obj_req.send(method='get', url=self.current_url, headers=self.headers)

        sensors_founded = []

        parse_data = self.obj_req.resp_body.get(self.obj_conf.resp_group, None)
        for sensor_data in parse_data:
            obj_sensor = ParserSensor(sensor_data)

            if obj_sensor.member_id in self.obj_conf.exclude_list:
                logger.warning(f"Excluding sensor: {obj_sensor.member_id}")
                continue

            if self.auto:
                pass
            else:
                if obj_sensor.is_healthy:
                    logger.info(f"{obj_sensor.member_id} is in good health.")
                else:
                    self.handle_case_result(passed=False, msg=f"{obj_sensor.member_id} is in bad health.")

            sensors_founded.append(obj_sensor.member_id)

        if self.auto:
            self.obj_conf.standard_list = sensors_founded
            # pass
        else:
            if self.obj_conf.standard_list:
                logger.info(f"Sensors expected:{json.dumps(self.obj_conf.standard_list, indent=4)}")
                logger.info(f"Sensors founded:{json.dumps(sensors_founded, indent=4)}")
                if sorted(self.obj_conf.standard_list) == sorted(sensors_founded):
                    logger.info(f"All sensors are found..")
                else:
                    self.handle_case_result(passed=False, msg=f"Sensors list comparing failed.")
        pass

    @init_case("testVoltageSensor")
    def test_voltage_sensor(self):
        self.obj_req.send(method='get', url=self.current_url, headers=self.headers)

        sensors_founded = []

        parse_data = self.obj_req.resp_body.get(self.obj_conf.resp_group, None)
        for sensor_data in parse_data:
            obj_sensor = ParserSensor(sensor_data)

            if obj_sensor.name in self.obj_conf.exclude_list:
                logger.warning(f"Excluding sensor: {obj_sensor.name}")
                continue

            if self.auto:
                pass
            else:
                if obj_sensor.is_healthy:
                    logger.info(f"{obj_sensor.name} is in good health.")
                else:
                    self.handle_case_result(passed=False, msg=f"{obj_sensor.name} is in bad health.")

            sensors_founded.append(obj_sensor.member_id)

        if self.auto:
            self.obj_conf.standard_list = sensors_founded
        else:
            if self.obj_conf.standard_list:
                logger.info(f"Sensors expected:{json.dumps(self.obj_conf.standard_list, indent=4)}")
                logger.info(f"Sensors founded:{json.dumps(sensors_founded, indent=4)}")
                if sorted(self.obj_conf.standard_list) == sorted(sensors_founded):
                    logger.info(f"All sensors are found..")
                else:
                    self.handle_case_result(passed=False, msg=f"Sensors list comparing failed.")
        pass

    @init_case("testSensor")
    def test_sensor(self):
        self.obj_req.send(method='get', url=self.current_url, headers=self.headers)

        sensors_founded = []

        # check whether sensor count is expected
        real_sensor_count = self.obj_req.resp_body.get('Members@odata.count', None)
        if self.auto:
            self.obj_conf.expected_sensor_count = real_sensor_count
        else:
            if self.obj_conf.expected_sensor_count == real_sensor_count:
                logger.error(f"Sensor count is expected: {real_sensor_count}")
            else:
                logger.error(f"Sensor count is not expected: got#{real_sensor_count}, "
                             f"expected#{self.obj_conf.expected_sensor_count}")
                self.handle_case_result(passed=False, msg="Sensor count is not expected")

        # get and check real sensor data
        members = get_odata_ids(data=self.obj_req.resp_body)
        for uri in members:
            url = urllib.parse.urljoin(self.base_url, uri)
            self.obj_req.send(method='get', url=url, headers=self.headers)
            obj_sensor = ParserSensor(self.obj_req.resp_body)

            if obj_sensor.id in self.obj_conf.exclude_list:
                logger.warning(f"Excluding sensor: {obj_sensor.id}")
                continue

            if self.auto:
                pass
            else:
                if obj_sensor.is_healthy:
                    logger.info(f"{obj_sensor.name} is in good health.")
                else:
                    self.handle_case_result(passed=False, msg=f"{obj_sensor.name} is in bad health.")

            sensors_founded.append(obj_sensor.id)

        if self.auto:
            self.obj_conf.standard_list = sensors_founded
        else:
            if self.obj_conf.standard_list:
                logger.info(f"Sensors expected:{json.dumps(self.obj_conf.standard_list, indent=4)}")
                logger.info(f"Sensors founded:{json.dumps(sensors_founded, indent=4)}")
                if sorted(self.obj_conf.standard_list) == sorted(sensors_founded):
                    logger.info(f"All sensors are found..")
                else:
                    self.handle_case_result(passed=False, msg=f"Sensors list comparing failed.")
        pass

    @init_case("testFWVersions")
    def test_firmware_versions(self):
        fws = {}
        fws_founded = []

        self.obj_req.send(method='get', url=self.current_url, headers=self.headers)
        members = get_odata_ids(data=self.obj_req.resp_body)
        for uri in members:
            url = urllib.parse.urljoin(self.base_url, uri)
            self.obj_req.send(method='get', url=url, headers=self.headers)
            obj_fw = ParserFirmware(self.obj_req.resp_body)
            if obj_fw.id in self.obj_conf.exclude_list:
                logger.warning(f"Skip checking FW: {obj_fw.desc}")
                continue

            if self.auto:
                pass
            else:
                if self.obj_conf.standard_list and obj_fw.id in self.obj_conf.standard_list:
                    pass
                else:
                    self.handle_case_result(passed=False, msg=f"{obj_fw.id} cannot be found in standard list.")

            fws[obj_fw.id] = obj_fw.version
            fws_founded.append(obj_fw.id)
            pass

        if self.auto:
            self.obj_conf.standard_list = fws
        else:
            # chk result
            if fws == self.obj_conf.standard_list:
                logger.info(f"All FW versions Are expected, data we got {json.dumps(fws, indent=4)}.")
            else:
                logger.error(f"FW versions test failed, data we got {json.dumps(fws, indent=4)}, "
                             f"expected list:{json.dumps(self.obj_conf.standard_list, indent=4)}")
                self.handle_case_result(passed=False, msg="FW versions test failed")

            if self.obj_conf.standard_list:
                logger.info(f"FWs expected:{json.dumps(self.obj_conf.standard_list, indent=4)}")
                logger.info(f"FWs founded:{json.dumps(fws_founded, indent=4)}")
                if sorted(self.obj_conf.standard_list) == sorted(fws_founded):
                    logger.info(f"All sensors are found..")
                else:
                    self.handle_case_result(passed=False, msg=f"Sensors list comparing failed.")
        pass

    @init_case("testRedfishSEL")
    def test_redfish_sel(self):
        self.obj_req.send(method='get', url=self.current_url, headers=self.headers)
        entries = self.obj_req.resp_body.get("Members")

        for entry in entries:
            obj = ParserRedfishSEL(entry)
            if obj.message_id in self.obj_conf.exclude_list:
                continue
            else:
                if self.auto:
                    self.obj_conf.exclude_list.append(obj.message_id)
                else:
                    self.handle_case_result(passed=False, msg=f"Found unexpected Redfish SEL on {obj.created} "
                                                              f": {obj.message_id}.")

        if self.auto:
            self.obj_conf.exclude_list = sorted(list(set(self.obj_conf.exclude_list)))


if __name__ == "__main__":
    a = MiBMCRedfish()
    a.auto = True
    a.test_thermal_sensor()
    a.test_voltage_sensor()
    a.test_sensor()
    a.test_firmware_versions()
    a.test_redfish_sel()

pass
