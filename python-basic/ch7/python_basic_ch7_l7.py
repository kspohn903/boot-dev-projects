def check_high_score(current_player_name, high_scoring_player_name):
    status_string = "are" if (current_player_name == high_scoring_player_name) else "are not"
    return f"You {status_string} the highest scoring player!"

