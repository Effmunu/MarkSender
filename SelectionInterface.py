#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Implements the GUI interface for selecting students and topics.
Also provides conversion function for 1D and 2D arrays of tk.BooleanVar into
1D or 2D array of int (easier to use afterwards).

:Author: NPAC 2015-2016
:Date: 11 Mar 2016
:Mail: antoine.laudrain[at]u-psud.fr
"""

import sys
import Tkinter as tk
from Buttons import *


def gui(data, topic_list, student_list):
    """
    GUI interface for selecting students and topics.
    We define an array of booleans, each controlling a whole student.
    We define an array of booleans, each controlling a whole topic.
    We define a 2D array of booleans, each controlling single topic for single
    student.
    All booleans are objects from tk.BooleanVar in order to be bound to the
    Checkbuttons.
    The display is done as follow : we define 5 zones: (grid = (row, column))
        the center one contains the array of checkbuttons
            (grid : (2, 2) -> (nb_student+1, nb_topic+1)
        the left one contains 2 columns: checkbutton and student name
            (grid : (2, 0) -> (nb_student+1, 1)
        the right one (symmetric): student name and checkbutton
            (grid : (2, nb_topic+2) -> (nb_student+1, nb_topic+3)
        the top one contains 2 rows: topic name and checkbutton
            (grid : (0, 2) -> (1, nb_topic+1)
        the bot one (symmetric): checkbutton and topic name
            (grid : (nb_student+2, 2) -> (nb_student+3, nb_topic+1)
    I added a select_all, and a reset button.
    Also added a validate (which is actually like closing the window) and an
    abort button which actually reset and validate (to be changed ?)
    ---------------
    :param topic_list: list of the topics in the order they should appear
    :param student_list: list of the students in the order they should appear
    """
    window = tk.Tk() # must be before everything else... Don't exactly know why.

    nb_student = len(student_list)
    nb_topic = len(topic_list)
    # note that tk.BooleanVar() value is False by default
    # prepare the boolean array for student global controllers
    bool_student = [tk.BooleanVar() for student in range(nb_student)]
    # prepare the boolean array for topic global controllers
    bool_topic = [tk.BooleanVar() for topic in range(nb_topic)]
    # prepare the boolean 2D array for single controllers
    bool_array = [[tk.BooleanVar() for topic in range(nb_topic)] \
                                   for student in range(nb_student)]


    # Now display the elements

    # Fill the left and right zones with student labels and master checkboxes.
    for student in range(nb_student):
        # if there is no student (empty line header), disable the left button.
        if student_list[student] == "":
            tk.Checkbutton(state=tk.DISABLED, master=window)\
                .grid(row=student+2, column=0)
        # else, make a full Student control button.
        else:
            StudentCheckbutton(student, bool_topic, bool_student, bool_array, student_list, topic_list, data, window)\
                .grid(row=student+2, column=0)
        # in both case, draw the labels, left and right.
        tk.Label(window, text=student_list[student])\
            .grid(row=student+2, column=1)
        tk.Label(window, text=student_list[student])\
            .grid(row=student+2, column=nb_topic+2)
        # if there is no student (empty line header), disable the right button.
        if student_list[student] == "":
            tk.Checkbutton(state=tk.DISABLED, master=window)\
                .grid(row=student+2, column=nb_topic+3)
        # else, make a full Student control button.
        else:
            StudentCheckbutton(student, bool_topic, bool_student, bool_array, student_list, topic_list, data, window)\
                .grid(row=student+2, column=nb_topic+3)

    # Fill the top and bot zones with topic labels and master checkboxes.
    for topic in range(nb_topic):
        # draw the top label.
        tk.Label(window, text=topic_list[topic]).grid(row=0, column=topic+2)
        # if there is no topic (empty column header), disable the top and 
        # bottom buttons
        if topic_list[topic] == "":
            tk.Checkbutton(state=tk.DISABLED, master=window)\
                .grid(row=1, column=topic+2)
            tk.Checkbutton(state=tk.DISABLED, master=window)\
                .grid(row=nb_student+2, column=topic+2)
        # else, make the full topic control top and bottom buttons
        else:
            TopicCheckbutton(topic, bool_topic, bool_student, bool_array, student_list, topic_list, data, window)\
                .grid(row=1, column=topic+2)
            TopicCheckbutton(topic, bool_topic, bool_student, bool_array, student_list, topic_list, data, window)\
                .grid(row=nb_student+2, column=topic+2)
        # draw the bottom label.
        tk.Label(window, text=topic_list[topic])\
            .grid(row=nb_student+3, column=topic+2)

    # Fill the center zone with the array of checkboxes.
    for student in range(nb_student):
        for topic in range(nb_topic):
            # if there are no student or topic header, or the cell is not
            # filled, the cell should not be clickable.
            if student_list[student] == ""\
            or topic_list[topic] == ""\
            or data[student+4][topic+3] == "":
                tk.Checkbutton(state=tk.DISABLED, master=window)\
                    .grid(row=student+2, column=topic+2)
            # otherwise, put a single button
            else:
                SingleCheckbutton(topic, student, bool_topic, bool_student, bool_array, student_list, topic_list, data, window)\
                    .grid(row=student+2, column=topic+2)

    def select_all():
        for student in range(nb_student):
            for topic in range(nb_topic):
                bool_array[student][topic].set(True)
        for student in range(nb_student):
            bool_student[student].set(True)
        for topic in range(nb_topic):
            bool_topic[topic].set(True)

    def reset():
        for student in range(nb_student):
            for topic in range(nb_topic):
                bool_array[student][topic].set(False)
        for student in range(nb_student):
            bool_student[student].set(False)
        for topic in range(nb_topic):
            bool_topic[topic].set(False)

    def abort():
        reset()
        window.quit()

    # select_all button: top right
    tk.Button(window, text="ALL", command=select_all)\
        .grid(row=0, column=nb_topic+2, rowspan=2, columnspan=2)
    # reset button: top left
    tk.Button(window, text="Reset", command=reset)\
        .grid(row=0, column=0, rowspan=2, columnspan=2)
    # validate_button: bottom right
    tk.Button(window, text="Validate", command=window.quit)\
        .grid(row=nb_student+2, column=nb_topic+2, rowspan=2, columnspan=2)
    # abort_button: bottom left
    tk.Button(window, text="Abort", command=abort)\
        .grid(row=nb_student+2, column=0, rowspan=2, columnspan=2)

    window.mainloop()
    return bool_topic, bool_student, bool_array


def to_std_1Darray(bool_list):
    """
    Convert a 1D array of Tkinter.BooleanVar into a 1D array of int
    ---------------
    :param bool_array: 1D array of BooleanVar
    :return: 1D array of int
    """
    return [1 if b.get() else 0 for b in bool_list]


def to_std_2Darray(bool_array):
    """
    Convert a 2D array of Tkinter.BooleanVar into a 2D array of int
    ---------------
    :param bool_array: 2D array of BooleanVar
    :return: 2D array of int
    """
    return [to_std_1Darray(b_list) for b_list in bool_array]


def print_BooleanVar_map(bool_topic, bool_student, bool_array):
    """
    Debug function to print the values in the arrays containing the boolean
    variables.
    ---------------
    :param bool_topic: array of the boolean for topic masters
    :param bool_student: array of the booleans for student masters
    :param bool_array: array 2D of the booleans for single.
    """
    print '  [',
    for i in range(len(bool_topic)):
        print 1 if bool_topic[i].get() else 0, ',',
    print ']'
    for i in range(len(bool_student)):
        print 1 if bool_student[i].get() else 0, '[',
        for j in range(len(bool_topic)):
            print 1 if bool_array[i][j].get() else 0, ',',
        print ']'


if __name__ == '__main__':
    this_topic_list = ['AC_total', 'Nuclei_final', 'Cosmo_final', 'GR', 
                       'Nuclei_total', 'Detectors', 'QFT_midterm',
                       'Nuclei_midterm', 'Accelerators', 'TL',
                       'Particles_final', 'QFT_total', 'Astro_midterm', 
                       'Particles_total', 'QFT_final', 'Particles_midterm']
    this_topic_list.sort()
    this_student_list = ['A', 'B', 'C', 'D']

    bool_topic, bool_student, bool_array = gui(this_topic_list, this_student_list)
    print_BooleanVar_map(bool_topic, bool_student, bool_array)

    sys.exit(0)
