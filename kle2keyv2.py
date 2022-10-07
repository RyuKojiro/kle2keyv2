#!/usr/bin/env python3

import json
import sys

for arg in sys.argv[1:]:
    with open(arg) as fp:
        j = json.load(fp)
        
        print(j)
