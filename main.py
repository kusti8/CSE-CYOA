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
#import all other code files for use in returning results of player commands

def printf(s): #modify print() to have "typewriter" effect 
    if s:
        for char in s:
            print(char, end='')
            sys.stdout.flush()
            sleep(0.02)
        print()
    else: #print 'you cannot do that' if a function returns a blank string
        printf("You cannot do that.")

printf('\nPrison Escape!') 
printf('Copyright (c) 2018, 2019 Justin Diament and Gustav Hansen. All rights reserved.')
printf('Licensed to CSE, High Technology High School.')
printf('Revision 1.2 / Serial number 8675309 \n')
#print technical information

printf('Slam! A guard slams your cell door shut. Welcome to Yodok Concentration Camp, Pyongyang, North Korea. \nIt\'s going to be a long 300 years or until death, whichever comes last. Or perhaps they will execute you quickly. Who knows.')
printf('You face the back wall of the cell. An undersized cot is to your right, on the ground. A moderatly large painting picture of Kim Jong Un is on the wall in front of you. ')
printf('Below the wall the left is a weekly schedule, written in English. Next to that on the floor are bowls of food and water. The floor is well-packed dirt.')
printf("\nTo play, simply type in phrases, starting with a verb and ending with a noun (like 'read schedule'). The hard part is figuring out what are the right commands.")
#print an introduction that tells the player the beginning of the game's storyline 

def cell_options(obj): #determines which file to look through for command results based on player location in-game
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
    

while not state.state['dead']: #while the player is still alive (ends the game if dead is set to True)
    i = input('> ')
    if i:
        obj = parse.parse_input(i) #sends input to the parser to check for commands that mean the same thing
        if not obj['object'] or not obj['action']:
            printf("You cannot do that.") #print 'you cannot do that' if what they enter is not a valid command
        try: 
            if obj['action'] in common_actions.common_options.keys(): 
                result = common_actions.common_options[obj['action']](obj)
                if not result:
                    cell_options(obj)
                else:
                    printf(result)
                #looks through possible command results in the code file for the room the player is in as well as 
                #common actions to find if their command has a result
            else:
                cell_options(obj)
        except KeyError:
            if obj['action']: #print 'you cannot do that' if an error occurs based on a command entered by the player
                printf("You cannot do that.")