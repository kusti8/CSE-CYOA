import collections
import state
import rooms.messhall
import rooms.bathroom
import rooms.corridor
import rooms.recreation
import common_actions
#import code handling actions the player can do anywhere and global state variables, as well as all rooms the player can go to from the cell

def every_turn_cell(): #things that can possibly occur after the player sleeps
    out = ''
    if state.state['dead']: #returns nothing if the player has lost the game already
        return ''
    if 'A very special painting' in state.state['inventory']: #kills the player if they do not replace the painting as instructed
        out += '\nA guard notices you have removed and disrespected the painting of His Greatness Kim Jong Un. You are killed immediately. \n\n'
        out += common_actions.game_quit()
    if state.state['bowl_flipped'] and common_actions.get_weekday(state.state['day']) == 'Friday': #gives the player a hint on Friday if they flip their bowl over as the note says to 
      out += '\nA very short, sickly looking man walks by your cell and whispers something:\n\t'
      out += '"An item, you need. Go through the ground, you must."'
      state.state ['bowl_flipped'] == False #turns the bow flipped state variable to False so that this does not occur again on the next Friday
    if common_actions.get_weekday(state.state['day']) == 'Tuesday' or common_actions.get_weekday(state.state['day']) == 'Thursday': #sends the player to the mess hall on Tuesdays and Thursdays
        state.state['location'] = 'messhall' 
        out += '\nA guard comes to your cell and brings you to the mess hall.'
        out += rooms.messhall.welcome() #calls the welcome message in the mess hall code
    if common_actions.get_weekday(state.state['day']) == 'Monday' or common_actions.get_weekday(state.state['day']) == 'Wednesday': #sends the player to the bathroom on Mondays and Wednesdays
        state.state['location'] = 'bathroom'
        out += '\nA guard comes to your cell and brings you to the bathroom.'
        out += rooms.bathroom.welcome() #calls the welcome message in the bathroom code
    if common_actions.get_weekday(state.state['day']) == 'Saturday' or common_actions.get_weekday(state.state['day']) == 'Sunday': #sends the player to the recreation room on Saturdays and Sundays
        state.state['location'] = 'recreation'
        out += '\nA guard comes to your cell and brings you to recreation.'
        out += rooms.recreation.welcome() #calls the welcome message in the recreation code
    return out


def dig_hole(obj): #allows the player to attempt to dig a hole in the cell floor
    out = ''
    if 'spoon' not in state.state['inventory']: #promps the player that attempting to dig a hole with their bare hands might get them executed
        response = input('Are you sure you want to do this? It is estimated to take around 3 months. You might be executed by then. Which is it: (yes) or (no)?')
        if response.lower() != 'y' and response.lower() != 'yes': #
            return 'You chose not to dig a hole.' #returns a message if the player chooses not to dig a hole
        state.state['last_day_eaten'] = state.state['day']+90 #prevents the player from dying of hunger when they spend 3 months digging the hole
        out += common_actions.increment_day(obj,90)
        out += '\n'
    else:
        out += "After a week, you find something in the dirt. It's a GameBoy! Now you can be entertained in prison." #if the player has a spoon, advances time by a week and gives them the GameBoy they dig up. 
        out += common_actions.add_to_inventory("GameBoy")
        if 'Sorry, but you are out of inventory space' not in out: #doesn't use 7 
            state.state['last_day_eaten'] = state.state['day']+7 
            out += common_actions.increment_day(obj,7)
            
    return out


def examine(obj): #possible results of an examine [item] command
    if obj['object'] == 'cot': #message if the [item] is the cot
        return 'It looks like it might fit you if you were 4 foot 9. Too bad you weren\'t arrested at age 7. Lacks a pillow'
    if obj['object'] == 'A very special painting': #message if the [item] is the painting
        return 'Kim Jong Un is wearing a Supreme shirt and Gucci jacket. High quality craftsmanship. The painting is sadly the most valuble object in the cell. Not well secured to the wall though. Looks like it might fall off.'
    if obj['object'] == 'schedule': #message if the [item] is the schedule
        return 'Comic Sans font, size 13. \nMonday: Bathroom break \nTuesday: Mess Hall\nWednsday: Bathroom break  \nThursday: Mess Hall \nFriday: Nothing \nSaturday: Recreation \nSunday: Recreaction'
    if obj['object'] == 'bowls': #message if the [item] is bowls
        return 'Looks like dog kibble and year-old apple juice. Better not eat that.'
    if obj['object'] == 'floor': #message if the [item] is the floor
        return 'Cold and dusty. Looks hard to dig through.'
    if obj['object'] == 'door': #message if the [item] is the door
        return 'Barred and locked. There is a large keyhole on the door.'
    if obj['object'] == 'note' and state.state['painting_got']: #message if the [item] is the note
        return "You read the note. \"If you want some help, make sure your food bowl is upside down on Friday and I'll come visit.\nYou also better put back that painting or else they\'ll kill you for disrespecting Kim. -Yoda\""

def move_painting(obj): #adds the painting to the player's inventory if they attempt to move it
    if obj['object'] == 'A very special painting':
        return get_painting(obj)

def get_painting(obj): #adds the painting to the player's inventory
    out = common_actions.add_to_inventory('A very special painting')
    if 'Sorry, but you are out of inventory space' not in out: #prevents result from being printed if lack of inventory space prevents painting removal
        state.state['painting_got'] = True
        out += '\nOh? There seems to be a note on the wall where the painting was covering moments ago.' #tells the player that there is a note behind where the painting was
    return out

def get(obj): #result of a get [item] command
    if obj['object'] == 'schedule': #prevents player from picking up schedule
        return 'They check to see if the schedule is still there every night. Better leave it.'
    if obj['object'] == 'A very special painting': #calls get_painting if [item] is the painting
        return get_painting(obj)
    if obj['object'] == 'bowl':
        out = 'You would rather eat mess hall food than the dog kibble in the bowl.'
        return out

def flip(obj): #allows the player to flip their food bowl as the note instructs
  if obj['object'] == 'bowl':
    state.state['bowl_flipped'] = True #sets the global state variable for the flip status of the bowl to True
    return 'You flipped the bowl. Now all you have to do is wait until Friday.'

def open_item(obj): #results if player attempts to open the door 
    if obj['object'] == 'door' and 'key' not in state.state['inventory']: #if the player does not have a key, inform them that the door is locked
        return "Cannot open the door. It is locked"
    elif obj['object'] == 'door' and 'key' in state.state['inventory']: #if the player has a key, open the door and enter the corridor
        state.state['location'] == 'corridor'
        return rooms.corridor.welcome()

def welcome_back(): #informs the player that they have returned to their cell
    state.state['location'] = 'cell' #sets the global location variable to 'cell'
    return 'Welcome back to your cell. Home sweet home.'

def cheat(obj): #a cheat command intended for debugging and development. Left in for demonstration and grading purposes
    if not state.state['inventory']: #if 'cheat' entered, give the player a variety of items that make winning the game trivial and infinate inventory space
        state.state['inventory'] = ['Trump: The Art of the Deal', 'clout', 'key', 'GameBoy', 'backpack', 'spoon']
        state.state['inventory_limit'] = 1000 
    if obj['object'] in ['recreation', 'cell', 'bathroom', 'messhall', 'corridor']: #if cheat [location] entered, teleport the player to a room of their choice
        state.state['location'] = obj['object']
    return 'You cheated. How do you feel?'

def fake(obj): #fake sleep command that the player gains the ability to use after completing the quiz game at recreation
    if obj['object'] == 'sleep' and state.state['fake_sleep']: #makes sure the player has gained the fake sleep ability
        state.state['night'] = True #sets time state to night
        return 'It is now 2:00 am. Type (sleep) to wake up at your normal time'

def use_key(obj): 
    if obj['object'] == 'key' and 'key' not in state.state['inventory']:
        return "Cannot open the door. It is locked"
    elif obj['object'] == 'key' and 'key' in state.state['inventory']:
        state.state['location'] == 'corridor'
        return rooms.corridor.welcome()

cell_options = {  #connects the player's entered commands to the parser to account for different terms that mean the same thing
    'sleep': common_actions.increment_day,
    'dig': dig_hole,
    'examine': examine,
    'get': get,
    'move': move_painting,
    'flip': flip,
    'open': open_item,
    'cheat': cheat,
    'fake': fake,
    'use': use_key
}