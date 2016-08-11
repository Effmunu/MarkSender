Project to automatically send marks to students from a summary in a .csv file.
(And trying to learn about Git in the same time.)

The data should be stored in a CSV file which 3 first columns and 4 first lines
are reserved space (template given). All other columns are taken to be topics,
all other lines are taken to be students. The program can manage empty cells.
(Don't know if empty columns are considered as topic.)

Call the program with
    python main.py path/to/file.csv

============================================================
===== For developpers ======================================
============================================================
Please solve a TODO using a new branch, merge and then ask for a pull request.

TODO: maybe try to transform the gui function into a SelectionInterface class
TODO: the dictionary building part in 'retrieve_marks' could be removed.
    (I prefered to keep it even if not used, but it could be retrieved from
    previous commits).
TODO: The function actually sending the mail is still to be done.
    But there is a function printing the mail instead of writting them
    (dry-run).
TODO: option for dry-run (parser in main ?)
TODO: option for sorting topics (-t/--sort-topics) and students
    (-s/--sort-students).
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

