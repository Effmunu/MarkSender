#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Mail utils for the send_mark project. Provides:
    build_body
    send_mail_fake: just for testing purpose for now, it's a dumb function.
Should provide build_header

:Author: NPAC 2015-2016
:Date: 20 Feb 2016
:Mail: antoine.laudrain[at]u-psud.fr
"""

def build_body(iStudent, topic_list, data, to_send_array):
    """
    Reminder of data structure:
    First  line: Name, Surname, Email, name of the topics...
    Second line: Mean values for each topic
    Third  line: Max values for each topic
    Fourth line: Min values for each topic
    Following lines: students data
    ---------------
    :param iStudent: line number of the student
    :param topic_list: list of the topics, in the order read in the csv file
    :param data: the full data table (list of list formatted csv file)
    :param to_send_array: std boolean array received after the gui
    :return: "" if nothing is to be sent (no registered mark or no topic
    selected). Message body otherwise.
    """
    msg = "Hello,\n"
    nb_topics_to_send = 0
    for iTopic in range(len(topic_list)):
        # if the topic has not been selected for this student
        if not to_send_array[iStudent][iTopic]:
            continue
        # if no mark was entered for this student at this topic
        if data[iStudent+4][iTopic+3] == '':
            continue
        nb_topics_to_send += 1
        line_buffer = "Your mark for %s is %s. Mean is %s, highest grade is %s, lowest grade is %s.\n" \
            % (topic_list[iTopic], \
            data[iStudent+4][iTopic+3], \
            data[1][iTopic+3], \
            data[2][iTopic+3], \
            data[3][iTopic+3])
        msg += line_buffer
    msg += "Have a good day,\n"
    msg += "Antoine Laudrain"

    # if no mark was registered in the database or no topic selected,
    # no need for sending a message.
    if nb_topics_to_send == 0:
        return ""
    # else, returns the message
    else:
        return msg


def send_mail_fake(mail_add, body):
    """
    Fake a mail sending: should be used in dry-runs.
    ---------------
    :param mail_add: mail adress of the receiver
    :param body: body of the mail
    """
    print "Mail will be sent to", mail_add, "with content :"
    print body
    print '-'*40

