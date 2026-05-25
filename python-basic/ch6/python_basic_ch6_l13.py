can_create_guild = 0b1000
can_review_guild = 0b0100
can_delete_guild = 0b0010
can_edit_guild = 0b0001

def get_create_bits(user_permissions):
    # AND the user's bits with the 'create' permission bit
    return user_permissions & can_create_guild


def get_review_bits(user_permissions):
    # AND the user's bits with the 'review' permission bit
    return user_permissions & can_review_guild


def get_delete_bits(user_permissions):
    # AND the user's bits with the 'delete' permission bit
    return user_permissions & can_delete_guild


def get_edit_bits(user_permissions):
    # AND the user's bits with the 'edit' permission bit
    return user_permissions & can_edit_guild
