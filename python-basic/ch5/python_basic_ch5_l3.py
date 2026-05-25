def calculate_total_damage(spell_power, amp):
    return spell_power * amp

def take_magic_damage(health, resist, amp, spell_power):
    total_damage = calculate_total_damage(spell_power, amp)
    total_damage -= resist
    health -= total_damage
    return health



