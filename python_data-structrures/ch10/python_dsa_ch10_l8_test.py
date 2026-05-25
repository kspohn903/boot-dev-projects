import random
from python_dsa_ch10_l8 import *
from user import *
from ref import *  # ref module is hidden because it has the solution!

run_cases = [
    (6, 2, [User(0), User(9), User(16), User(17)]),
    (
        12,
        4,
        [
            User(2),
            User(10),
            User(11),
            User(17),
            User(22),
            User(27),
            User(30),
            User(33),
        ],
    ),
]

submit_cases = run_cases + [
    (
        24,
        6,
        [
            User(2),
            User(3),
            User(9),
            User(10),
            User(12),
            User(16),
            User(18),
            User(19),
            User(22),
            User(23),
            User(35),
            User(39),
            User(45),
            User(51),
            User(54),
            User(68),
            User(69),
            User(70),
        ],
    ),
]


def test(num_users, num_to_delete, expected):
    users = get_users(num_users)
    users_copy = users.copy()
    random.shuffle(users_copy)
    users_to_delete = users_copy[:num_to_delete]
    bst = BSTNode()
    for user in users:
        bst.insert(user)
    print("=====================================")
    print("Tree:")
    print_tree(bst)
    print("-------------------------------------\n")
    try:
        actual_bst = BSTNode()
        for user in users:
            actual_bst.insert(user)
        print("Deleting users: " + str(users_to_delete))
        for user in users_to_delete:
            actual_bst = actual_bst.delete(user)
        print("Actual Tree:")
        print_tree(actual_bst)
        print("-------------------------------------")
        actual = ref_inorder(actual_bst, [])
        print(f"Expected: {expected}")
        print(f"Actual:   {actual}")
        if expected == actual:
            print("Pass \n")
            return True
        print("Fail \n")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def print_tree(bst_node):
    if bst_node is not None:
        lines = []
        format_tree_string(bst_node, lines)
        for line in lines:
            print(line)


def format_tree_string(bst_node, lines, level=0):
    if bst_node is not None:
        format_tree_string(bst_node.right, lines, level + 1)
        lines.append(" " * 4 * level + "> " + str(bst_node.val))
        format_tree_string(bst_node.left, lines, level + 1)


def main():
    passed = 0
    failed = 0
    skipped = len(submit_cases) - len(test_cases)
    for test_case in test_cases:
        correct = test(*test_case)
        if correct:
            passed += 1
        else:
            failed += 1
    if failed == 0:
        print("============= PASS ==============")
    else:
        print("============= FAIL ==============")
    if skipped > 0:
        print(f"{passed} passed, {failed} failed, {skipped} skipped")
    else:
        print(f"{passed} passed, {failed} failed")


test_cases = submit_cases
if "__RUN__" in globals():
    test_cases = run_cases

main()

