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
    def __init__(self, topic, bool_topic, bool_student, bool_array, student_list, topic_list, data, master=None):
        """
        Check button for global topic selector
        :param topic: topic number
        :param bool_topic: array of the topic booleans
        :param bool_student: array of the student booleans
        :param bool_array: array of the single booleans
        :param data: data array, needed to check for empty cells
        :param master: see Tkinter.Checkbutton
        """
        tk.Checkbutton.__init__(self, master, variable=bool_topic[topic], 
                                command=self.on_click)
        self.topic = topic
        self.bool_topic = bool_topic
        self.bool_student = bool_student
        self.bool_array = bool_array
        self.student_list = student_list
        self.topic_list = topic_list
        self.data = data

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
                self.bool_array[student][self.topic].set(False)
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
                self.bool_array[student][self.topic].set(True)
                # if the line is complete
                if line_is_complete():                                                            
                    # set student global selector to 1                                            
                    self.bool_student[student].set(True)                                          
                # else the student global selector should already be 0                            
        
    def line_is_complete(self):
        """
        Check if the student line is complete.                                                    
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


class StudentCheckbutton(tk.Checkbutton):
    """
    Check button for selecting a whole student
    """
    def __init__(self, student, bool_topic, bool_student, bool_array, student_list, topic_list, data, master=None):
        """
        Check button for global topic selector
        :param student: student number
        :param bool_topic: array of the topic booleans
        :param bool_student: array of the student booleans
        :param bool_array: array of the single booleans
        :param data: data array, needed to check for empty cells
        :param master: see Tkinter.Checkbutton
        """
        tk.Checkbutton.__init__(self, master, variable=bool_student[student], 
                                command=self.on_click)
        self.student = student
        self.bool_topic = bool_topic
        self.bool_student = bool_student
        self.bool_array = bool_array
        self.student_list = student_list
        self.topic_list = topic_list
        self.data = data

    def on_click(self):
        """
        Action to execute when the button is clicked
        """
        student_nb = len(self.bool_student)
        topic_nb = len(self.bool_topic)

        # if we untick a whole student
        if not self.bool_student[self.student].get():
            for topic in range(topic_nb):
                if self.topic_list[topic] == "":
                    # if the topic column is empty (actually has no header), do nothing
                    continue
                if self.data[self.student+4][topic+3] == "":
                    # if the cell is not filled, do nothing
                    continue
                # untick every box in the column
                self.bool_array[self.student][topic].set(False)
                # untick every topic global selector
                self.bool_topic[topic].set(False)
        # if we tick a whole student
        else:
            for topic in range(topic_nb):
                if self.topic_list[topic] == "":
                    # if the topic column is empty (actually has no header), do nothing
                    continue
                if self.data[self.student+4][topic+3] == "":
                    # if the cell is not filled, do nothing
                    continue
                # tick every box in the column
                self.bool_array[self.student][topic].set(True)
                # if the line is complete
                if column_is_complete():
                    # set topic global selector to 1
                    self.bool_topic[topic].set(True)
                # else the topic global selector should already be 0

    def column_is_complete(self):
        """
        Check if the topic column is complete.                                                    
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


class SingleCheckbutton(tk.Checkbutton):
    """
    Check button for selecting a single topic/student pair
    """
    def __init__(self, topic, student, bool_topic, bool_student, bool_array, student_list, topic_list, data, master=None):
        """
        Check button for global topic selector
        :param topic: topic number
        :param student: student number
        :param bool_topic: array of the topic booleans
        :param bool_student: array of the student booleans
        :param bool_array: array of the single booleans
        :param data: data array, needed to check for empty cells
        :param master: see Tkinter.Checkbutton
        """
        tk.Checkbutton.__init__(self, master, variable=bool_array[student][topic], 
                                command=self.on_click)
        self.topic = topic
        self.student = student
        self.bool_topic = bool_topic
        self.bool_student = bool_student
        self.bool_array = bool_array
        self.student_list = student_list
        self.topic_list = topic_list
        self.data = data

    def on_click(self):
        """
        Action to execute when the button is clicked
        """
        student_nb = len(self.bool_student)
        topic_nb = len(self.bool_topic)

        # if we untick a single pair
        if not self.bool_array[self.student][self.topic].get():
            # untick corresponding topic global selector
            self.bool_topic[self.topic].set(False)
            # untick correponding student global selector
            self.bool_student[self.student].set(False)
        # if we tick a single pair, check if it completes a whole column or line;
        # we consider empty cells and columns/lines without headers as ticked
        else:
            # completed the whole student line?
            topic = 0
            while topic < topic_nb and (self.bool_array[self.student][topic].get()\
                                        or self.topic_list[topic] == ""\
                                        or self.data[self.student+4][topic+3] == ""):
                topic +=1
            # if the line is complete
            if topic >= topic_nb:
                # set student global selector to 1
                self.bool_student[self.student].set(True)
            # else the student global selector should already be 0

            # completed the whole topic column?
            student = 0
            while student < student_nb and (self.bool_array[student][self.topic].get()\
                                            or self.student_list[student] == ""\
                                            or self.data[student+4][self.topic+3] == ""):
                student +=1
            # if the line is complete
            if student >= student_nb:
                # set topic global selector to True
                self.bool_topic[self.topic].set(True)
            # else the topic global selector should already be False

