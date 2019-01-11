import state

def parse_input(text):
    verbs = {
        'walk': ['move', 'run', 'jog'],
        'sleep': ['dream'],
        'dig': [],
        'examine': ['look', 'check', 'read'],
        'eat': ['drink'],
        'get': ['retrieve', 'collect', 'take', 'get', 'grab'],
        'move': ['displace'],
        'remove': ['return', 'throw'],
        'flip': [],
        'open': [],
        'go': ['goto' 'walk', 'walkto','travel'],
        'talk': ['converse'],
        'play': [],
        'use': ['utilize', 'turn', 'on'],
        'push': [],
        'leave': ['quit'],
        'shoot': ['throw'],
        'ask': ['inquire', 'request'],
        'trade': ['barter'],
        'cheat': []
    }
    nouns = {
        'cell': {
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
            'GameBoy': [],
            'cell': []
        },
        'messhall': {
            'buffet': [],
            'library': ['books', 'book', 'shelf'],
            'food': [],
            'spoon': ['spork'],
            'huck': ['Huck', 'Huckleberry'],
            'gatsby': ['Gatsby'],
            'trump': ['Trump'],
            'messhall': []
        },
        'bathroom': {
            'toilet': ['bidet', 'toilette'],
            'sink': [],
            'walls': ['wall', 'room'],
            'ceiling': ['roof'],
            'object': ['thing', 'item'],
            'mirror': [],
            'bathroom': []
        },
        'recreation': {
            'basketball': ['bball', 'ball', 'match', 'court', 'hoop', 'game'],
            'man': ['bench','benches', 'men'],
            'guys': ['men', 'people', 'corner', 'gang', 'black', 'market', 'shop', 'store'],
            'lambo': ['lamborghini', 'car'],
            'lantern': ['light'],
            'key': ['room'],
            'backpack': [],
            'recreation': []
        },
        'corridor': {
            'forward': ['straight', 'north', 'up'],
            'corridor': []
        }
    }
    
    def parse(obj, location, tokenized):
        for main, options in obj.items():
            if tokenized[location] in options or tokenized[location]==main:
                return main
    
    def merge_dicts(d, non_location):
        out = {}
        for location in d.keys():
            if location != non_location:
                out.update(d[location])
        return out
    
    tokenized = text.strip().split()
    out = {'action': '', 'object': ''}
    out['action'] = parse(verbs, 0, tokenized)
    
    my_nouns = nouns[state.state['location']] # Nouns for my room
    out['object'] = parse(my_nouns, -1, tokenized)
    
    if not out['object']: # We didn't find it in our nouns
        out['object'] = parse(merge_dicts(nouns, state.state['location']), -1, tokenized)
        
    if len(tokenized) < 2:
        out['object'] = 'NONE'
    
    return out