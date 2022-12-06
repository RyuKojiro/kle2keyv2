#!/usr/bin/env python3

import json
import os
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-I', dest='layout_path', default='..',
                    help='path to layout directory in KeyV2 (default: ../)')
parser.add_argument('--no-legends', dest='enable_legends', action='store_false',
                    help='Disables key legends')
parser.add_argument('files', type=str, nargs='+',
                    help='files to convert')

args = parser.parse_args()

def sanitizedLegend(unsafe):
    legends = key.split("\n")
    legend = legends[-1]

    if legend == '\\':
        return '\\\\'

    return legend

for arg in args.files:
    with open(arg) as fp:
        basename = os.path.splitext(os.path.basename(arg))[0]
        j = json.load(fp)
        
        layout = list()
        legends = list()
        for row in j:
            lay = list()
            leg = list()

            w = 1
            for key in row:
                if type(key) is dict:
                    if 'x' in key:
                        lay.append(0 - key['x'])
                    if 'w' in key:
                        w = key['w']
                else:
                    lay.append(w)
                    leg.append(sanitizedLegend(key))
                    w = 1

            layout.append(lay)
            legends.append(leg)

        print("include <%s/layout.scad>"%args.layout_path)
        print("")
        print("%s_layout = [" % basename)
        for row in layout:
            print('\t' + str(row) + ',')
        print("];")
        print("")
        if args.enable_legends:
            print("%s_legends = [" % basename)
            for row in legends:
                print('\t["' + '", "'.join(row) + '"],')
            print("];")
            print("")
        print("module %s_default(profile) {" % basename)

        if args.enable_legends:
            print("\tlayout(%s_layout, profile, %s_legends) children();" % (basename, basename))
        else:
            print("\tlayout(%s_layout, profile) children();" % basename)

        print("}")
