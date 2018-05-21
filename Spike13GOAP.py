from random import randrange


combat_goals = {'damage': 0, 'enemy': 20, 'mana': 0, 'aggro': 0}
combat_actions = {'weak attack': {'enemy': -2, 'damage': +1},
                  'strong attack': {'enemy': -3, 'damage': +2, 'mana': -1},
                  'minor heal': {'damage': -2, 'mana': +1, 'aggro': 2},
                  'major heal': {'damage': -3, 'mana': +2, 'aggro': 5},
                  'wander': {'mana': -2, 'aggro': 3}
                  }

def calculate_discontentment(act_val, cur_goals, in_combat):
    ft_goals = {}
    for goal_key in cur_goals.keys():
        ft_goals[goal_key] = cur_goals[goal_key]
    for goal, change in act_val.items():
        if goal == 'aggro':
            ft_goals[goal] = change
        elif change > 0:
            ft_goals[goal] = min(ft_goals[goal] + change, 10)
        else:
            ft_goals[goal] = max(ft_goals[goal] + change, 0)
    ret_dis = ft_goals['damage'] * 2 + ft_goals['mana']
    if in_combat:
        ret_dis += ft_goals['enemy']
    else:
        ret_dis += ft_goals['aggro']
    return ret_dis

def get_future_goals(action, cur_goals):
    ft_goals = cur_goals
    print(list(actions[action].items()))
    for goal, change in list(actions[action].items()):
        if goal == 'aggro':
            ft_goals[goal] = change
        elif change > 0:
            ft_goals[goal] = min(ft_goals[goal] + change, 10)
        else:
            ft_goals[goal] = max(ft_goals[goal] + change, 0)
    return ft_goals

def check_utility(action, goal):
    if goal in actions[action]:
        action_value = -(actions[action][goal])
        return action_value
    else:
        return 0

def perform_action(do_action):
    act = actions[do_action]
    for goal, change in act.items():
        if goal == 'aggro':
            goals[goal] = change
        elif change > 0:
            goals[goal] = min(goals[goal]+change, 10)
        else:
            goals[goal] = max(goals[goal]+change, 0)

def choose_action(in_combat):
    planned_moves = []
    ft_goals = {}
    for goal_key in goals.keys():
        ft_goals[goal_key] = goals[goal_key]
    discontentment = goals['damage'] + goals['mana']
    if in_combat:
        discontentment += goals['enemy']
    else:
        discontentment += goals['aggro']
    while len(planned_moves) < 5:
        future_discontentment = 100
        next_act = 'wander'
        for act_key in actions.keys():
            if ft_goals['damage'] < 2:
                if ((act_key == 'minor heal') or (act_key == 'major heal')):
                    continue
            elif ((act_key == 'wander') and (in_combat)):
                continue
            elif not in_combat:
                if ((act_key == 'weak attack') or (act_key == 'strong attack')):
                    continue
            act_val = actions[act_key]
            ret_dis = calculate_discontentment(act_val, ft_goals, in_combat)
            if ret_dis < future_discontentment:
                future_discontentment = ret_dis
                next_act = act_key
        planned_moves.append(next_act)
        ft_goals = get_future_goals(planned_moves[-1], ft_goals)
    return planned_moves
#    best_goal, best_goal_value = max(list(goals.items()), key=lambda item: item[1])
#    best_action = None
#    best_utility = None
#    for key, value in actions.items():
#        if best_goal in value:
#            if best_action is None:
#                best_action = key
#                best_utility = check_utility(best_action, best_goal)
#            else:
#                new_utility = check_utility(key, best_goal)
#                if new_utility > best_utility:
#                    best_action = key
#                    best_utility = new_utility
#    return best_action

def print_actions():
    print('Actions:')
    for name, effects in list(actions.items()):
        print(" * [%s]: %s" % (name, str(effects)))

#----------------------------------------------------------------------
#
#----------------------------------------------------------------------

def fight_until_finished():
    print_actions()
    print('3...2...1...Begin!')
    fighting = True
    in_combat = True
    while fighting:
        print('Goals:', goals)
        queued_actions = choose_action(in_combat)
        print('Planned actions:', queued_actions)
        for action in queued_actions:
            perform_action(action)
            print('New goals:', goals)
            if goals['damage'] >= 10:
                fighting = False
                print('Defeat!')
            elif ((goals['enemy'] == 0) and (in_combat)):
                in_combat = False
                print("Enemy defeated! Interrupting current actions.")
                break
            elif not in_combat:
                if randrange(10) < goals['aggro']:
                    in_combat = True
                    goals['enemy'] = 20
                    print("Enemy appeared! Interrupting current actions.")
                    break
        print('-------------------------')

#-----------------------------------------------------------
#
#-----------------------------------------------------------

if __name__ == '__main__':
    goals = combat_goals
    actions = combat_actions
    fight_until_finished()
