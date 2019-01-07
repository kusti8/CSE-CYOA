import collections
import state

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
    if len(state.state['inventory']) >= state.state['inventory_limit']:
        return "Sorry, but you are out of inventory space."
    else:
        state.state['inventory'].append(item)
        return "You now have " + item

def remove_from_inventory(item):
    if item in state.state['inventory']:
        state.state['inventory'].remove(item)
        return "You have removed " + item + " from your inventory." 


def quit():
    state.state['dead'] = True
    return "\nYou have died."
    
def get_weekday(day_num):
    return days[day_num % 7]

################ACTION FUNCTIONS################

def every_turn(obj):
    out = ''
    if 'A very special painting' in state.state['inventory']:
        out += '\nA guard notices you have removed and disrespected the painting of His Greatness Kim Jong Un. You are killed immediately. \n\n'
        out += quit()
    if state.state['day'] > 30:
        out += '\nIt is the 30th day. You are executed by North Korea.'
        out += quit()
    elif state.state['day'] > 20:
        state.state['execution_posted'] = True
        out += '\nYour execution date has been posted on the wall. It is in 10 days. A shiver runs down your spine as you see it. Time is running out.'
    if state.state['bowl_flipped'] and get_weekday(state.state['day']) == 'Thursday':
      out += '\nA man walked by your cell and whispers something:\n\t'
      out += 'An item, you need. Go through the ground, you must.'
    return out

def increment_day(obj, num=1):
    state.state['day'] = state.state['day'] + num
    weekday = get_weekday(state.state['day'])
    out = "It is now %s day %d." % (weekday, state.state['day'])
    
    if state.state['day'] - state.state['last_day_eaten'] > 4:
        out += '\nYou are very hungry. You look at the kibble anxiously.'
    if state.state['day'] - state.state['last_day_eaten'] > 9:
        out += ('\n' + quit())
    
    out += every_turn(obj)

    return out


def dig_hole(obj):
    if 'spoon' not in state.state['inventory']:
        response = input('Are you sure you want to do this? It is estimated to take around 3 months? [yn]')
        if response.lower() != 'y':
            return ''
        state.state['last_day_eaten'] = state.state['day']+90
        out = increment_day(obj,90)
        out += '\n'
    else:
        state.state['last_day_eaten'] = state.state['day']+7
        out = increment_day(obj,7)
        out += '\n'
        out += "You've found a GameBoy. Now you can be entertained in prison."
        state.state['inventory'].append("GameBoy")
    return out


def examine(obj):
    if obj['object'] == 'cot':
        return 'It looks like it might fit you if you were 4 foot 9. Too bad you weren\'t arrested at age 7. Lacks a pillow'
    if obj['object'] == 'A very special painting':
        return 'Kim Jong Un is wearing a Supreme shirt and Gucci jacket. High quality craftsmanship. The painting is sadly the most valuble object in the cell. Not well secured to the wall though. Looks like it might fall off.'
    if obj['object'] == 'schedule':
        return 'Comic Sans font, size 13. \nMonday: Bathroom break - 20 min \nTuesday: Mess Hall - 1 hour \nWednsday: Bathroom break - 20 min \nThursday: Mess Hall - 1 hour \nFriday: Nothing \nSaturday: Recreation - 2 hours \nSunday: Recreaction - 2 hours'
    if obj['object'] == 'bowls':
        return 'Looks like dog kibble and apple juice. Better than nothing I suppose.'
    if obj['object'] == 'floor':
        return 'Cold and dusty. Looks hard to dig through.'
    if obj['object'] == 'door':
        return 'Barred and locked. Large keyhole on the outside of the door. On the other side of the hall is a dim lightbulb.'
    if obj['object'] == 'note' and state.state['painting_got']:
        return "If you want some help, make sure your food bowl is upside down on Thursday and I'll see.\nYou also better put back that painting or else they\'ll kill you for disrespecting Kim. -Yoda"


def get_inventory(obj):
    out = 'You have:'
    for item, count in collections.Counter(state.state['inventory']).items():
        out += '\n' + str(count) + ' ' + item
        if count > 1:
            out += 's'
    return out

def move_painting(obj):
    if obj['object'] == 'A very special painting':
        return get_painting(obj)

def get_painting(obj):
    out = add_to_inventory('A very special painting')
    state.state['painting_got'] = True
    out += '\nThere seems to be a note on the wall.'
    return out

def get(obj):
    if obj['object'] == 'inventory':
        return get_inventory(obj)
    elif obj['object'] == 'A very special painting':
        return get_painting(obj)

def flip(obj):
  if obj['object'] == 'bowl':
    state.state['bowl_flipped'] = True
    return 'You flipped the bowl. Now all you have to do is wait until Thursday.'

def eat(obj):
    state.state['last_day_eaten'] = state.state['day']
    return 'You cautiously pick up the bowl of "food".\nYou examine it. It seems to be dog kibble. You question your life choices, and take a bite of the kibble.\n\nIt was exactly as bad as you thought it would be. You down it with some old apple juice.'

def remove(obj):
    return remove_from_inventory(obj['object'])

def open_item(obj):
    if obj['object'] == 'door':
        return "Cannot open the door. It is locked"

cell_options = {
    'sleep': increment_day,
    'dig': dig_hole,
    'examine': examine,
    'get': get,
    'eat': eat,
    'move': move_painting,
    'remove': remove,
    'flip': flip,
    'open': open_item
}