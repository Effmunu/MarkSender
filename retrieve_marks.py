#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Retrieve the marks of a group a students from a CSV chart 
in order to automatically send them by mail.
TODO : the mail sending part has still to be done.
Skeleton of the CSV file : separated by semi-colons ';'

First  line: Name, Surname, Email, name of the topics...
Second line: Mean values for each topic
Third  line: Max values for each topic
Fourth line: Min values for each topic
Following lines: students data

Thus the first 3 columns and first 4 lines are reserved space.

:Author: NPAC 2015-2016
:Date: 20 Feb 2016
:Mail: antoine.laudrain[at]u-psud.fr
"""

import sys

def build_list_dic(file_raw_data):
    """
    Builds the topics and students lists and dictionaries from the raw data in
    the csv file.
    The topics list is the alphabetical list of topics. This should be further
    used to display the topics in the right order in the graphical interface.
    The topics dictionary associates the column number of the future array of
    booleans to the topic name.
    The students list is the alphabetical list of students. This should be
    further used to display the topics in the right order on the graphical
    interface.
    The students dictionary associates the row number of the future array of 
    booleans to the student name.
    I must use a separated list because dic.keys() or dic.values() return a list
    which is shuffled.
    Dictionnaries: keys = names; values = line/column number
    ---------------
    :param file_raw_data: list of the lines in the CSV file
    :returns: data (list of list formatted csv file), topic_list, student_list,
    topic_dic, student_dic
    """

    # readlines returns the list of lines, finishing by '\n', so we remove
    # these characters. We also format the data to be easily usable : split the
    # csv file wrt each cell
    data = []
    for line in file_raw_data:
        data.append(line[:-1].split(';'))
    # now we have a 2D list with the values

    # create a dictionary for topics:
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

    # create a dictionary of students:
    # skip line 0 to 3 since they are the list of subjects, mean, max, min
    student_list = []
    for student_nb in range(4, len(data)):
        student_list.append(data[student_nb][0])
    student_dic = {}
    for student_nb in range(len(student_list)):
        student_dic[student_list[student_nb]] = student_nb

    # alphabetically sort data

    # sort the topic columns
    # sort the list of topics
    topic_list.sort()
    # fill the 3 first columns
    topic_sorted_data = [data[line_nb][0:3] for line_nb in range(len(data))]
    # fill the topic columns
    for topic in topic_list:
        topic_nb = topic_dic[topic]
        for line_nb in range(len(data)):
            topic_sorted_data[line_nb].append(data[line_nb][topic_nb + 3])

    # sort the student lines
    # sort the list of students
    student_list.sort()
    # fill the 4 first lines
    data = [topic_sorted_data[line_nb] for line_nb in range(4)]
    # fill the student lines
    for student in student_list:
        student_nb = student_dic[student]
        data.append(topic_sorted_data[student_nb + 4])

    return data, topic_list, student_list, topic_dic, student_dic


if __name__ == "__main__":
    input_file_path = "test_marks.csv"
    try:
        with open(input_file_path, 'r') as input_file:
            file_raw_data = input_file.readlines()
    except IOError:
        print "File not found :", input_file_path
        sys.exit(1)

    # build the topic and student dictionaries
    data, topic_list, student_list, topic_dic, student_dic\
        = build_list_dic(file_raw_data)
    print "data :"
    print data
    print ' '
    print "Topics found: ", topic_list
    print "Students found: ", student_list

    sys.exit(0)

