import state
import common_actions
import rooms.cell
#import code handling actions the player can do anywhere and global state variables, as well as the cell room so that the welcome function can be called when the player returns to their cell

def welcome(): #print a description of the corridor when the player first enters
    out = 'You opened the door of your cell! Congratulations! However, your escape is not over yet. You must still navigate the corridor and escape the prison building. \nYou\'re in the final stretch. Don\'t mess it up.'
    if not state.state['night']: #adds to the welcome message if the player exits their cell during the day
        out += '\nIt\'s the middle of the day and there are guards everywhere. You could try to escape, but that looks like it might get you killed.\n Want to (go back) to your cell or (proceed forward) down the corridor?'
    else: #adds to the welcome message if the player exits their cell during the night
        out += '\nIt is dark and difficult to see. There seems to be very few guards during the night. It might be difficult to avoid them in the dark, however.\nWant to (go back) to your cell or (proceed forward) down the corridor?'
    if state.state['night'] and 'lantern' in state.state['inventory']: #adds to the welcome message if the player exits their cell during the night AND has a lantern in their inventory
        out += '\nLuckily, you have your trusty lantern. You turn it on and the corridor suddenly becomes a whole lot brighter. This might be your best chance at escaping! \nWant to (go back) to your cell or (proceed forward) down the corridor?'
    return out

def leave(obj): #returns the player to their cell
    return rooms.cell.welcome_back()
    
def go(obj): #determines the result of a 'go back' or 'proceed forward' command (proceed is parsed to 'go')
    if obj['object'] == 'back': #calls leave if the player chose to go back
        return leave(obj)
    if not state.state['night']: #kills the player and calls game_quit if they attempt to proceed forward during the day
        out = 'You take just a few steps forward into the corridor before a guard comes around the corner of the hall. Say your prayers. '
        out += common_actions.game_quit()
        return out
    elif state.state['night'] and 'lantern' in state.state['inventory']: #tells the player that they have won if they attempt to proceed forward during the night WITH the lantern in their inventory
        out = 'You quietly creep forward. No one has noticed you yet. Suddenly, you trip and drop your lantern! It doesn\'t break, but the sound echos through the halls.'
        out += '\nAlarms start going off. You start sprinting. Gunshots ring out around you. With the skill of a true master of the Matrix, you dodge the bullets.\Finally, you crash through a door and it opens to the outside. You breathe in your first breath of fresh air in weeks. You\'ve made it. You\'re out. You won!'
        state.state['dead'] = True #quits the program without printing 'you have died' like game_quit does
        return out
    else: #kills the player and calls game_quit if they attempt to proceed forward during the night without the lantern
        out = 'You can\'t see anything, so you pick a random direction and start running. Next thing you know, you run head first into the the prison director himself.\nHe\'s not known as one to show mercy.'
        out += common_actions.game_quit()
        return out

corridor_options = {  #connects the player's entered commands to the parser to account for different terms that mean the same thing
    'leave': leave,
    'go': go
}