import state
import common_actions
import rooms.cell

def welcome():
    state.state['sub_location'] = 'tables'
    return "\n\nWelcome to the Mess Hall. Eat up, because they serve something that isn't kibble here.\nThere is a food buffet at the far end of the room. To the left is a small one shelf library. Many books are missing. You are at the tables with a few other inmates. You may ask to (leave) to go back to your cell at any time."

def get(obj):
    out = ''
    if obj['object'] == 'food' and state.state['sub_location'] == 'buffet':
        out += common_actions.add_to_inventory('food')
    if obj['object'] == 'spoon' and state.state['sub_location'] == 'buffet':
        out += common_actions.add_to_inventory('spoon')
        out += '. Very useful in a prison.'
    if obj['object'] == 'drink' and state.state['sub_location'] == 'buffet':
        out += 'You try to take a drink. Looks like the Coke, Pepsi, and water are all filled with motor oil. Dang. You pass on the drinks.'
    if obj['object'] == 'huck' and state.state['sub_location'] == 'library':
        out += common_actions.add_to_inventory('Huckleberry Finn')
    if obj['object'] == 'gatsby' and state.state['sub_location'] == 'library':
        out += common_actions.add_to_inventory('The Great Gatsby')
    if obj['object'] == 'trump' and state.state['sub_location'] == 'library':
        out += common_actions.add_to_inventory('Trump: The Art of the Deal')
    if obj['object'] == 'book' and state.state['sub_location'] == 'library':
        out += 'Select a book to take by name using the abbreviated title in parenthesis: (Huck), (Gatsby), or (Trump)'
    return out

def examine(obj):
    if obj['object'] == 'food' and 'food' in state.state['inventory']:
        return 'Mystery flavor. Probably chicken but who knows. Beats kibble though.'
    if obj['object'] == 'spoon' and 'soup' in state.state['inventory']:
        return 'Made of metal for some reason. Oddly large. Seems like a liability in a maximum security prison'

def go(obj):
    if obj["object"] == 'buffet':
        state.state['sub_location'] = 'buffet'
        return 'The buffet looks very appitizing compared to the kibble. There is also a place to take silverware for civilized eating, but not all inmates do.\n A drink machine labeled with recognizable soda brands is next to the silverware.'
    if obj["object"] == 'library':
        state.state['sub_location'] = 'library'
        return 'The books on the top shelf are labeled American classics. Copies of (Huck)leberry Finn, The Great (Gatsby), and (Trump): The Art of the Deal are all that remain.'

def talk(obj):
    dennis_options = [
        "mr. dennis",
        "mr dennis",
        "dennis",
        "bob dennis",
        "bobby d",
        "big bobby d"
    ]
    name = input("You start a conversation with a guy at the table. He asks you your name: ")
    out = ''
    if name.lower() in dennis_options:
        out += 'The man suddenly bows. I did not think I would meet you here. Here is some clout. Save travels, oh holy one.\n'
        out += common_actions.add_to_inventory('clout')
    else:
        out += 'The man grunts and turns away. You feel unimportant.'
    return out

def leave(obj):
    return rooms.cell.welcome_back()

messhall_options = {
    'get': get,
    'go': go,
    'talk': talk,
    'leave': leave
}