import rooms.cell as cell
import parse
import state

print('\nPrison Escape!')
print('Copyright (c) 2018, 2019 Justin Diament and Gustav Hansen. All rights reserved.')
print('Licensed to CSE, High Technology High School.')
print('Revision 0.1 / Serial number 8675309 \n')

print('Slam! A guard slams your cell door shut. Welcome to Yodok Concentration Camp, Pyongyang, North Korea. \nIt\'s going to be a long 300 years or until death, whichever comes last. Or perhaps they will execute you quickly. Who knows.')
print('You face the back wall of the cell. An undersized cot is to your left, on the ground. A moderatly large painting picture of Kim Jong Un is on the wall in front of you. ')
print('On the wall to the right is a weekly schedule, written in English. Below that on the floor is are bowls of food and water. The floor is well-packed dirt.')

while not state.state['dead']:
    obj = parse.parse_input(input('> '))
    if state.state['location'] == 'cell':
        print(cell.cell_options[obj['action']](obj))