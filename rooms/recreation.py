import state
import common_actions
import rooms.cell
#import code handling actions the player can do anywhere and global state variables, as well as the cell room so that the welcome function can be called when the player returns to their cell
import tetris
import sys
from time import sleep
#import code handeling tetris minigame

def printf(s): #modify print() to have "typewriter" effect 
    for char in s:
        print(char, end='')
        sys.stdout.flush()
        sleep(0.02)
    print()

def welcome():  #print a description of the recreation room when the player first enters and set their sub location in the room to 'foyer' (nowhere)
    state.state['sub_location'] = 'foyer'
    return "\n\nWelcome to recreation! There's a group of guys playing pickup basketball to your right. \nA ways away in front of you is a few benches. The only people there is are two weird old men. To the left is a group of strong looking guys huddled in the coner. You may ask to (leave) to go back to your cell at any time."

def leave(obj): #returns the player to their cell
    return rooms.cell.welcome_back()
    
def go(obj):
    if obj['object'] == 'basketball':
        state.state['sub_location'] = 'basketball'
        return "There are a group of guys playing basketball, but you don't want to disturb them. There is a ball laying at your feet"
    if obj['object'] == 'man':
        state.state['sub_location'] = 'old_man'
        printf('You approach the benches. Do you wish to go talk to the man on the (left), the man on the (right), or (neither)?\n')
        dec = input().lower()
        if dec == 'left':
            return "The man is happy to have someone to talk to and gives you a proposition. If you can beat him in a game of Tetris, he will make you famous at the prison.\n. Say play to challenge him."
        if dec == 'right':
            questions = [
                '"Quicklyyyyy: What is Mr. Dennis\' greatest fear?\n(a) Elevators\n(b) 2nd Place at TSA States\n(c) Milling machines\n(d) Purple"',
                '"Which of these essays with get you a 100 on your English test?\n(a) A well thought out and clear essay\n(b) MLA citations\n(c) Crazy conspiracy theories\n(d) Tainted Christ"',
                '"Where does Mrs. Finley go all day?\n(a) She\'s in her office\n(b) Teaching Health class\n(c) No one knows!\n(d) Practicing CPR"',
                '"It is ten minutes to the end of the math period. What is half the class doing?\n(a) Homework\n(b) Prelab\n(c) Smash\n(d) Cards'
            ]
            correct_answers = ['b', 'd', 'c', 'd']
            your_answers = []
            printf('The man ignores your awkward greeting and starts asking you a variety of strange questions, rapid fire.\n')
            for question in questions:
                printf(question)
                your_answers.append(input('> ').strip().lower())
            if your_answers == correct_answers:
                state.state['fake_sleep'] = True
                return 'The man\'s voice changes to a normal tone and he stops attacking you with questions. \nHe says, "you seem knowledgeable about... stuff. Here\'s a tip. Try faking sleep some time and snooping around at night when the guards are tired. It might help you out.\nYou have gained the ability to fake sleep! Type (fake sleep) rather than (sleep) to pretend until 2:00 AM."'
            else:
                return 'The man stares at you with scorn. "Do you even have a 55 GPA? Try again fool."'
        if dec == 'neither' or dec == 'back' or dec == 'no':
            state.state['sub_location'] = 'foyer'
            return "Your nerves get the best of you and you slowly back away from the benches."
    if obj['object'] == 'guys':
        if 'clout' in state.state['inventory']:
            state.state['sub_location'] = 'market'
            out = "Turns out this is the prison black market. One man openes his jacket to reveal a few items:\n"
            for item in state.state['shop_inventory']:
                out += item + '\n'
            out+= 'Request an item to know what the market wants in return for it'
            return out
        else:
            state.state['sub_location'] = 'foyer'
            return "You don't have enough clout to visit the black market. Find some clout and try again. The guys push you back to the center of the rec hall."

def get(obj): #if the player tries to get a basketball and is located at the basktball court, add basketball to inventory
    out = ''
    if obj['object'] == 'basketball' and state.state['sub_location'] == 'basketball':
        out += common_actions.add_to_inventory('ball')
        out += '\nOne of the ball players shrugs and pulls an entire new backetball out of his pants pocket. Don\'t question it.'
    return out

def shoot(obj): #if the player tries to shoot hoops and has a basketball, avail them about their lack of ball skills
    out = ''
    if obj['object'] == 'basketball' and state.state['sub_location'] == 'basketball':
        out += 'You shoot the basketball, but it misses wildly, bounces back, and hits you in the head. Your time at HTHS has not prepared you for athletics.\n'
        out += common_actions.remove_from_inventory('ball')
    return out
    
def ask(obj):
    out = ''
    if state.state['sub_location'] == 'market' and len(state.state['inventory']) >= 4 and 'lantern' in state.state['shop_inventory']:
        out += 'The guys see how many items you have and are impressed. They gives you a lantern in recognition of your item prowess.\n'
        out += common_actions.add_to_inventory('lantern') + '.\n'
        state.state['shop_inventory'].remove('lantern')
    if obj['object'] == 'lantern' and state.state['sub_location'] == 'market':
        out += '"This item has no price. I give it out to people that have manage to build a large collection of items"'
    if obj['object'] == 'lambo' and state.state['sub_location'] == 'market':
        out += '"Son, do you really think you have enough money for this?"'
    if obj['object'] == 'key' and state.state['sub_location'] == 'market':
        out += '"I\'m looking for something that provides endless entertainment for this thing.'
    if obj['object'] == 'backpack' and state.state['sub_location'] == 'market':
        out += 'I would like something that would teach me how to improve our business in return for this.'
    return out

def trade(obj):
    out = ''
    if state.state['sub_location'] == 'market' and len(state.state['inventory']) >= 4 and 'lantern' in state.state['shop_inventory']:
        out += 'The guys see how many items you have and are impressed. He gives you a lantern because of it.'
        out += common_actions.add_to_inventory('lantern')
        state.state['shop_inventory'].remove('lantern')
    elif obj['object'].lower() == 'gameboy' and state.state['sub_location'] == 'market' and 'GameBoy' in state.state['inventory']:
        out += 'The men tell you that this key will open any cell door, but you\'ll just be shot by the guards if you do it during the day unrer normal circumstances. '
        out += common_actions.add_to_inventory('key') + '.\n'
        if 'Sorry, but you are out of inventory space' not in out:
            out += common_actions.remove_from_inventory('GameBoy') + '.\n'
            state.state['shop_inventory'].remove('key')
    elif obj['object'] == 'trump' and state.state['sub_location'] == 'market' and 'Trump: The Art of the Deal' in state.state['inventory']:
        out += 'The generic backpack is worn down, but expands your inventory just as effectivly as a designer bag. '
        out += common_actions.add_to_inventory('backpack') + '.\n'
        if 'Sorry, but you are out of inventory space' not in out:
            out += common_actions.remove_from_inventory('trump') + '.\n'
            state.state['shop_inventory'].remove('backpack')
    elif obj['object'] == 'lantern' or obj['object'] == 'key' or obj['object'] == 'backpack' and state.state['sub_location'] == 'market':
        out += '"No, tell us what YOU have to offer. Then we can complete a trade. Use the trade command on an item of yours."'
    elif obj['object'] == 'lambo' and state.state['sub_location'] == 'market':
        out += '"Hah! Like we would trade someone like you the lambo."'
    elif state.state['sub_location'] == 'market': 
        out += 'We don\'t have a use for that sorry item. Got anything cool? \nAsk what we want for a specific item before trying to trade.'
    return out

def play(obj):
    if state.state['sub_location'] != 'old_man':
        return
    game = tetris.Game()
    game.start()
    if game.score > 200:
        out = '"Congratulations on playing a great game," he says. "Here\'s some clout."'
        out += common_actions.add_to_inventory('clout')
        return out
    else:
        return 'The man shrugs and frowns. "I guess kids these days just don\'t know how to play tetris," he mutters.'

recreation_options = { #connects the player's entered commands to the parser to account for different terms that mean the same thing
    'leave': leave,
    'go': go,
    'get': get,
    'shoot': shoot,
    'ask': ask,
    'trade': trade,
    'play': play
}