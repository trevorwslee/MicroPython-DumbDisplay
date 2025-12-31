

_init_action = {'satiety': 100, 'toilet': 100, 'happy': 100, 'health': 100, 'logiki': 50}

action = _init_action.copy()

def reset_action():
    global action
    action = _init_action.copy()

