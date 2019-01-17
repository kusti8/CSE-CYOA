state = { #contains state variables that apply to the player at all times
    'day': 1, #keeps track of day number
    'inventory': [], #keeps track of player inventory contents
    'inventory_limit': 2, #initial inventory limit of 2, set to 6 if they acquire a backpack
    'last_day_eaten': 1, #keeps track of how long since the player has last eaten
    'dead': False, #set to true when game lost or won to trigger program termination
    'painting_got': False, #keeps track of if the player has removed the painting on their cell wall
    'execution_posted': False, #keeps track of if the player has been told about their execution date yet or not
    'bowl_flipped': False, #keeps track of if the player has flipped their food bowl in their cell
    'location': 'cell', #keeps track of the player's room location
    'sub_location': 'tables', #keeps track of the player's location within a room if it has multiple sub-locations
    'ceiling_pushed': False, #keeps track of if the player has opened the crevice in the bathroom ceiling yet
    'shop_inventory': ['lantern', 'key', 'backpack', 'lambo'], #keeps track of items still avaliable at the black market
    'fake_sleep': False, #keeps track of if the player has gained the ability to pretend to sleep in their cell yet
    'night': False #keeps track of if it is nighttime or daytime
}