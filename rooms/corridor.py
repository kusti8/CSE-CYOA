import state
import common_actions
import rooms.cell

def welcome():
    out = 'You got out of your cell! Congratulations. However, the adventure is not done yet. You still have to get through the corridor and outside. You have people outside who are ready to pick you up. You\'re in the final stretch. Don\'t mess it up.'
    if not state.state['night']:
        out += '\nThe sun is blinding you and there are guards everywhere. You can just barely see the end. There are guards everywhere and not many places to run.'
    else:
        out += '\nIt is dark and hard to see. There seem to be less guards during the night. You are pretty sure you need to go forward.'
    if state.state['night'] and 'lantern' in state.state['inventory']:
        out += '\nLuckily, you have your trusty lantern. The corridor suddenly becomes a whole lot brighter. You can\'t see the end, but there are no guards in sight.'

def leave(obj):
    return rooms.cell.welcome_back()
    
def go(obj):
    if not state.state['night']:
        out = 'You only take a step forward, but you already manage to trip on the flat concrete ground. A guard comes up and towers over you. "This feels just like middle school," you think. I\'m sorry, but you did not survive.'
        out += common_actions.game_quit()
        return out
    elif state.state['night'] and 'lantern' in state.state['inventory']:
        out = 'You quietly creep forward. No one has heard you yet. But then you drop your lantern. It doesn\'t break, but everyone in the prison can hear it. Alarms start going off.'
        out += 'You start sprinting. Gunshots are ringing out everywhere. You dodge them with the skills that you learned from The Matrix. You crash into the door and it opens. You breathe in your first breath of fresh air in weeks. You made it. You\'re out. You won!'
        state.state['dead'] = True
        return out
    else:
        out = 'You can\'t see anything, so you pick a random direction and start running. Next thing you know, you\'ve run head first into the prison directory. He spares no mercy.'
        out += common_actions.game_quit()
        return out

corridor_options = {
    'leave': leave,
    'go': go
}