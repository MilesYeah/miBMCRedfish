#!/usr/bin/python3

import argparse
# from collections import FunctionType
import re

from miBMCRedfish import MiBMCRedfish
from py_core.handlerLogger import logger

parser = argparse.ArgumentParser()

parser.add_argument('-j', '--json', help="specify configuration file to run", type=str)
parser.add_argument('-l', '--ls', help="list available cases", action='store_true')
parser.add_argument('-c', '--cases', help="specify case names to run", type=str)
parser.add_argument('-n', '--num', help="specify cases number to run", type=str)
# parser.add_argument('-m', '--module', help="specify module to run", type=str)

parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-V", "--version", help="Show version of package", action="store_true")

args = parser.parse_args()

# if args.help:
#     exit(0)

if args.verbose:
    print(f"Verbose mode")

if args.json:
    obj = MiBMCRedfish(args.json)
else:
    obj = MiBMCRedfish()

if args.version:
    logger.info(f"Version of miBMCRedfish: {obj.VERSION}")
    exit(0)

AVAILABLE_CASES = []
for attr in MiBMCRedfish.__dict__:
    if attr.startswith('test'):
        AVAILABLE_CASES.append(getattr(MiBMCRedfish, attr))

if args.ls:
    for item in enumerate(AVAILABLE_CASES):
        print(f"{item[0]:> 6} : {item[1].__name__}")
        pass
    exit(0)
    pass


TO_RUNs = []
if args.cases:
    if re.findall('all', args.cases, re.I):
        TO_RUNs = AVAILABLE_CASES
    else:
        for case in re.split('[,:]', args.cases):
            TO_RUNs.append(getattr(MiBMCRedfish, case))
            pass
elif args.num:
    try:
        if ":" in args.num or "-" in args.num:
            start, end = re.split('[-:]', args.num)
            TO_RUNs = AVAILABLE_CASES[int(start):int(end) + 1]
        elif re.findall('all', args.num, re.I):
            TO_RUNs = AVAILABLE_CASES
        else:
            nums = re.split('[,]', args.num)
            for num in nums:
                TO_RUNs.append(AVAILABLE_CASES[int(num)])
    except IndexError as e:
        MiBMCRedfish.test_passed = False
        logger.error(f"{e}, cannot find specified case.")
        logger.info("Please select from below list:")
        for item in enumerate(AVAILABLE_CASES):
            print(f"{item[0]:> 6} : {item[1].__name__}")
        exit(2)
else:
    logger.error("Please specify one or more case to run.")
    exit(3)

for case in TO_RUNs:
    case(obj)

if not obj.test_passed:
    exit(1)

pass
