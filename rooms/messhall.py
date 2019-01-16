import state
import common_actions
import rooms.cell
#import code handling actions the player can do anywhere and global state variables, as well as the cell room so that the welcome function can be called when the player returns to their cell

def welcome(): #print a description of the mess hall when the player first enters and set their sub location in the room to 'tables'
    state.state['sub_location'] = 'tables'
    return "\n\nWelcome to the Mess Hall. Eat up, because they serve something that isn't kibble here.\nThere is a food buffet at the far end of the room. To the left is a small one shelf library. Many books are missing. You are at the tables with a few other inmates. You may ask to (leave) to go back to your cell at any time."

def get(obj): #result of a get [item] command
    out = ''
    print(obj)
    if obj['object'] == 'food' and state.state['sub_location'] == 'buffet':
        out += common_actions.add_to_inventory('food') #adds food to inventory if located at buffet
    if obj['object'] == 'spoon' and state.state['sub_location'] == 'buffet':
        out += common_actions.add_to_inventory('spoon') #adds spoon to inventory if located at buffet
        out += '. Very useful in a prison.' #adds a hint to spoon receipt text
    if obj['object'] == 'drink' and state.state['sub_location'] == 'buffet': #tells the player they cannot take a drink if they attempt to at the buffet
        out += 'You try to take a drink. Looks like the Coke, Pepsi, and water are all filled with motor oil. Dang. You pass on the drinks.'
    if obj['object'] == 'huck' and state.state['sub_location'] == 'library': 
        out += common_actions.add_to_inventory('Huckleberry Finn') #adds Huckleberry Finn to inventory if located at library
    if obj['object'] == 'gatsby' and state.state['sub_location'] == 'library':
        out += common_actions.add_to_inventory('The Great Gatsby') #adds The Great Gatsby to inventory if located at library
    if obj['object'] == 'trump' and state.state['sub_location'] == 'library':
        out += common_actions.add_to_inventory('Trump: The Art of the Deal') #adds Trump: The Art of the Deal to inventory if located at library
    if obj['object'] == 'library' and state.state['sub_location'] == 'library': 
        out += 'Select a book to take by name using the abbreviated title in parenthesis: (Huck), (Gatsby), or (Trump)' #tells the player to pick a specific book if the try to get a generic book
    return out

def go(obj): #allows the player to go to sub locations in the mess hall
    if obj["object"] == 'buffet' or obj["object"] == 'food':
        state.state['sub_location'] = 'buffet' #goes to the buffet and describes it
        return 'The buffet looks very appetizing compared to the kibble. There is also a place to take silverware for civilized eating, but not all inmates do.\nA drink machine labeled with recognizable soda brands is next to the silverware.'
    if obj["object"] == 'library':
        state.state['sub_location'] = 'library' #goes to the mini library and describes it
        return 'The books on the top shelf are labeled American classics. Copies of (Huck)leberry Finn, The Great (Gatsby), and (Trump): The Art of the Deal are all that remain.\nA sign states that you can take a book if you would like.'
    if obj["object"] == 'tables':
        state.state['sub_location'] = 'tables' #goes to the tables and describes it
        return 'You sit down at one of the tables. Next to you is a bored looking man poking at his food. You could try to talk to him.'

def talk(obj): #allows the player to initiate a conversation with a man if located at the tables
    if state.state['sub_location'] is not 'tables':
        return
    dennis_options = [ #lists all words or phrases that initiate a special reaction from the man
        "mr. dennis",
        "mr dennis",
        "dennis",
        "bob dennis",
        "bobby d",
        "big bobby d",
        "robert dennis"
    ]
    name = input("You start a conversation with a guy at the table. He asks you your name: ") #takes in a name string that the player types in
    out = ''
    print(name.lower().strip(), dennis_options)
    if name.lower().strip() in dennis_options: #if the name entered is a nickname of former HTHS teacher and TSA extrodinare Mr. Robert Dennis, add clout to their inventory
        out += 'The man suddenly bows. I did not think I would meet you here. Here is some clout. Save travels, oh holy one.\n'
        out += common_actions.add_to_inventory('clout')
    else:
        out += 'The man grunts and turns away. You feel unimportant.' #all other names illicit no response
    return out

def leave(obj): #returns the player to their cell
    return rooms.cell.welcome_back()

messhall_options = { #connects the player's entered commands to the parser to account for different terms that mean the same thing
    'get': get,
    'go': go,
    'talk': talk,
    'leave': leave
}