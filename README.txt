Project to automatically send marks to students from a summary in a .csv file.

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

TODO: still have to implement the actual mail sending.

TODO: behaviour of ABORT button in SelectionInterface (quit all the program) ?
    (care with its docstring then)

TODO: warning if no mail.

TODO: correct docstrings.
TODO: merge and rename build_list_dic (alone in its file).


