import state
import common_actions
import rooms.cell
#import code handling actions the player can do anywhere and global state variables, as well as the cell room so that the welcome function can be called when the player returns to their cell

def welcome(): #print a description of the bathroom when the player first enters
    return "\n\nWelcome to the bathroom. It is very shabby: there is almost no room to move around, the ceiling is low and almost hits you in the head, and the floor is covered in dirt, but at least you get a bathroom. Rumor is some inmates don't get one.\nThere is a single toilet in front of you and a sink and mirror behind you. The walls to the right and left are covered in graffiti. You may ask to (leave) to go back to your cell at any time."

def use(obj): #possible results of a use [item] command
    if obj['object'] == 'toilet' or obj['object'] == 'bathroom': #message if the [item] is the toilet
        return "Hey. Player. Yes you. Mind your own business. I'm using the toilet."
    if obj['object'] == 'sink': #message if the [item] is the sink
        return "You wash your hands thoroughly, remembering to wait until you finish singing Happy Birthday, just like your momma taught you."
    if obj['object'] == 'mirror': #message if the [item] is the mirror
        return "You look at yourself in the mirror. You're still devilishly handsome, even in prison."

def examine(obj): #possible results of an examine [item] command
    if obj['object'] == 'toilet': #message if the [item] is the toilet
        return 'White porcelain and beautiful. Just kidding.'
    if obj['object'] == 'sink': #message if the [item] is the sink
        return 'Has two knobs, one for cold water and one for hot. The hot water one is snapped at an odd angle.'
    if obj['object'] == 'mirror': #message if the [item] is the mirror
        return "You look at yourself in the mirror. You're still devilishly handsome, even in prison."
    if obj['object'] == 'walls': #message if the [item] is the walls
        return "There's a ton of graffiti. Some is in other languages. A long soliloquy in the middle stands out:\n\nSelon toutes les lois connues de l'aviation, il est impossible qu'une abeille puisse voler. \nSes ailes sont trop petites pour tirer son gros corps du sol. L'abeille, bien sûr, vole quand même. \nParce que les abeilles ne se soucient pas de ce que les humains pensent impossible."
    if obj['object'] == 'ceiling': #message if the [item] is the ceiling
        return "The ceiling is very low and almost hits you in the head."
    if obj['object'] == 'floor': #message if the [item] is the floor
        return "Made of dirty tile. Much stronger than your cell's floor."
    
def push(obj): #result of a push ceiling command
    if obj['object'] == 'ceiling': 
        state.state['ceiling_pushed'] = True #set the state of the ceiling to pushed so that the item inside can be accessed
        return 'The low ceiling gives way and reveals a secret crevice above your head. There appears to be an object in the shadows of the crevice.'  #response to player upon pushing ceiling
      
def get(obj): #result of a get [item] command
    if obj['object'] == 'ceiling': #pushes ceiling if the player tries to 'get' the low tile
        return push(obj)
    if obj['object'] == 'object' and state.state['ceiling_pushed']:  
        #if the ceiling has been pushed, adds the backpack and clout hidden there to their inventory
        out = 'You pull out the object. It is a Supreme brand backpack! The backpack also gives you clout, by the sheer essence of being Supreme.' #response to player upon getting the backpack
        out += common_actions.add_to_inventory('backpack') + '\n'
        out += common_actions.add_to_inventory('clout') + '\n'
        return out

def leave(obj): #returns the player to their cell
    return rooms.cell.welcome_back()

def wash(obj):
    obj['object'] = 'sink'
    return use(obj)

bathroom_options = { #connects the player's entered commands to the parser to account for different terms that mean the same thing
    'use': use,
    'examine': examine,
    'push': push,
    'get': get,
    'leave': leave,
    'wash': wash
}