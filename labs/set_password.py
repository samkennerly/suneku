#!/usr/env/python
'''
Edit Jupyter config file to use a password.
Path to config file should be first command-line argument to this script.
Password should be stored in your ~/suneku/.env file.
'''
from notebook.auth import passwd
import sys
import os

PASSWORD_PARAM          = 'c.NotebookApp.password'
ENABLE_PASSWORD_PARAM   = 'c.NotebookApp.password_required'


def replace_line(line,param,value):
    line_start = param + ' = '
    if line.strip('#').strip().startswith(line_start):
        return "%s = %s\n" % (param,value)
    else:
        return line

def change_text(text,param,value):
    replace = lambda line: replace_line(line,param,value)
    return [ replace(line) for line in text ]

def main(config_file,password):

    print( "Reading", config_file )
    with open(config_file,'r') as f:
        text = f.readlines()

    print( "Salting and hashing password" )
    salted_hashed_quoted = "'%s'" % passwd(str(password))

    print( "Editing", config_file )
    text = change_text(text,PASSWORD_PARAM,salted_hashed_quoted)
    text = change_text(text,ENABLE_PASSWORD_PARAM,True)

    print( "Overwriting", config_file )
    with open(config_file,'w') as f:
        f.writelines(text)


if __name__ == '__main__':

    # Get path to Jupyter config file
    assert len(sys.argv) > 0, "Need name of Jupyter config file as first argument!"
    config_file = sys.argv[1]

    # Get password from environment
    password = os.environ.get('JUPYTER_PASSWORD')
    assert password is not None, "Need to set JUPYTER_PASSWORD in ~/suneku/.env file!"

    # Edit password settings in the Jupyter config file
    main(config_file,password)