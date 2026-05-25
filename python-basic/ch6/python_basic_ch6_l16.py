def binary_string_to_int(num_servers, num_players, num_admins):
    # Convert each binary string to an integer using base 2
    servers_int = int(num_servers, 2)
    players_int = int(num_players, 2)
    admins_int = int(num_admins, 2)
    
    # Return all three converted values
    return servers_int, players_int, admins_int
