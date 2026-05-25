def area_of_circle(diameter):
    pi = 3.14
    radius = diameter / 2
    area = pi * radius * radius
    return area


sword_length = 1.0
spear_length = 2.0

# don't touch above this line

sword_area = area_of_circle(sword_length)
spear_area = area_of_circle(spear_length)

# don't touch below this line
print("Sword length: {:.2f} meters.\nSword attack area: {:.2f} square meters".format( sword_length, sword_area ) )
print("Spear length: {:.2f}\nSpear attack area: {:.2f} square meters".format( spear_length, spear_area ) )

