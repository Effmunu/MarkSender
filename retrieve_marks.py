#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Retrieve the marks of a group a students from a CSV chart in order to
automatically send them by mail.
Skeleton of the CSV file: separated by semi-colons ';'

First  line: Name, Surname, Email, name of the topics...
Second line: Mean values for each topic
Third  line: Max values for each topic
Fourth line: Min values for each topic
Following lines: students data

Thus the first 3 columns and first 4 lines are reserved space.

:Author: NPAC 2015-2016
:Date: August 2016
:Mail: antoine.laudrain[at]u-psud.fr
"""

import sys
import copy

def build_list_dic(file_raw_data, sort_students, sort_topics):
    """
    Builds the topics and students lists and dictionaries from the raw data in
    the csv file.
    The students/topics list is the alphabetical list of students/topics. This
    should be further used to display the students/topics in the right order in
    the graphical interface.
    The students/topics dictionary is used for sorting. It associates the
    line/column number of the student/topic in the file read, so before sorting.
    Dictionnaries: keys = names; values = line/column number.
    -------------------------------------------------------
    :param file_raw_data: list of the lines in the CSV file
    :param sort_students: boolean flag for student sorting
    :param sort_topics: boolean flag for topic sorting
    :returns: data (list of list formatted csv file), topic_list, student_list
    """

    # readlines returns the list of lines, finishing by '\n', so we remove
    # these characters. We also format the data to be easily usable : split the
    # csv file wrt each cell
    data = []
    for line in file_raw_data:
        data.append(line[:-1].split(';'))
    # now we have a 2D list with the values

    # Create a dictionary for topics, needed for eventual sorting:
    # columns 0,1,2 are name, surname and email, so skipped
    topic_list = []
    for topic_nb in range(3, len(data[0])):
        topic_list.append(data[0][topic_nb])
        # I know I could have a better syntax for this operation
        # (for topic in data[0]... append(topic)) but I keep it for the sake for
        # symmetry with the student part where it is not possible.
    topic_dic = {}
    for topic_nb in range(len(topic_list)):
        topic_dic[topic_list[topic_nb]] = topic_nb

    # Create a dictionary of students, needed for eventual sorting:
    # skip line 0 to 3 since they are the list of subjects, mean, max, min
    student_list = []
    for student_nb in range(4, len(data)):
        student_list.append(data[student_nb][0])
    student_dic = {}
    for student_nb in range(len(student_list)):
        student_dic[student_list[student_nb]] = student_nb

    ########################################################
    # alphabetically sort data if options were passed
    ########################################################

    if sort_topics:
        # sort the list of topics
        topic_list.sort()
        unsorted_data = copy.deepcopy(data)
        # fill the 3 first columns for all lines
        topic_sorted_data = [data[line_nb][0:3] for line_nb in range(len(data))]
        # fill the topic columns
        for topic in topic_list:
            topic_nb = topic_dic[topic]
            for line_nb in range(len(data)):
                data[line_nb].append( unsorted_data[line_nb][topic_nb + 3] )

    if sort_students:
        # sort the list of students
        student_list.sort()
        unsorted_data = copy.deepcopy(data)
        # fill the 4 first lines
        data = [unsorted_data[line_nb] for line_nb in range(4)]
        # fill the student lines, loop is ordered
        for student in student_list:
            student_nb = student_dic[student] # pick the original student number
            data.append( unsorted_data[student_nb + 4] )

    return data, topic_list, student_list


if __name__ == "__main__":
    input_file_path = "test_marks.csv"
    try:
        with open(input_file_path, 'r') as input_file:
            file_raw_data = input_file.readlines()
    except IOError:
        print "File not found :", input_file_path
        sys.exit(1)

    # build the topic and student dictionaries
    data, topic_list, student_list = build_list_dic(file_raw_data, False, False)
    print "data :"
    print data
    print ' '
    print "Topics found: ", topic_list
    print "Students found: ", student_list

    sys.exit(0)

