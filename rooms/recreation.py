import state
import common_actions
import rooms.cell
import tetris

def welcome():
    state.state['sub_location'] = 'foyer'
    return "\n\nWelcome to recreation! There's a group of guys playing pickup basketball to your right. \nA ways away in front of you is a few benches. The only person there is a weird old man. To the left is a group of strong looking guys huddled in the coner. You may ask to (leave) to go back to your cell at any time."

def leave(obj):
    return rooms.cell.welcome_back()
    
def go(obj):
    if obj['object'] == 'basketball':
        state.state['sub_location'] = 'basketball'
        return "There are a group of guys playing basketball, but you don't want to disturb them. There is a ball laying at your feet"
    if obj['object'] == 'man':
        state.state['sub_location'] = 'old_man'
        return 'You approach the old man. He says: "I challenge you to a game of Tetris. If you win, you will become well known in the prison"'
    if obj['object'] == 'guys':
        if 'clout' in state.state['inventory']:
            state.state['sub_location'] = 'market'
            out = "Turns out this is the prison black market. One man openes his jacket to reveal a few items.\n"
            for item in state.state['shop_inventory']:
                out += item + '\n'
            out+= 'Request an item to know what the market wants in return for it'
            return out
        else:
            state.state['sub_location'] = 'foyer'
            return "You don't have enough clout to visit the black market. Find some clout and try again. The guys push you back to the center of the rec hall."

def get(obj):
    out = ''
    if obj['object'] == 'basketball' and state.state['sub_location'] == 'basketball':
        out += common_actions.add_to_inventory('ball')
        out += '\nOne of the ball players shrugs and pulls an entire new backetball out of his pants pocket. Don\'t question it.'
    return out

def shoot(obj):
    out = ''
    if obj['object'] == 'basketball' and state.state['sub_location'] == 'basketball':
        out += 'You shoot the basketball, but it misses wildly, bounces back, and hits you in the head. Your time at HTHS has not prepared you for athletics.\n'
        out += common_actions.remove_from_inventory('ball')
    return out
    
def ask(obj):
    if state.state['sub_location'] == 'market' and len(state.state['inventory']) >= 4 and 'lantern' in state.state['shop_inventory']:
        out = 'The guys see how many items you have and are impressed. He gives you a lantern because of it.'
        out += common_actions.add_to_inventory('lantern')
        state.state['shop_inventory'].remove('lantern')
        return out
    if obj['object'] == 'lantern' and state.state['sub_location'] == 'market':
        return '"This item has no price. I give it out to people that have manage to build a large collection of items"'
    if obj['object'] == 'lambo' and state.state['sub_location'] == 'market':
        return '"Son, do you really think you have enough money for this?"'
    if obj['object'] == 'key' and state.state['sub_location'] == 'market':
        return '"I\'m looking for something that provides endless entertainment for this thing.'
    if obj['object'] == 'backpack' and state.state['sub_location'] == 'market':
        return 'I would like something that would teach me how to improve our business in return for this.'

def trade(obj):
    out = ''
    if state.state['sub_location'] == 'market' and len(state.state['inventory']) >= 4 and 'lantern' in state.state['shop_inventory']:
        out += 'The guys see how many items you have and are impressed. He gives you a lantern because of it.'
        out += common_actions.add_to_inventory('lantern')
        state.state['shop_inventory'].remove('lantern')
    if obj['object'] == 'GameBoy' and state.state['sub_location'] == 'market' and 'GameBoy' in state.state['inventory']:
        out += 'The men tell you that this key will open any cell door, but you\'ll just be shot by the guards if you do tduring the day unrer normal circumstances'
        out += common_actions.add_to_inventory('key')
        out += common_actions.remove_from_inventory('GameBoy')
        state.state['shop_inventory'].remove('key')
    if obj['object'] == 'trump' and state.state['sub_location'] == 'market' and 'Trump: The Art of the Deal' in state.state['inventory']:
        out += 'The generic backpack is worn down, but expands your inventory just as effectivly as a designer bag.'
        out += common_actions.add_to_inventory('backpack')
        out += common_actions.remove_from_inventory('trump')
        state.state['shop_inventory'].remove('backpack')
    return out

def play(obj):
    game = tetris.Game()
    game.start()
    if game.score > 3:
        out = "Congratulations. Here's some clout."
        out += common_actions.add_to_inventory('clout')
        return out
    else:
        return 'I guess kids these days just don\'t know how to paly tetris.'

recreation_options = {
    'leave': leave,
    'go': go,
    'get': get,
    'shoot': shoot,
    'ask': ask,
    'trade': trade,
    'play': play
}