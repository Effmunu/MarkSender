Project to automatically send marks to students from a summary in a .csv file.
(And trying to learn about Git in the same time.)

The data should be stored in a CSV file which 3 first columns and 4 first lines
are reserved space (template given). All other columns are taken to be topics,
all other lines are taken to be students. The program can manage empty cells.
(Don't know if empty columns are considered as topic.)

Call the program with
    python main.py path/to/file.csv
Help available with
    ./main.py -h

============================================================
===== For developpers ======================================
============================================================
Please solve a TODO using a new branch, merge and then ask for a pull request.

TODO: maybe try to transform the gui function into a SelectionInterface class
TODO: behaviour of ABORT button in SelectionInterface (quit all the program) ?
    (care with its docstring then)

TODO: warning if no mail.
TODO: untickable button if unfilled cell. But considered as ticked for global
    ticking. This kind of empty tolumn should not be removed from the display:
    could be used to separate the topics if wanted (thin column in the
    display).
    -> buttons done, now have to modify the behaviour.

http://stackoverflow.com/questions/20687220/disable-checkbutton-tkinter-grey-out
http://stackoverflow.com/questions/3295270/overriding-tkinter-x-button-control-the-button-that-close-the-window

TODO: rename main into marksender
TODO: merge and rename build_list_dic (alone in its file).

