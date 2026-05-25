def calculate_guild_perms(*party_members_bin):
    # glorfindel, galadriel, elendil, elrond
    bin_register = 0b0000
    for party_member_bin in party_members_bin:
        bin_register |= party_member_bin
    return bin_register

