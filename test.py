#!/usr/bin/python

import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument("arguments", help="")#, nargs='+')
parser.add_argument("-o","--option", help="", action="store_true")
args = parser.parse_args()

print args.arguments #Contains the list of file names given in arguments
print args.option  #Contains value of option (True if -o precise, False if not)

# >>>python test.py mycsv1.csv mycsv2.csv
# args.arguments -> ['mycsv1.csv', 'mycsv2.csv']
# args.option -> False

### /!\
# Multiple arguments are allowed by "nargs='+'"
# if you only want one argument remove this option,
# and 'args.arguments' will just give you the string 'mycsv1.csv'

# in that case:
# >>>python test.py mycsv1.csv mycsv2.csv
# test.py: error: unrecognized arguments: mycsv2.csv

# and:
# >>>python test.py mycsv.csv -o
# args.arguments -> 'mycsv.csv'
# args.option -> True
### /!\

# python test.py -o
# This will give you:
# main.py: error: too few arguments

### /!\
# If you remove 'action="store_true"' in the definition of option
# this will allows you to pass a optional string into 'args.option'

#in that case:
# >>>python test.py mycsv.csv
# args.arguments -> ['mycsv.csv'] # if you keep "nargs='+'" option
# args.option -> None

# and:
# >>>python test.py mycsv.csv -o mystring
# args.arguments -> 'mycsv.csv' # if you remove "nargs='+'" option
# args.option -> 'mystring'

# and:
# >>>python test.py mycsv.csv -o
# test.py: error: argument -o/--option: expected one argument
### /!\

# If you make your main.py an executable 'chmod +x main.py',
# you can use:
# ./main.py mycsv.csv
# instead of:
# python main.py mycsv.csv
### /!\
# I have already done this in the first pull request.
### /!\

# And in addition you can add the MarkSender
# (the directory which contains main.py and the modules)
# to the PATH 'PATH=$PATH:/path/to/MarkSender'
# (you can write this in terminal or in .bashrc)
# and you can write:
# main.py mycsv.csv

# Renaming main.py into marksender you can just write:
# marksender mycsv.csv
