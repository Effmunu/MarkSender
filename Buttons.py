#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Define the CheckButton classes inherited from Tkinter.Checkbutton.
Needed to add the position as an attribute to able the on_click function.

There is an boolean 2D array for selecting separately each topic for each 
student (bool_array), a boolean 1D array to select all topic for a given student
(bool_student), and a boolean 1D array to select all student for a given topic 
(bool_topic).

If a global student is ticked, it should tick every topic for this student,
and check if this has completed a whole topic. In that case, also tick the
global topic.
If a global topic is ticked, same with student <---> topic.

If a global student is unticked, it should untick every topic for this student,
and set every global topic to untick (since there is now at least one line 
unticked for every topic).
If a global topic is unticked, same with student <---> topic.

If a single student/topic box is ticked, it should check if this has completed
a whole student. In that case also tick the global student. Samingly for topic.

If a single student/topic box is unticked, also untick the corresponding global
student and topic.

:Author: NPAC 2015-2016
:Date: 11 Mar 2016
:Mail: antoine.laudrain[at]u-psud.fr
"""

import Tkinter as tk


class TopicCheckbutton(tk.Checkbutton):
    """
    Check button for selecting a whole topic
    """
    def __init__(self, topic, bool_topic, bool_student, bool_array, master=None):
        """
        Check button for global topic selector
        :param topic: topic number
        :param bool_topic: array of the topic booleans
        :param bool_student: array of the student booleans
        :param bool_array: array of the single booleans
        :param master: see Tkinter.Checkbutton
        """
        tk.Checkbutton.__init__(self, master, variable=bool_topic[topic], 
                                command=self.on_click)
        self.topic = topic
        self.bool_topic = bool_topic
        self.bool_student = bool_student
        self.bool_array = bool_array

    def on_click(self):
        """
        Action to execute when the button is clicked
        """
        student_nb = len(self.bool_student)
        topic_nb = len(self.bool_topic)

        if not self.bool_topic[self.topic].get():
            # if we untick a whole topic
            for student in range(student_nb):
                self.bool_array[student][self.topic].set(False)
                # untick every box in the column
                self.bool_student[student].set(False)
                # untick every student global selector
        else: # if we tick a whole topic
            for student in range(student_nb):
                self.bool_array[student][self.topic].set(True)
                # tick every box in the column
                topic = 0
                while topic < topic_nb and self.bool_array[student][topic].get():
                    topic +=1
                if topic >= topic_nb: # if the line is complete
                    self.bool_student[student].set(True)
                    # set student global selector to 1
                # else the student global selector should already be 0


class StudentCheckbutton(tk.Checkbutton):
    """
    Check button for selecting a whole student
    """
    def __init__(self, student, bool_topic, bool_student, bool_array, master=None):
        """
        Check button for global topic selector
        :param student: student number
        :param bool_topic: array of the topic booleans
        :param bool_student: array of the student booleans
        :param bool_array: array of the single booleans
        :param master: see Tkinter.Checkbutton
        """
        tk.Checkbutton.__init__(self, master, variable=bool_student[student], 
                                command=self.on_click)
        self.student = student
        self.bool_topic = bool_topic
        self.bool_student = bool_student
        self.bool_array = bool_array

    def on_click(self):
        """
        Action to execute when the button is clicked
        """
        student_nb = len(self.bool_student)
        topic_nb = len(self.bool_topic)

        if not self.bool_student[self.student].get(): # if we untick a whole student
            for topic in range(topic_nb):
                self.bool_array[self.student][topic].set(False)
                # untick every box in the column
                self.bool_topic[topic].set(False)
                # untick every topic global selector
        else: # if we tick a whole student
            for topic in range(topic_nb):
                self.bool_array[self.student][topic].set(True)
                # tick every box in the column
                student = 0
                while student < student_nb and self.bool_array[student][topic].get():
                    student +=1
                if student >= student_nb: # if the line is complete
                    self.bool_topic[topic].set(True) # set topic global selector to 1
                # else the topic global selector should already be 0


class SingleCheckbutton(tk.Checkbutton):
    """
    Check button for selecting a single topic/student pair
    """
    def __init__(self, topic, student, bool_topic, bool_student, bool_array, master=None):
        """
        Check button for global topic selector
        :param topic: topic number
        :param student: student number
        :param bool_topic: array of the topic booleans
        :param bool_student: array of the student booleans
        :param bool_array: array of the single booleans
        :param master: see Tkinter.Checkbutton
        :param options: see Tkinter.Checkbutton
        """
        tk.Checkbutton.__init__(self, master, variable=bool_array[student][topic], 
                                command=self.on_click)
        self.topic = topic
        self.student = student
        self.bool_topic = bool_topic
        self.bool_student = bool_student
        self.bool_array = bool_array

    def on_click(self):
        """
        Action to execute when the button is clicked
        """
        student_nb = len(self.bool_student)
        topic_nb = len(self.bool_topic)

        if not self.bool_array[self.student][self.topic].get():
            # if we untick a single pair
            self.bool_topic[self.topic].set(False)
            # untick corresponding topic global selector
            self.bool_student[self.student].set(False)
            # untick correponding student global selector
        else: # if we tick a single pair, check if it completes a column or line
            # completed the whole student line ?
            topic = 0
            while topic < topic_nb and self.bool_array[self.student][topic].get():
                topic +=1
            if topic >= topic_nb: # if the line is complete
                self.bool_student[self.student].set(True)
                # set student global selector to 1
            # else the student global selector should already be 0

            # completed the whole topic column ?
            student = 0
            while student < student_nb and self.bool_array[student][self.topic].get():
                student +=1
            if student >= student_nb: # if the line is complete
                self.bool_topic[self.topic].set(True)
                # set topic global selector to True
            # else the topic global selector should already be False

