import state

def welcome():
    state.state['sub_location'] = 'tables'
    return "\n\nWelcome to the messhall. Eat up, because they serve something that isn't kibble here.\nThere is a food buffet at the far end of the room. To the left is a small one shelf library. Many books are missing."

def get(obj):
    if obj['object'] == 'food' and state.state['sub_location'] == 'buffet':
        return 'You are given a bowl of some sus.'
    if obj['object'] == 'spoon' and state.state['sub_location'] == 'buffet':
        
        return 'You acquire a spoon. Very useful in a prison.'

def go(obj):
    if obj["object"] == 'buffet':
        state.state['sub_location'] = 'buffet'
        return 'The buffet looks very appitizing compared to the kibble. There is also a place to take silverware for civilized eating, but not all inmates do\n. A drink machine labeled with recognizable soda brands is next to the silverware.'
    if obj["object"] == 'books':
        state.state['sub_location'] = 'library'
        return 'The books on the top shelf are labeled American classics. Copies of Huckleberry Finn, The Great Gatsby, and Trump: The Art of the Deal are all that remain'

messhall_options = {
    'get': get,
    'go': go
}