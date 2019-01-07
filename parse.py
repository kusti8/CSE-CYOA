def parse_input(text):
    verbs = {
        'take': ['get', 'grab'],
        'walk': ['move', 'run', 'jog'],
        'sleep': ['dream'],
        'dig': [],
        'examine': ['look', 'check', 'read'],
        'eat': ['drink'],
        'get': ['get', 'retrieve', 'collect', 'take'],
        'move': ['displace'],
        'remove': ['return', 'throw'],
        'flip': [],
        'open': [],
        'go': ['goto' 'walk', 'walkto','travel']
    }
    nouns = {
        'left': ['west'],
        'right': ['right'],
        'cot': ['bed'],
        'A very special painting': ['picture', 'Kim', 'drawing', 'painting'],
        'schedule': [],
        'note': ['paper', 'sheet'],
        'bowl': ['kibble', 'food', 'drink', 'water', 'juice', 'bowls'],
        'floor': ['ground'],
        'door': [],
        'inventory': [],
        'buffet': [],
        'book': ['books', 'library', 'shelf']
    }
    tokenized = text.strip().split()
    out = {'action': '', 'object': ''}
    for verb, options in verbs.items():
        if tokenized[0] in options or tokenized[0]==verb:
            out['action'] = verb
    for noun, options in nouns.items():
        if tokenized[-1] in options or tokenized[-1]==noun:
            out['object'] = noun
    return out