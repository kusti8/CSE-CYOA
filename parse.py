import state
#import global state variables file

def parse_input(text): 
    verbs = { #replaces verbs with a synonym if a function will understand a synonym of a verb entered in a command
        'walk': ['run', 'jog'],
        'sleep': ['dream'],
        'dig': [],
        'examine': ['check', 'read'],
        'look': [],
        'eat': ['drink'],
        'get': ['retrieve', 'collect', 'take', 'grab', 'pick'],
        'move': ['displace'],
        'remove': ['return', 'drop'],
        'flip': ['turn'],
        'open': ['unlock'],
        'go': ['goto' 'walk', 'walkto','travel', 'proceed'],
        'talk': ['converse'],
        'play': [],
        'use': ['utilize', 'on'],
        'push': [],
        'leave': ['quit'],
        'shoot': ['throw'],
        'ask': ['inquire', 'request'],
        'trade': ['barter', 'give'],
        'cheat': [],
        'fake': [],
        'die': ['kill', 'commit'],
        'wash': [],
        'help': []
    }
    nouns = { #replaces nouns with a synonym if a function will understand a synonym of a noun entered in a command
        'cell': { #noun replacements when player is located in the cell
            'left': ['west'],
            'right': ['east'],
            'cot': ['bed'],
            'A very special painting': ['picture', 'Kim', 'drawing', 'painting'],
            'schedule': [],
            'note': ['paper', 'sheet'],
            'bowl': ['kibble', 'food', 'drink', 'water', 'juice', 'bowls'],
            'floor': ['ground'],
            'door': [],
            'inventory': [],
            'GameBoy': ['gameboy', 'Gameboy'],
            'cell': [],
            'sleep': [],
            'hole': ['escape', 'dirt'],
            'day': ['weekday', 'date']
        },
        'messhall': { #noun replacements when player is located in the mess hall
            'buffet': [],
            'library': ['books', 'book', 'shelf', 'bookshelf'],
            'food': [],
            'spoon': ['spork'],
            'huck': ['Huck', 'Huckleberry'],
            'gatsby': ['Gatsby'],
            'trump': ['Trump'],
            'messhall': [],
            'drink': ['water', 'coke', 'pepsi'],
            'tables': ['table'],
            'him': []
        },
        'bathroom': { #noun replacements when player is located in the bathroom
            'toilet': ['bidet', 'toilette'],
            'sink': [],
            'walls': ['wall', 'room', 'graffiti'],
            'ceiling': ['roof'],
            'object': ['thing', 'item'],
            'mirror': [],
            'bathroom': [],
            'hands': []
        },
        'recreation': { #noun replacements when player is located in the recreation room
            'basketball': ['bball', 'ball', 'match', 'court', 'hoop', 'game'],
            'man': ['bench','benches', 'men'],
            'guys': ['people', 'corner', 'gang', 'black', 'market', 'shop', 'store'],
            'lambo': ['lamborghini', 'car'],
            'lantern': ['light'],
            'key': ['room'],
            'backpack': [],
            'recreation': []
        },
        'corridor': { #noun replacements when player is located in the corridor
            'forward': ['straight', 'north', 'up'],
            'corridor': []
        }
    }
    
    def parse(obj, location, tokenized): 
        # Go through all of the words and check if we are equal to the word or any of the synonyms
        for main, options in obj.items():
            if tokenized[location] in options or tokenized[location]==main:
                return main
    
    def merge_dicts(d, non_location):
        # Merge the individual dictionaries of the nouns for the different rooms
        out = {}
        for location in d.keys():
            if location != non_location:
                out.update(d[location])
        return out
    
    tokenized = text.strip().split() # Split into words
    out = {'action': '', 'object': ''}
    out['action'] = parse(verbs, 0, tokenized) # Find a verb as the first word
    
    my_nouns = nouns[state.state['location']] # Nouns for my room
    out['object'] = parse(my_nouns, -1, tokenized) # Find a noun of my room as the last word
    
    if not out['object']: # We didn't get a noun, so broaden the search to all of the locations
        out['object'] = parse(merge_dicts(nouns, state.state['location']), -1, tokenized) # Merge all the rest of the nouns together
        
    if len(tokenized) < 2: #if phrase length is less than two words
        out['object'] = 'NONE'
    
    return out #return phrase as the player command functions will understand