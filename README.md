# EYUP
EYUP: the Yorkshire programming language and environment . Completed as part of my dissertation project at the University of Sheffield.

To see how to use the language and environment read the 'eyup_concepts' document. Note this is the edited version of the EYUP Concepts document provided by Dr Anthony Simons at the start of the project. The changes, additions and omissions are located at the end of the document and are of particular note.

## Running the system in its current version
Simply run the eyup.exe application to run the latest version of EYUP in your system's command prompt.

## Running the source code
    1) install python3 system  
    2) navigate to the eyup main directory and run the command: 'pip install -r requirements.txt'
    3) run the shell.py python file inside src to run the program with your changes saved

## Running the tests
While in the parent directory of tests (eyup) in the command line, run: *__'pytest --cov=src tests'__*

This should re-produce the tests, with the following coverage table:

| Name                | Stmts | Miss | Cover |
|---------------------|-------|------|-------|
| \src\__init__.py    | 9     | 0    | 100%  |
| \src\bodgers.py     | 123   | 1    | 99%   |
| \src\errors.py      | 52    | 0    | 100%  |
| \src\interpreter.py | 468   | 184  | 61%   |
| \src\nodes.py       | 235   | 64   | 73%   |
| \src\parse.py       | 592   | 142  | 76%   |
| \src\positions.py   | 15    | 0    | 100%  |
| \src\shell.py       | 64    | 43   | 33%   |
| \src\tokens.py      | 205   | 5    | 98%   |
| \src\values.py      | 734   | 188  | 74%   |
| __TOTAL__           | 2497  | 627  | 75%   |
