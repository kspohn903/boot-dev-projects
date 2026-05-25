def create_stats_message(strength, wisdom, dexterity):
    stat_total = strength + wisdom + dexterity
    # stats_pool = (strength, wisdom, dexterity)
    msg = f"You have {strength} strength, {wisdom} wisdom, and {dexterity} dexterity for a total of {stat_total} stats."
    return msg

