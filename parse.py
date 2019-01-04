def parse_input(text):
    verbs = {
        'take': ['get', 'grab'],
        'walk': ['move', 'run', 'jog'],
        'sleep': ['dream'],
        'dig': [],
        'examine': ['look', 'check'],
        'eat': ['drink']
    }
    nouns = {
        'left': ['west'],
        'right': ['right'],
        'cot': ['bed'],
        'painting': ['picture', 'Kim', 'drawing'],
        'schedule': ['paper', 'sheet'],
        'bowls': ['kibble', 'food', 'drink', 'water', 'juice'],
        'floor': ['ground'],
        'door': []
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