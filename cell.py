import collections
import parse

print('\nPrison Escape!')
print('Copyright (c) 2018, 2019 Justin Diament and Gustav Hansen. All rights reserved.')
print('Licensed to CSE, High Technology High School.')
print('Revision 0.1 / Serial number 8675309 \n')

print('Slam! A guard slams your cell door shut. Welcome to Yodok Concentration Camp, Pyongyang, North Korea. \nIt\'s going to be a long 300 years or until death, whichever comes last.')
print('You face the back wall of the cell. An undersized cot is to your left, on the ground. A moderatly large painting picture of Kim Jong Un is on the wall in front of you. ')
print('On the wall to the right is a weekly schedule, written in English. Below that on the floor is are bowls of food and water. The floor is well-packed dirt.')

state = {
    'day': 1,
    'inventory': [],
    'inventory_limit': 2,
    'last_day_eaten': 1,
    'dead': False
}

days = {
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday',
    0: 'Sunday'
}

################UTILITY FUNCTIONS################


def add_to_inventory(item):
    if len(state['inventory']) >= state['inventory_limit']:
        return "Sorry, but you are out of inventory space."
    else:
        state['inventory'].append(item)
        return "You now "


def quit():
    state['dead'] = True
    return "You have died of starvation."

################ACTION FUNCTIONS################


def increment_day(obj, num=1):
    state['day'] = state['day'] + num
    weekday = days[state['day'] % 7]
    out = "It is now %s day %d" % (weekday, state['day'])
    if state['day'] - state['last_day_eaten'] > 3:
        out += '\nYou are very hungry. You look at the kibble anxiously.'
    if state['day'] - state['last_day_eaten'] > 5:
        out += ('\n' + quit())
    return out


def dig_hole(obj):
    if 'spoon' not in state['inventory']:
        out = increment_day(90)
        out += '\n'
        out += "You've tried to dig hole. Three months later, no progress."
    else:
        out = increment_day(7)
        out += '\n'
        out += "You've found a GameBoy. Now you can be entertained in prison."
        state['inventory'].append("GameBoy")
    return out


def examine(obj):
    if obj['object'] == 'cot':
        return 'It looks like it might fit you if you were 4 foot 9. Too bad you weren\'t arrested at age 7. Lacks a pillow'
    if obj['object'] == 'painting':
        return 'Kim Jong Un is wearing a Supreme shirt and Gucci jacket. High quality craftsmanship. The painting is sadly the most valuble object in the cell. Not well secured to the wall though. Looks like it might fall off.'
    if obj['object'] == 'schedule':
        return 'Comic Sans font, size 13. \nMonday: Bathroom break - 20 min \nTuesday: Mess Hall - 1 hour \nWednsday: Bathroom break - 20 min \nThursday: Mess Hall - 1 hour \nFriday: Nothing \nSaturday: Recreation - 2 hours \nSunday: Recreaction - 2 hours'
    if obj['object'] == 'bowls':
        return 'Looks like dog kibble and apple juice. Better than nothing I suppose.'
    if obj['object'] == 'floor':
        return 'Cold and dusty. Looks hard to dig through.'
    if obj['object'] == 'door':
        return 'Barred and locked. Large keyhole on the outside of the door. On the other side of the hall is a dim lightbulb.'


def get_inventory(obj):
    out = 'You have:'
    for item, count in collections.Counter(state['inventory']).items():
        out += '\n' + count + ' ' + item
        if count > 1:
            out += 's'
    return out


def get(obj):
    if obj['object'] == 'inventory':
        get_inventory(obj)


def eat(obj):
    state['last_day_eaten'] = state['day']
    return 'You cautiously pick up the bowl of "food".\nYou examine it. It seems to be dog kibble. You question your life choices, and take a bite of the kibble.\n\nIt was exactly as bad as you thought it would be. You down it with some old apple juice.'


cell_options = {
    'sleep': increment_day,
    'dig': dig_hole,
    'examine': examine,
    'get': get,
    'eat': eat,
}

while not state['dead']:
    obj = parse.parse_input(input())
    print(cell_options[obj['action']](obj))