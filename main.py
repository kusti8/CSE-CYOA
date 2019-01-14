import rooms.cell as cell
import rooms.messhall as messhall
import rooms.bathroom as bathroom
import rooms.recreation as recreation
import rooms.corridor as corridor
import parse
import state
import common_actions
from time import sleep
import sys

def printf(s):
    if s:
        for char in s:
            print(char, end='')
            sys.stdout.flush()
            #sleep(0.02)
        print()

printf('\nPrison Escape!')
printf('Copyright (c) 2018, 2019 Justin Diament and Gustav Hansen. All rights reserved.')
printf('Licensed to CSE, High Technology High School.')
printf('Revision 1.0 / Serial number 8675309 \n')

printf('Slam! A guard slams your cell door shut. Welcome to Yodok Concentration Camp, Pyongyang, North Korea. \nIt\'s going to be a long 300 years or until death, whichever comes last. Or perhaps they will execute you quickly. Who knows.')
printf('You face the back wall of the cell. An undersized cot is to your left, on the ground. A moderatly large painting picture of Kim Jong Un is on the wall in front of you. ')
printf('On the wall to the right is a weekly schedule, written in English. Below that on the floor is are bowls of food and water. The floor is well-packed dirt.')

def cell_options(obj):
    if state.state['location'] == 'cell':
        printf(cell.cell_options[obj['action']](obj))
    elif state.state['location'] == 'messhall':
        printf(messhall.messhall_options[obj['action']](obj))
    elif state.state['location'] == 'bathroom':
        printf(bathroom.bathroom_options[obj['action']](obj))
    elif state.state['location'] == 'recreation':
        printf(recreation.recreation_options[obj['action']](obj))
    elif state.state['location'] == 'corridor':
        printf(corridor.corridor_options[obj['action']](obj))
    

while not state.state['dead']:
    i = input('> ')
    if i:
        obj = parse.parse_input(i)
        if not obj['object'] or not obj['action']:
            printf("Unknown command.")
        try:
            if obj['action'] in common_actions.common_options.keys():
                result = common_actions.common_options[obj['action']](obj)
                if not result:
                    cell_options(obj)
                else:
                    printf(result)
            else:
                cell_options(obj)
        except KeyError:
            if obj['action']:
                printf("Unknown command.")