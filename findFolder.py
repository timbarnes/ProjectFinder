#!/usr/bin/python3
import os
import sys

PROJECT_BASE = 'P:/'
PHOTO_BASE = 'G:/PHOTOS of our PROJECTS/'

if len(sys.argv) < 3:
    sys.exit("Usage: findProject project|photos pattern")
if sys.argv[1] == 'project':
    folders = os.listdir(PROJECT_BASE)
elif sys.argv[1] == 'photos':
    folders = os.listdir(PHOTO_BASE)
else:
    sys.exit("Usage: findProject project|photos pattern")


results = [x for x in folders if x.upper().count(sys.argv[2].upper()) > 0]
c = 1
for x in results:
    print("{:02}: {}".format(c, x))
    c += 1
