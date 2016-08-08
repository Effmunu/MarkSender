#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Open a CSV file and build dictionaries of topic and students.
Open GUI to select which topics / students should be sent their marks.
Build the mails.
Send the mails

:Author: NPAC 2015-2016
:Date: 12 Mar 2016
:Mail: antoine.laudrain[at]u-psud.fr
"""

import sys
import argparse
import SelectionInterface as seli
from retrieve_marks import build_list_dic
import mailUtils as mailU

def main(argv):
    """
    Main program.
    ---------------
    :param argv: described in built-in help
    :return:    0 if evertything ok,
                1 if file couldn't be opened.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path", metavar="file",
                    help="csv input file, semi-column separated")
    parser.add_argument("-s", "--sort-students", action="store_true",
                    help="alphabetically sort the students before the display")
    parser.add_argument("-t", "--sort-topics", action="store_true",
                    help="alphabetically sort the topics before display")
    parser.add_argument("--dry-run", action="store_true",
                    help="do everything without actually sending the mails")

    args = parser.parse_args()

    # the csv file should have semi-colon (;) separated values
    try:
        with open(args.input_file_path, 'r') as input_file:
            file_raw_data = input_file.readlines()
    except IOError:
        print "File not found:", input_file_path
        return 1

    # build the topics and students list and dictionary
    data, topic_list, student_list = build_list_dic(file_raw_data,\
        args.sort_students, args.sort_topics)

    # open the selection interface
    _, _, bool_array = seli.gui(topic_list, student_list)
    # convert the array
    to_send_array = seli.to_std_2Darray(bool_array)

    if not args.dry_run:
        for student_nb in range(len(student_list)):
            mail_body = mailU.build_body(student_nb, topic_list, data, to_send_array)
            if mail_body == "":
                continue
            mailU.send_mail_fake(data[student_nb+4][2], mail_body)
            # column 2 contains the mails



if __name__ == '__main__':
    sys.exit(main(sys.argv))

