import state
import common_actions
import rooms.cell

def welcome():
    return "\n\nWelcome to the bathroom. It is very shabby: there is almost no room to move around, the ceiling is low and almost hits you in the head, and the floor is covered in dirt, but at least you get a bathroom. Rumor is some inmates don't get one.\nThere is a single toilet in front of you and a sink and mirror behind you. The walls to the right and left are covered in graffiti. You may ask to (leave) to go back to your cell at any time."

def use(obj):
    if obj['object'] == 'toilet':
        return "Hey. Mind your business. I'm using the toilet"
    if obj['object'] == 'sink':
        return "You wash your hands thoroughly, remembering to wait until you finish singing Happy Birthday, just like your momma taught you."
    if obj['object'] == 'mirror':
        return "You look at yourself in the mirror. You're still devilishly handsome, even in prison."

def examine(obj):
    if obj['object'] == 'toilet':
        return 'White porcelin and beautiful. Just kidding.'
    if obj['object'] == 'sink':
        return 'Has two knobs, one for cold water and one for hot. The hot water one is snapped at an odd angle.'
    if obj['object'] == 'mirror':
        return "You look at yourself in the mirror. You're still devilishly handsome, even in prison."
    if obj['object'] == 'walls': 
        return "There's a ton of grafitti. Some is in other languages. A long soliloqy in the middle stands out:\n\nSelon toutes les lois connues de l'aviation, il est impossible qu'une abeille puisse voler. \nSes ailes sont trop petites pour tirer son gros corps du sol. L'abeille, bien sûr, vole quand même. \nParce que les abeilles ne se soucient pas de ce que les humains pensent impossible."
    
def push(obj):
    if obj['object'] == 'ceiling':
        state.state['ceiling_pushed'] = True
        return 'The low ceiling gives way and reveals a secret crevice above your head. There appears to be an object in the shadows of the crevice'
    
def get(obj):
    if obj['object'] == 'ceiling':
        return push(obj)
    if obj['object'] == 'object' and state.state['ceiling_pushed']:
        out = common_actions.add_to_inventory('backpack') + '\n'
        out += common_actions.add_to_inventory('clout') + '\n'
        out += 'You pull out the objet. It is a Supreme brand backpack! The backpack also gives you clout, by the sheer essence of being Supreme.'
        return out

def leave(obj):
    return rooms.cell.welcome_back()

bathroom_options = {
    'use': use,
    'examine': examine,
    'push': push,
    'get': get,
    'leave': leave
}