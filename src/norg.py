#!/usr/bin/python
""" norg.py

NORG is a python script designed to help my god forsaken note organization skills. Hopefully with this in my life, my life improves at least 1% better.


Author: jmoon

"""

from time import gmtime, strftime

import argparse
import os
import subprocess
import sys

ARG_MSG_DESCRIPTION = 'NORG is a Note ORGanizer'
DEFAULT_NOTE_NAME = 'notes_{date}.md'.format(date=strftime('%b-%d-%H%M%S'))

BROWSER = 'google-chrome-stable'
NORG_PATH = os.path.realpath(__file__)
USER_TEMPLATE_PATH = os.path.dirname(NORG_PATH) + '/user_template.md'

def newNote(args):
    note_name = args.n or DEFAULT_NOTE_NAME
    note_template = readUserTemplate(args.t or USER_TEMPLATE_PATH)
    note_template = note_template.replace("DATE", strftime('%b, %d. %Y'))

    with open(note_name, "w+") as new_note_file:
        new_note_file.write(note_template)
    new_note_file.close()

    print(f'{note_name} has been created')

def compileNote(args):
    print('Not implemented yet')
    pass

def openNote(args):
    print(f'Opening {args.n}')
    return subprocess.call([BROWSER, args.n])

def readUserTemplate(path=USER_TEMPLATE_PATH):
    try:
        with open(USER_TEMPLATE_PATH, "r") as user_template_file:
            user_template = user_template_file.read()
        user_template_file.close()
        return user_template
    except FilenotFoundError:
        print('User template does not exist.')
        sys.exit(1)

def main():
    # namespace issue with argparse
    # append help automatically to avoid the error
    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    # Create Argument Parser
    parser = argparse.ArgumentParser(
            prog='norg',
            description=ARG_MSG_DESCRIPTION)
    subparsers = parser.add_subparsers(
            help='commands')

    # Subparser for create new note
    parser_new = subparsers.add_parser('new', help='Create a new note')
    parser_new.add_argument('-t', type=str, help='Specify path to custom template')
    parser_new.add_argument('-n', type=str, help='The name of the new note')
    parser_new.set_defaults(func=newNote)

    # Subparser for compile note into pdf format
    parser_compile = subparsers.add_parser('compile', help='Compile note into pdf format')
    parser_compile.add_argument('-p', type=str, help='Specify the absolute path to the note')
    parser_compile.set_defaults(func=compileNote)

    # Subparser for open note in markdown format on browser
    parser_open = subparsers.add_parser('open', help='Open note on the markdown browser')
    parser_open.add_argument('-n', type=str, help='Specify the note to open')
    parser_open.set_defaults(func=openNote)

    # parse the arguments
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
