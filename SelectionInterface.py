#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Implements the GUI interface for selecting students and topics.
Also provides conversion function for 1D and 2D arrays of tk.BooleanVar into
1D or 2D array of int (easier to use afterwards).

:Author: NPAC 2015-2016
:Date: Created 11 Mar 2016 - Last update 12 Aug 2016
:Mail: antoine.laudrain[at]u-psud.fr
"""

import sys
import Tkinter as tk
from Buttons import *


class SelectionInterface(object):
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
    """

    def __init__(self, data, topic_list, student_list):
        """
        Initialization of the GUI.
        ---------------
        :param topic_list: list of the topics in the order they should appear
        :param student_list: list of the students in the order they should appear
        """

        self.data = data
        self.topic_list = topic_list
        self.student_list = student_list
        self.nb_student = len(student_list)
        self.nb_topic = len(topic_list)

        self.window = tk.Tk() # must be before everything else... Don't exactly know why.

        # note that tk.BooleanVar() value is False by default
        # prepare the boolean array for student global controllers
        self.bool_student = [tk.BooleanVar() for iStudent in range(self.nb_student)]
        # prepare the boolean array for topic global controllers
        self.bool_topic = [tk.BooleanVar() for iTopic in range(self.nb_topic)]
        # prepare the boolean 2D array for single controllers
        self.bool_single = [[tk.BooleanVar() for iTopic in range(self.nb_topic)] \
                                for iStudent in range(self.nb_student)]

        # Now display the elements
        self.display_topics()
        self.display_students()
        self.display_single()
        self.display_aux()

        self.window.mainloop()

    #######################################################
    def display_students(self):
        """
        Display the left and right parts of the selection interface (students).
        """

        # Fill the left and right zones with student labels and master checkboxes.
        for iStudent in range(self.nb_student):
            # if there is no student (empty line header), disable the left button.
            if self.student_list[iStudent] == "":
                tk.Checkbutton(state=tk.DISABLED, master=self.window)\
                    .grid(row=iStudent+2, column=0)
            # else, make a full Student control button.
            else:
                StudentCheckbutton(iStudent,
                                self.bool_topic, self.bool_student, self.bool_single,
                                self.student_list, self.topic_list, self.data,
                                self.window)\
                    .grid(row=iStudent+2, column=0)

            # in both case, draw the labels, left and right.
            tk.Label(self.window, text=self.student_list[iStudent])\
                .grid(row=iStudent+2, column=1)
            tk.Label(self.window, text=self.student_list[iStudent])\
                .grid(row=iStudent+2, column=self.nb_topic+2)

            # if there is no student (empty line header), disable the right button.
            if self.student_list[iStudent] == "":
                tk.Checkbutton(state=tk.DISABLED, master=self.window)\
                    .grid(row=iStudent+2, column=self.nb_topic+3)
            # else, make a full Student control button.
            else:
                StudentCheckbutton(iStudent,
                                self.bool_topic, self.bool_student, self.bool_single,
                                self.student_list, self.topic_list, self.data,
                                self.window)\
                    .grid(row=iStudent+2, column=self.nb_topic+3)

    #######################################################
    def display_topics(self):
        """
        Display the top and bottom parts of the selection interface (topics).
        """

        # Fill the top and bot zones with topic labels and master checkboxes.
        for iTopic in range(self.nb_topic):
            # draw the top label.
            tk.Label(self.window, text=self.topic_list[iTopic])\
                .grid(row=0, column=iTopic+2)

            # if there is no topic (empty column header), disable the top and 
            # bottom buttons
            if self.topic_list[iTopic] == "":
                tk.Checkbutton(state=tk.DISABLED, master=self.window)\
                    .grid(row=1, column=iTopic+2)
                tk.Checkbutton(state=tk.DISABLED, master=self.window)\
                    .grid(row=self.nb_student+2, column=iTopic+2)

            # else, make the full topic control top and bottom buttons
            else:
                TopicCheckbutton(iTopic,
                                self.bool_topic, self.bool_student, self.bool_single,
                                self.student_list, self.topic_list, self.data,
                                self.window)\
                    .grid(row=1, column=iTopic+2)
                TopicCheckbutton(iTopic,
                                self.bool_topic, self.bool_student, self.bool_single,
                                self.student_list, self.topic_list, self.data,
                                self.window)\
                    .grid(row=self.nb_student+2, column=iTopic+2)

            # draw the bottom label.
            tk.Label(self.window, text=self.topic_list[iTopic])\
                .grid(row=self.nb_student+3, column=iTopic+2)

    #######################################################
    def display_single(self):
        """
        Display the core of the selection grid.
        """

        # Fill the center zone with the array of checkboxes.
        for iStudent in range(self.nb_student):
            for iTopic in range(self.nb_topic):
                # if there are no student or topic header, or the cell is not
                # filled, the cell should not be clickable.
                if self.student_list[iStudent] == ""\
                or self.topic_list[iTopic] == ""\
                or self.data[iStudent+4][iTopic+3] == "":
                    tk.Checkbutton(state=tk.DISABLED, master=self.window)\
                        .grid(row=iStudent+2, column=iTopic+2)
                # otherwise, put a single button
                else:
                    SingleCheckbutton(iTopic, iStudent,
                                    self.bool_topic, self.bool_student, self.bool_single,
                                    self.student_list, self.topic_list, self.data,
                                    self.window)\
                        .grid(row=iStudent+2, column=iTopic+2)

    #######################################################
    def display_aux(self):
        """
        Display auxiliary buttons (All, Reset, Valid, Abort).
        """

        # select_all button: top right
        tk.Button(self.window, text="ALL", command=self.select_all)\
            .grid(row=0, column=self.nb_topic+2, rowspan=2, columnspan=2)
        # reset button: top left
        tk.Button(self.window, text="Reset", command=self.reset)\
            .grid(row=0, column=0, rowspan=2, columnspan=2)
        # validate_button: bottom right
        tk.Button(self.window, text="Validate", command=self.window.quit)\
            .grid(row=self.nb_student+2, column=self.nb_topic+2, rowspan=2, columnspan=2)
        # abort_button: bottom left
        tk.Button(self.window, text="Abort", command=self.abort)\
            .grid(row=self.nb_student+2, column=0, rowspan=2, columnspan=2)


    #######################################################
    def select_all(self):
        for iStudent in range(self.nb_student):
            for iTopic in range(self.nb_topic):
                self.bool_single[iStudent][iTopic].set(True)
        for iStudent in range(self.nb_student):
            self.bool_student[iStudent].set(True)
        for iTopic in range(self.nb_topic):
            self.bool_topic[iTopic].set(True)

    def reset(self):
        for iStudent in range(self.nb_student):
            for iTopic in range(self.nb_topic):
                self.bool_single[iStudent][iTopic].set(False)
        for iStudent in range(self.nb_student):
            self.bool_student[iStudent].set(False)
        for iTopic in range(self.nb_topic):
            self.bool_topic[iTopic].set(False)

    def abort(self):
        self.reset()
        self.window.quit()

    def get_selection(self):
        return self.bool_topic, self.bool_student, self.bool_single


def to_std_1Darray(bool_list):
    """
    Convert a 1D array of Tkinter.BooleanVar into a 1D array of int.
    ---------------
    :param bool_single: 1D array of BooleanVar
    :return: 1D array of int
    """
    return [1 if b.get() else 0 for b in bool_list]


def to_std_2Darray(bool_single):
    """
    Convert a 2D array of Tkinter.BooleanVar into a 2D array of int.
    ---------------
    :param bool_single: 2D array of BooleanVar
    :return: 2D array of int
    """
    return [to_std_1Darray(b_list) for b_list in bool_single]


def print_BooleanVar_map(bool_topic, bool_student, bool_single):
    """
    Debug function to print the values in the arrays containing the boolean
    variables.
    ---------------
    :param bool_topic: array of the boolean for topic masters
    :param bool_student: array of the booleans for student masters
    :param bool_single: array 2D of the booleans for single.
    """
    print '  [',
    for iTopic in range(len(bool_topic)):
        print 1 if bool_topic[iTopic].get() else 0, ',',
    print ']'
    for iStudent in range(len(bool_student)):
        print 1 if bool_student[iStudent].get() else 0, '[',
        for iTopic in range(len(bool_topic)):
            print 1 if bool_single[iStudent][iTopic].get() else 0, ',',
        print ']'


if __name__ == '__main__':
    this_topic_list = ["Topic1", "", "Topic2", "Topic3", "Topic4"]
    this_student_list = ['A', 'B', '', 'E', 'C', 'D']
    this_data = [
		["Name","Surname","mail","Topic1","","Topic2","Topic3","Topic4",""],
		["Mean","","","25","","26","28","29","30"],
		["Highest","","","49","","50","52","53","54"],
		["Lowest","","","1","","2","4","5","6"],
		["A","a","a.a@a.a","1","","2","4","5","6"],
		["B","b","b.b@b.b","17","","18","20","21","22"],
		["","","","","","","","",""],
		["E","e","e.e@e.e","18","","23","39","14","23"],
		["C","c","c.c@c.c","33","","","36","37",""],
		["D","d","","49","","50","52","53","54"]
    ]

    selection_interface = SelectionInterface(this_data, this_topic_list, this_student_list)
    bool_topic, bool_student, bool_array = selection_interface.get_selection()

    sys.exit(0)
