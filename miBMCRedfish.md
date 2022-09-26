# miBMCRedfish

## Init environment
Please install required libraries by command `pip install -r requirements.txt` with Internet access.





## Run
All data will be saved in log file: `logs/all.log`.

Previous log files will be renamed to `all.log.{file_modify_datetime}.bak`



### Command line instructions
```hlp

python main.py -h

usage: main.py [-h] [-j JSON] [-l] [-c CASES] [-n NUM] [-a] [-v] [-V]

options:
  -h, --help            show this help message and exit
  -j JSON, --json JSON  specify configuration file to run
  -l, --ls              list available cases
  -c CASES, --cases CASES
                        specify case names to run
  -n NUM, --num NUM     specify cases number to run
  -a, --auto            auto sense
  -v, --verbose         increase output verbosity
  -V, --version         Show version of package

```

* `-j JSON, --json JSON`
  * specify test configuration file
  * default: `miBMCRedfish.json`
  * if the json file is not in current folder, specify abs path please
* `-l, --ls`
  * list available test cases
* `-c CASES, --cases CASES`
  * specify to be tested case names
  * use `all` to run all cases, case insensitive
    * `python.exe main.py -c all`
  * use `,` or `:` split case names, `,:`can be used at same time
    * `python.exe main.py -c test_thermal_sensor,test_voltage_sensor:test_firmware_versions`
  * Example: 
* `-n NUM, --num NUM`
  * specify to be tested case names
  * use `all` to run all cases, case insensitive
  * use `,` to specify single enumerations of case, this can also specify test sequence
    * `python.exe main.py -n 0,3,1`
  * use `-` or `:` to specify a series of case
    * `python.exe main.py -n 0:3`
    * `python.exe main.py -n 0-3`
* `-a, --auto`            
  * auto sense
* `-V, --version`
  * Show version of MiBMCRedfish




## Configurations

All parameters are defined in file `miBMCRedfish.json`

### auth
```json
"auth_group": "auth",
"auth": {
    "username": "miles",
    "password": "Aa123456",
    "BMCIP": "192.168.123.98"
},
"auth_intel": {
    "username": "admin",
    "password": "Superuser@123",
    "BMCIP": "192.168.123.98"
},
```

* auth_group
  * we can define several groups for authentication, and specify the auth group by this parameter
  * the default auth group is `auth` when auth_group is not defined
* username
  * user name of redfish
* password
  * password name of redfish
* BMCIP
  * ip address of redfish


### testThermalSensor
```json
"testThermalSensor": {
    "caseID": 1,
    "method": "test_thermal_sensor",
    "URI": "redfish/v1/Chassis/FCP_Baseboard/Thermal",
    "standardList": [],
    "excludeList": [
        "Aggr1 Temp",
        "BB BMC Temp"
    ],
    "resp_group": "Temperatures",
    "expected_sensor_count": 10
},
```

* caseID
  * the enum of current case
* method
  * the method defined in Python source code
* URI
  * the URI to get thermal sensors
* standardList
  * expected sensor list to be checked
  * check all the sensors when this value is empty
  * `MemberId` will be the sensor name
* excludeList
  * sensors we skip check
* resp_group
  * the group name to get sensors in a group
* expected_sensor_count
  * check the expected sensor count



### testVoltageSensor
```json
"testVoltageSensor": {
    "caseID": 2,
    "method": "test_voltage_sensor",
    "URI": "redfish/v1/Chassis/FCP_Baseboard/Power",
    "standardList": [],
    "excludeList": [],
    "resp_group": "Voltages",
    "expected_sensor_count": 10
},
```

* caseID
  * the enum of current case
* method
  * the method defined in Python source code
* URI
  * the URI to get thermal sensors
* standardList
  * expected sensor list to be checked
  * check all the sensors when this value is empty
  * `MemberId` will be the sensor name
* excludeList
  * sensors we skip check
* resp_group
  * the group name to get sensors in a group
* expected_sensor_count
  * check the expected sensor count


### testSensor
```json
"testSensor": {
    "caseID": 3,
    "method": "test_sensor",
    "URI": "redfish/v1/Chassis/FCP_Baseboard/Sensors",
    "standardList": [],
    "excludeList": [],
    "resp_group": "Members",
    "expected_sensor_count": 11
},
```
* caseID
  * the enum of current case
* method
  * the method defined in Python source code
* URI
  * the URI to get thermal sensors
* standardList
  * expected sensor list to be checked
  * check all the sensors when this value is empty
  * `Id` will be the sensor name
* excludeList
  * sensors we skip check
* resp_group
  * the group name to get sensors in a group
* expected_sensor_count
  * check the expected sensor count


### testFWVersions
```json
"testFWVersions": {
    "caseID": 3,
    "method": "test_firmware_versions",
    "URI": "redfish/v1/UpdateService/FirmwareInventory",
    "standardList": {
        "HSBP1_CPLD1": "00.02.01.01 ",
        "HSBP1_CPLD2": "00.02.01.01",
        "afm_recovery": "0.0",
        "afm_active": "0.0",
        "bios_active": "SE5C7411.86B.8424.D03.2207271338",
        "bios_recovery": "84.24.4403",
        "bmc_active": "egs-1.19-0-gd174d3-3cc10000",
        "bmc_recovery": "egs-1.19-0-0000",
        "cpld_active": "FCP_v2p0",
        "cpld_recovery": "2.0",
        "me": "06.00.03.172.0"
    },
    "excludeList": []
}
```
* caseID
  * the enum of current case
* method
  * the method defined in Python source code
* URI
  * the URI to get thermal sensors
* standardList
  * expected sensor list to be checked
  * check all the sensors when this value is empty
  * `Id` will be the sensor name
* excludeList
  * sensors we skip check


### testRedfishSEL
```json
"testRedfishSEL": {
    "caseID": 4,
    "method": "test_redfish_sel",
    "URI": "redfish/v1/Systems/system/LogServices/EventLog/Entries",
    "standardList": [],
    "excludeList": [
        "OpenBMC.0.1.BIOSBoot",
        "OpenBMC.0.1.BMCTimeUpdatedViaHost",
        "OpenBMC.0.1.CPUStatus",
        "OpenBMC.0.1.ChassisIntrusionDetected",
        "OpenBMC.0.1.DCPowerOff",
        "OpenBMC.0.1.DCPowerOn",
        "OpenBMC.0.1.EventLogCleared",
        "OpenBMC.0.1.InvalidLoginAttempted",
        "OpenBMC.0.1.InventoryAdded",
        "OpenBMC.0.1.InventoryRemoved",
        "OpenBMC.0.1.LinkStatusChanged",
        "OpenBMC.0.1.OCPStatus",
        "OpenBMC.0.1.PowerButtonPressed",
        "OpenBMC.0.1.PowerRestorePolicyApplied",
        "OpenBMC.0.1.PowerSupplyInserted",
        "OpenBMC.0.1.PowerSupplyPowerLost",
        "OpenBMC.0.1.SELEntryAdded",
        "OpenBMC.0.1.ServiceFailure",
        "OpenBMC.0.1.SystemInterfaceUnprovisioned",
        "OpenBMC.0.1.FirmwareUpdateStarted",
        "OpenBMC.0.1.FirmwareUpdateStaged"
    ]
}
```
* caseID
  * the enum of current case
* method
  * the method defined in Python source code
* URI
  * the URI to get redfish sel entries
* standardList
  * None
* excludeList
  * Allowed Redfish SEL





## Release note

### 1.5
* Add option auto-sense
  * a file name can be specified before saving data.
* Add script to init environment.

### 1.4
* When test case is not passed, the exit code will not be 0.
* Add pip whiles so we can initialize the environment offline.

### 1.3
* Fix a log message bug in v1.2 since we used colorlog, so there are some unexpected charactors in each message, see below example for reference
  * `[1;32mI 2022-09-23 10:16:15,161 [0m| [34mINFO`
* Add python inpretater path for Linux usage

### 1.2
* Optimize logging module
  * Each log level has it own color, such as green, red, yellow

### 1.1
* Add an option to customize log level while initializing object for MiBMCRedfishBase
* Add option to show Version
  * when specifying showing FW of MiBMCRedfishBase, the test result will not be shown.

### 1.0
* Add command line options.
* Release test cases:
  * testThermalSensor
  * testVoltageSensor
  * testSensor
  * testFWVersions
  * test_redfish_sel
