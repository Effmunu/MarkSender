#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Define the CheckButton classes inherited from Tkinter.Checkbutton.
Needed to add the position as an attribute to able the on_click function.

There is an boolean 2D array for selecting separately each topic for each 
student (bool_single), a boolean 1D array to select all topic for a given student
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

###########################################################
class CommonCheckbutton(tk.Checkbutton):
    """
    Interface implementing common methods for check buttons.
    """
    def __init__(self,
                bool_topic, bool_student, bool_single,
                student_list, topic_list, data,
                master=None, **kwargs):
        """
        Common check button for global topic selector.
        ---------------
        :param topic: topic number
        :param bool_topic: array of the topic booleans
        :param bool_student: array of the student booleans
        :param bool_single: array of the single booleans
        :param data: data array, needed to check for empty cells
        :param master: see Tkinter.Checkbutton
        """

        tk.Checkbutton.__init__(self, master, kwargs)

        self.bool_topic = bool_topic
        self.bool_student = bool_student
        self.bool_single = bool_single
        self.student_list = student_list
        self.topic_list = topic_list
        self.data = data

    def topic_is_complete(self, topic):
        """
        Check if the topic column is complete.
        We consider empty cells (no mark) and empty lines (no header) as ticked.
        ---------------
        :return: True if complete, else False
        """

        student = 0
        while student < len(self.bool_student) and (\
                self.bool_single[student][topic].get()\
                or self.student_list[student] == ""\
                or self.data[student+4][topic+3] == ""):
            student += 1
        return student >= len(self.bool_student)

    def student_is_complete(self, student):
        """
        Check if the student line is complete.
        We consider empty cells (no mark) and empty columns (no header) as ticked.
        ---------------
        :return: True if complete, else False
        """

        topic = 0
        while topic < len(self.bool_topic) and(\
                self.bool_single[student][topic].get()\
                or self.topic_list[topic] == ""\
                or self.data[student+4][topic+3] == ""):
            topic += 1
        return topic >= len(self.bool_topic)


###########################################################
class TopicCheckbutton(CommonCheckbutton):
    """
    Check button for selecting a whole topic
    """
    def __init__(self, topic,
                bool_topic, bool_student, bool_single,
                student_list, topic_list, data,
                master=None):
        """
        Check button for global topic selector
        :param topic: topic number
        others: see CommonCheckbutton
        """

        CommonCheckbutton.__init__(self,
            bool_topic, bool_student, bool_single,
            student_list, topic_list, data,
            master, variable=bool_topic[topic], command=self.on_click)
        self.topic = topic

    def on_click(self):
        """
        Action to execute when the button is clicked
        """

        # if we untick a whole topic
        if not self.bool_topic[self.topic].get():
            for student in range(len(self.bool_student)):
                if self.student_list[student] == "":
                    # if the student line is empty (actually has no header), do nothing
                    continue
                if self.data[student+4][self.topic+3] == "":
                    # if the cell is not filled, do nothing
                    continue
                # untick every box in the column
                self.bool_single[student][self.topic].set(False)
                # untick every student global selector
                self.bool_student[student].set(False)

        # if we tick a whole topic
        else:
            for student in range(len(self.bool_student)):
                if self.student_list[student] == "":
                    # if the student line is empty (actually has no header), do nothing
                    continue
                if self.data[student+4][self.topic+3] == "":
                    # if the cell is not filled, do nothing
                    continue
                # tick every box in the column
                self.bool_single[student][self.topic].set(True)
                # if the line is complete
                if self.student_is_complete(student):
                    # set student global selector to 1                                            
                    self.bool_student[student].set(True)                                          
                # else the student global selector should already be 0                            


###########################################################
class StudentCheckbutton(CommonCheckbutton):
    """
    Check button for selecting a whole student
    """
    def __init__(self, student,
                bool_topic, bool_student, bool_single,
                student_list, topic_list, data,
                master=None):
        """
        Check button for global topic selector
        :param student: student number
        others: see CommonCheckbutton
        """

        CommonCheckbutton.__init__(self,
            bool_topic, bool_student, bool_single,
            student_list, topic_list, data,
            master, variable=bool_student[student], command=self.on_click)
        self.student = student

    def on_click(self):
        """
        Action to execute when the button is clicked
        """

        # if we untick a whole student
        if not self.bool_student[self.student].get():
            for topic in range(len(self.bool_topic)):
                if self.topic_list[topic] == "":
                    # if the topic column is empty (actually has no header), do nothing
                    continue
                if self.data[self.student+4][topic+3] == "":
                    # if the cell is not filled, do nothing
                    continue
                # untick every box in the column
                self.bool_single[self.student][topic].set(False)
                # untick every topic global selector
                self.bool_topic[topic].set(False)

        # if we tick a whole student
        else:
            for topic in range(len(self.bool_topic)):
                if self.topic_list[topic] == "":
                    # if the topic column is empty (actually has no header), do nothing
                    continue
                if self.data[self.student+4][topic+3] == "":
                    # if the cell is not filled, do nothing
                    continue
                # tick every box in the column
                self.bool_single[self.student][topic].set(True)
                # if the line is complete
                if self.topic_is_complete(topic):
                    # set topic global selector to 1
                    self.bool_topic[topic].set(True)
                # else the topic global selector should already be 0


###########################################################
class SingleCheckbutton(CommonCheckbutton):
    """
    Check button for selecting a single topic/student pair
    """
    def __init__(self, topic, student,
                bool_topic, bool_student, bool_single,
                student_list, topic_list, data,
                master=None):
        """
        Check button for global topic selector
        :param topic: topic number
        :param student: student number
        others: see CommonCheckbutton
        """

        CommonCheckbutton.__init__(self,
            bool_topic, bool_student, bool_single,
            student_list, topic_list, data,
            master, variable=bool_single[student][topic], command=self.on_click)
        self.topic = topic
        self.student = student

    def on_click(self):
        """
        Action to execute when the button is clicked
        """

        # if we untick a single pair
        if not self.bool_single[self.student][self.topic].get():
            # untick corresponding topic global selector
            self.bool_topic[self.topic].set(False)
            # untick correponding student global selector
            self.bool_student[self.student].set(False)

        # if we tick a single pair, check if it completes a whole column or line;
        else:
            # completed the whole student line?
            if self.student_is_complete(self.student):
                # set student global selector to 1
                self.bool_student[self.student].set(True)
            # else the student global selector should already be 0

            # completed the whole topic column?
            if self.topic_is_complete(self.topic):
                # set topic global selector to True
                self.bool_topic[self.topic].set(True)
            # else the topic global selector should already be False

