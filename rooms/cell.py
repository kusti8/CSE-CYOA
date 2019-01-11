import collections
import state
import rooms.messhall
import rooms.bathroom
import rooms.recreation
import common_actions

################ACTION FUNCTIONS################

def every_turn_cell():
    out = ''
    if 'A very special painting' in state.state['inventory']:
        out += '\nA guard notices you have removed and disrespected the painting of His Greatness Kim Jong Un. You are killed immediately. \n\n'
        out += common_actions.game_quit()
    if state.state['bowl_flipped'] and common_actions.get_weekday(state.state['day']) == 'Friday':
      out += '\nA man walked by your cell and whispers something:\n\t'
      out += 'An item, you need. Go through the ground, you must.'
    if common_actions.get_weekday(state.state['day']) == 'Tuesday' or common_actions.get_weekday(state.state['day']) == 'Thursday':
        state.state['location'] = 'messhall'
        out += '\nA guard comes to your cell and brings you to the mess hall.'
        out += rooms.messhall.welcome()
    if common_actions.get_weekday(state.state['day']) == 'Monday' or common_actions.get_weekday(state.state['day']) == 'Wednesday':
        state.state['location'] = 'bathroom'
        out += '\nA guard comes to your cell and brings you to the bathroom.'
        out += rooms.bathroom.welcome()
    if common_actions.get_weekday(state.state['day']) == 'Saturday' or common_actions.get_weekday(state.state['day']) == 'Sunday':
        state.state['location'] = 'recreation'
        out += '\nA guard comes to your cell and brings you to recreation.'
        out += rooms.recreation.welcome()
    return out


def dig_hole(obj):
    if 'spoon' not in state.state['inventory']:
        response = input('Are you sure you want to do this? It is estimated to take around 3 months? Which is it: (yes) or (no)?')
        if response.lower() != 'y' and response.lower() != 'yes':
            return ''
        state.state['last_day_eaten'] = state.state['day']+90
        out = common_actions.increment_day(obj,90)
        out += '\n'
    else:
        state.state['last_day_eaten'] = state.state['day']+7
        out = common_actions.increment_day(obj,7)
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
        return "If you want some help, make sure your food bowl is upside down on Friday and I'll come visit.\nYou also better put back that painting or else they\'ll kill you for disrespecting Kim. -Yoda"

def move_painting(obj):
    if obj['object'] == 'A very special painting':
        return get_painting(obj)

def get_painting(obj):
    out = common_actions.add_to_inventory('A very special painting')
    state.state['painting_got'] = True
    out += '\nThere seems to be a note on the wall.'
    return out

def get(obj):
    if obj['object'] == 'A very special painting':
        return get_painting(obj)
    if obj['object'] == 'food':
        out = 'You cautiously pick up the bowl of "food".\nYou examine it. It seems to be dog kibble.'
        return out + common_actions.add_to_inventory('food')

def flip(obj):
  if obj['object'] == 'bowl':
    state.state['bowl_flipped'] = True
    return 'You flipped the bowl. Now all you have to do is wait until Friday.'

def open_item(obj):
    if obj['object'] == 'door' and 'key' not in state.state['inventory']:
        return "Cannot open the door. It is locked"
    elif obj['object'] == 'door':
        state.state['location'] == 'corridor'
        return corridor.welcome()

def welcome_back():
    state.state['location'] = 'cell'
    return 'Welcome back to your cell. Home sweet home.'

def cheat(obj):
    if not state.state['inventory']:
        state.state['inventory'] = ['Trump: The Art of the Deal', 'clout', 'food', 'GameBoy', 'backpack', 'spoon']
        state.state['inventory_limit'] = 1000
    if obj['object'] in ['recreation', 'cell', 'bathroom', 'messhall', 'corridor']:
        state.state['location'] = obj['object']
    return 'You cheated. How do you feel?'

def fake(obj):
    if obj['object'] == 'sleep':
        state.state['night'] = True
        return 'It is now 2:00 am. Type (sleep) to wake up at your normal time'

cell_options = {
    'sleep': common_actions.increment_day,
    'dig': dig_hole,
    'examine': examine,
    'get': get,
    'move': move_painting,
    'flip': flip,
    'open': open_item,
    'cheat': cheat,
    'fake': fake
}