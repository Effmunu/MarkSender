#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Define the CheckButton classes inherited from Tkinter.Checkbutton.
Needed to add the position as an attribute to able the on_click function.

There is a boolean 2D array for selecting a single topic for a single student
(bool_single), a boolean 1D array to select all topic for a given student
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

Empty lines/columns (no header in the data array) or cells cannot be selected,
but are considered as filled when checking for line/column completeness.

:Author: NPAC 2015-2016
:Date: Created 20 Feb 2016 - Last update 12 Aug 2016
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
        :param bool_topic: array of the topic booleans
        :param bool_student: array of the student booleans
        :param bool_single: array of the single booleans (2D)
        :param student_list: list of the students as they should appear, needed
        to check for empty student headers
        :param topic_list: list of the topics as they should appear, needed to
        check for empty topic headers
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

    def topic_is_complete(self, iTopic):
        """
        Check if the topic column is complete.
        We consider empty cells (no mark) and empty lines (no header) as ticked.
        ---------------
        :param iTopic: topic index in the bool array to be checked
        :return: True if complete, else False
        """

        iStudent = 0
        while iStudent < len(self.bool_student) and (\
                self.bool_single[iStudent][iTopic].get()\
                or self.student_list[iStudent] == ""\
                or self.data[iStudent+4][iTopic+3] == ""):
            iStudent += 1
        return iStudent >= len(self.bool_student)

    def student_is_complete(self, iStudent):
        """
        Check if the student line is complete.
        We consider empty cells (no mark) and empty columns (no header) as ticked.
        ---------------
        :param iStudent: student index in the bool array to be checked
        :return: True if complete, else False
        """

        iTopic = 0
        while iTopic < len(self.bool_topic) and(\
                self.bool_single[iStudent][iTopic].get()\
                or self.topic_list[iTopic] == ""\
                or self.data[iStudent+4][iTopic+3] == ""):
            iTopic += 1
        return iTopic >= len(self.bool_topic)


###########################################################
class TopicCheckbutton(CommonCheckbutton):
    """
    Check button for selecting a whole topic.
    """

    def __init__(self, iTopic,
                bool_topic, bool_student, bool_single,
                student_list, topic_list, data,
                master=None):
        """
        Check button for global topic selector.
        ---------------
        :param iTopic: topic index in the bool array
        others: see CommonCheckbutton
        """

        CommonCheckbutton.__init__(self,
            bool_topic, bool_student, bool_single,
            student_list, topic_list, data,
            master, variable=bool_topic[iTopic], command=self.on_click)
        self.iTopic = iTopic

    def on_click(self):
        """
        Action to execute when the button is clicked.
        """

        # if we untick a whole topic
        if not self.bool_topic[self.iTopic].get():
            for iStudent in range(len(self.bool_student)):
                if self.student_list[iStudent] == "":
                    # if the student line is empty (actually has no header), do nothing
                    continue
                if self.data[iStudent+4][self.iTopic+3] == "":
                    # if the cell is not filled, do nothing
                    continue
                # untick every box in the column
                self.bool_single[iStudent][self.iTopic].set(False)
                # untick every student global selector
                self.bool_student[iStudent].set(False)

        # if we tick a whole topic
        else:
            for iStudent in range(len(self.bool_student)):
                if self.student_list[iStudent] == "":
                    # if the student line is empty (actually has no header), do nothing
                    continue
                if self.data[iStudent+4][self.iTopic+3] == "":
                    # if the cell is not filled, do nothing
                    continue
                # tick every box in the column
                self.bool_single[iStudent][self.iTopic].set(True)
                # if the line is complete
                if self.student_is_complete(iStudent):
                    # set student global selector to 1
                    self.bool_student[iStudent].set(True)
                # else the student global selector should already be 0


###########################################################
class StudentCheckbutton(CommonCheckbutton):
    """
    Check button for selecting a whole student.
    """

    def __init__(self, iStudent,
                bool_topic, bool_student, bool_single,
                student_list, topic_list, data,
                master=None):
        """
        Check button for global topic selector.
        ---------------
        :param iStudent: student index in the bool array
        others: see CommonCheckbutton
        """

        CommonCheckbutton.__init__(self,
            bool_topic, bool_student, bool_single,
            student_list, topic_list, data,
            master, variable=bool_student[iStudent], command=self.on_click)
        self.iStudent = iStudent

    def on_click(self):
        """
        Action to execute when the button is clicked.
        """

        # if we untick a whole student
        if not self.bool_student[self.iStudent].get():
            for iTopic in range(len(self.bool_topic)):
                if self.topic_list[iTopic] == "":
                    # if the topic column is empty (actually has no header), do nothing
                    continue
                if self.data[self.iStudent+4][iTopic+3] == "":
                    # if the cell is not filled, do nothing
                    continue
                # untick every box in the column
                self.bool_single[self.iStudent][iTopic].set(False)
                # untick every topic global selector
                self.bool_topic[iTopic].set(False)

        # if we tick a whole student
        else:
            for iTopic in range(len(self.bool_topic)):
                if self.topic_list[iTopic] == "":
                    # if the topic column is empty (actually has no header), do nothing
                    continue
                if self.data[self.iStudent+4][iTopic+3] == "":
                    # if the cell is not filled, do nothing
                    continue
                # tick every box in the column
                self.bool_single[self.iStudent][iTopic].set(True)
                # if the line is complete
                if self.topic_is_complete(iTopic):
                    # set topic global selector to 1
                    self.bool_topic[iTopic].set(True)
                # else the topic global selector should already be 0


###########################################################
class SingleCheckbutton(CommonCheckbutton):
    """
    Check button for selecting a single topic/student pair.
    """

    def __init__(self, iTopic, iStudent,
                bool_topic, bool_student, bool_single,
                student_list, topic_list, data,
                master=None):
        """
        Check button for global topic selector.
        ---------------
        :param iTopic: topic index in the bool array
        :param iStudent: student index in the bool array
        others: see CommonCheckbutton
        """

        CommonCheckbutton.__init__(self,
            bool_topic, bool_student, bool_single,
            student_list, topic_list, data,
            master, variable=bool_single[iStudent][iTopic], command=self.on_click)
        self.iTopic = iTopic
        self.iStudent = iStudent

    def on_click(self):
        """
        Action to execute when the button is clicked.
        """

        # if we untick a single pair
        if not self.bool_single[self.iStudent][self.iTopic].get():
            # untick corresponding topic global selector
            self.bool_topic[self.iTopic].set(False)
            # untick correponding student global selector
            self.bool_student[self.iStudent].set(False)

        # if we tick a single pair, check if it completes a whole column or line;
        else:
            # completed the whole student line?
            if self.student_is_complete(self.iStudent):
                # set student global selector to 1
                self.bool_student[self.iStudent].set(True)
            # else the student global selector should already be 0

            # completed the whole topic column?
            if self.topic_is_complete(self.iTopic):
                # set topic global selector to True
                self.bool_topic[self.iTopic].set(True)
            # else the topic global selector should already be False

