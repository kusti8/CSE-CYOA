import state
import collections
import rooms.cell

days = {
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday',
    0: 'Sunday'
}

other_inventory_names = {
    "huck": "Huckleberry Finn",
    "gatsby": "The Great Gatsby",
    "trump": "Trump: The Art of the Deal"
}

def add_to_inventory(item):
    if item == 'backpack':
        state.state['inventory_limit'] = 6
    if len(state.state['inventory']) >= state.state['inventory_limit']:
        return "Sorry, but you are out of inventory space."
    else:
        state.state['inventory'].append(item)
        return "You now have " + item

def remove_from_inventory(item):
    if item == 'backpack':
        return 'No, no no. Not today.'
    if item in state.state['inventory']:
        state.state['inventory'].remove(item)
        return "You have removed " + item + " from your inventory." 
    elif item in other_inventory_names.keys():
        state.state['inventory'].remove(other_inventory_names[item])
        return "You have removed " + other_inventory_names[item] + " from your inventory." 

def game_quit():
    state.state['dead'] = True
    return "\nYou have died."
    
def get_weekday(day_num):
    return days[day_num % 7]
    
def increment_day(obj, num=1):
    state.state['night'] = False
    state.state['day'] = state.state['day'] + num
    weekday = get_weekday(state.state['day'])
    out = "It is now %s day %d." % (weekday, state.state['day'])
    if state.state['day'] - state.state['last_day_eaten'] > 4:
        out += '\nYou are very hungry. You look at the kibble anxiously.'
    if state.state['day'] - state.state['last_day_eaten'] > 9:
        out += ('\n' + game_quit())
    
    out += every_turn_universal()
    
    if state.state['location'] == 'cell':
        out += rooms.cell.every_turn_cell()

    return out
    
def every_turn_universal():
    out = ''
    if state.state['day'] > 30:
        out += '\nIt is the 30th day. You are executed by North Korea.'
        out += quit()
    elif state.state['day'] > 20:
        state.state['execution_posted'] = True
        out += '\nYour execution date has been posted on the wall. It is in 10 days. A shiver runs down your spine as you see it. Time is running out.'
    return out
        
def get_inventory(obj):
    out = 'You have:'
    for item, count in collections.Counter(state.state['inventory']).items():
        out += '\n' + str(count) + ' ' + item
        if count > 1:
            out += 's'
    return out
    
def remove(obj):
    return remove_from_inventory(obj['object'])

def get(obj):
    if obj['object'] == 'inventory':
        return get_inventory(obj)
        
def eat(obj):
    state.state['last_day_eaten'] = state.state['day']
    remove_from_inventory('food')
    return 'You eat some food. Another day of not going hungry.'
    
def examine(obj):
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
    if obj['object'] == 'ball':
        return 'Used to play a traditional American sport. Orange and black.'
    if obj['object'] == 'backpack':
        return 'Used to store things, giving you more inventory space. Seems like something you should hold on to.'
    
    
common_options = {
    'get': get,
    'remove': remove,
    'eat': eat,
    'examine': examine
}