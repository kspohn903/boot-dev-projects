#                    [sword, arrow, spear, dagger], [fireball]
def calculate_damage(*dmg_sources):
    total_damage = 0
    average_damage = 0
    total_damage += sum(dmg_sources)
    n_damage_sources = len(dmg_sources)
    average_damage = total_damage / n_damage_sources

    return total_damage, average_damage

