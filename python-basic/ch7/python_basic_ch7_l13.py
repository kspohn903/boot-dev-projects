def combat_evaluation(player_power, enemy_defense):
    advantage, disadvantage, evenly_matched = False, False, False
    advantage = (player_power > enemy_defense)
    evenly_matched = (player_power == enemy_defense)
    disadvantage = (player_power < enemy_defense)
    # your code here
    return advantage, disadvantage, evenly_matched

