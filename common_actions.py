import state
import collections
import rooms.cell
import rooms.bathroom
import rooms.corridor
import rooms.messhall
import rooms.recreation
#import global state variables, collections library, and the cell location code

days = { #list of weekdays and their corresponding numbers
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday',
    0: 'Sunday'
}

other_inventory_names = { #list of alternate names for some items that can be added to your inventory
    "huck": "Huckleberry Finn",
    "gatsby": "The Great Gatsby",
    "trump": "Trump: The Art of the Deal"
}

def add_to_inventory(item): #adds an item to inventory or tells the player that they cannot do so if they are out of inventory space 
    if len(state.state['inventory']) >= state.state['inventory_limit']:
        return "Sorry, but you are out of inventory space."
    else:
        if item == 'backpack':
            state.state['inventory_limit'] = 6
        state.state['inventory'].append(item)
        return "You now have " + item

def remove_from_inventory(item): #removes an item from the player's inventory unless it is a backpack, which cannot be removed
    if item == 'backpack':
        return 'No, no no. Not today.'
    if item in state.state['inventory']:
        state.state['inventory'].remove(item)
        return "You have removed " + item + " from your inventory." 
    elif item in other_inventory_names.keys():
        state.state['inventory'].remove(other_inventory_names[item])
        return "You have removed " + other_inventory_names[item] + " from your inventory." 

def game_quit(): #quits the program and prints 'you have died' if the player loses
    state.state['dead'] = True
    return "\nYou have died."
    
def get_weekday(day_num): #prints the current day of the week
    return days[day_num % 7]
    
def increment_day(obj, num=1): #called when the player sleeps
    state.state['night'] = False #sets state to daytime
    state.state['day'] = state.state['day'] + num #increments the day number by one
    weekday = get_weekday(state.state['day'])
    out = "It is now %s day %d." % (weekday, state.state['day']) #prints the day and the day of the week to the player
    if state.state['day'] - state.state['last_day_eaten'] > 5: #informs the player that they need to eat soon
        out += '\nYou are very hungry. You look at the kibble anxiously.'
    if state.state['day'] - state.state['last_day_eaten'] > 9: #kills the player if they do not eat for 10 days in a row
        out += ('\n' + game_quit())
    
    out += every_turn_universal() #handles the countdown to execution on day 31
    
    if state.state['location'] == 'cell':
        out += rooms.cell.every_turn_cell() #adds additonal lines to be printed to the player in certain situations

    return out 
    
def every_turn_universal(): #handles the countdown to execution on day 31
    out = ''
    if state.state['day'] > 30: #if the player reaches a day past the 30th day tell them that they have been executed and quit the program
        out += '\nIt is the ' + str(state.state['day']) + 'th day. You are executed by North Korea.'
        out += game_quit()
    elif state.state['day'] > 20: #if the player reaches a day past the 20th day tell them how long until they will be executed
        state.state['execution_posted'] = True
        out += '\nYour execution date has been posted on the wall. It is in ' + str(30-state.state['day']) + ' days. A shiver runs down your spine as you see it. Time is running out.'
    return out
        
def get_inventory(obj): #prints the contents of the player's inventory
    out = 'You have:'
    for item, count in collections.Counter(state.state['inventory']).items():
        out += '\n' + str(count) + ' ' + item
        if count > 1:
            out += 's'
    return out
    
def remove(obj): #removes any item in the player's inventory permenently
    return remove_from_inventory(obj['object'])

def get(obj): #calls get inventory
    if obj['object'] == 'inventory':
        return get_inventory(obj)
    if obj['object'] == 'day':
        return "It is " + get_weekday(state.state['day']) + ", day " + str(state.state['day']) 
        
def eat(obj): #allows the player to eat food out of their inventory if they have any
    if 'food' in state.state['inventory']:
        state.state['last_day_eaten'] = state.state['day']
        remove_from_inventory('food')
        return 'You eat some food. Another day of not going hungry.'
    else:
        return 'Can\'t do that if you don\'t have any food to eat!'
    
def examine(obj): #allows inventory items to be examined at any time if the player has that item
    if obj['object'] == 'food' and 'food' in state.state['inventory']:
        return 'Mystery flavor. Probably chicken but who knows. Beats kibble though.'
    if obj['object'] == 'spoon' and 'soup' in state.state['inventory']:
        return 'Made of metal for some reason. Oddly large. Seems like a liability in a maximum security prison'
    if obj['object'] == 'huck' and 'Huckleberry Finn' in state.state['inventory']:
        return 'Inside cover has a Mark Twain quote: “Never argue with an idiot. They will drag you down to their level and beat you with experience.” You wish you had a game console instead of the book.'
    if obj['object'] == 'trump' and 'Trump: The Art of the Deal' in state.state['inventory']:
        return 'The dude on the cover has swagger to rival the Kim Jong Un painting but the book is lame. Might interest an imprisoned entrepreneur though.'
    if obj['object'] == 'gatsby' and 'The Great Gatsby' in state.state['inventory']:
        return 'You recall from Junior English at HTHS that this book is better than most classics but still a 4/10 at best. Has two towns named "Egg" though. You wish you had a game console instead of the book.'
    if obj['object'] == 'book': 
        return 'What book? Use abbreviated titles.'
    if obj['object'] == 'ball' and 'ball' in state.state['inventory']:
        return 'Used to play a traditional American sport. Orange and black.'
    if obj['object'] == 'backpack' and 'backpack' in state.state['inventory']:
        return 'Used to store things, giving you more inventory space. Seems like something you should hold on to.'
    
def die(obj): #If the player wants to die, kill them
    return game_quit()
    
def kill(obj): #If the player wants to die, kill them
    return die(obj)
    
def look(obj): #Reprints the room intro/welcome
    if state.state['location'] == 'cell':
        rooms.cell.welcome()
        return ' '
    elif state.state['location'] == 'bathroom':
        return rooms.bathroom.welcome()
    elif state.state['location'] == 'corridor':
        return rooms.corridor.welcome()
    elif state.state['location'] == 'messhall':
        return rooms.messhall.welcome()
    elif state.state['location'] == 'recreation':
        return rooms.recreation.welcome()

def help(obj): #lists the game's fundamental commands
    out = "Here are some common commands you can use:\n"
    out += """get inventory: List objects the player’s inventory contains (max two without a backpack item, six with a backpack)
get weekday: returns the in-game day of the week 
get [item]: adds an item currently accessible to the player to their inventory
remove [item]: removes an item from the player’s inventory permanently
examine [item]: provides additional information on an item currently accessible to the player or in their inventory
leave [location]: will return from any other room to your prison cell
sleep: advance to the next day
"""
    return out

common_options = { #connects the player's entered commands to the parser to account for different terms that mean the same thing
    'get': get,
    'remove': remove,
    'eat': eat,
    'examine': examine,
    'die': die,
    'kill': kill,
    'look': look,
    'help': help
}