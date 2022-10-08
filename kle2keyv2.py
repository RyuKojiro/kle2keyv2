#!/usr/bin/env python3

import json
import sys
import os

for arg in sys.argv[1:]:
    with open(arg) as fp:
        basename = os.path.splitext(os.path.basename(arg))[0]
        j = json.load(fp)
        
        layout = list()
        legends = list()
        for row in j:
            lay = list()
            leg = list()

            for key in row:
                lay.append(1)

            layout.append(lay)
            legends.append(leg)

        print("include <KeyV2/src/layout/layout.scad>")
        print("")
        print("%s_layout = [" % basename)
        for row in layout:
            print('\t' + str(row) + ',')
        print("];")
        print("")
        print("%s_legends = [" % basename)
        for row in legends:
            print('\t' + str(row) + ',')
        print("];")
        print("")
        print("module %s_default(profile) {" % basename)
        print("\tlayout(%s_layout, profile, %s_legends) children();" % (basename, basename))
        print("}")
