import random
from python_dsa_ch10_l7 import *
from user import *

run_cases = [
    (5, "Blake#0", "Carrell#14"),
    (10, "Ricky#1", "Vennett#29"),
]

submit_cases = run_cases + [
    (15, "Shelley#2", "George#42"),
]


def test(num_users, min_user, max_user):
    users = get_users(num_users)
    bst = BSTNode()
    for user in users:
        bst.insert(user)
    print("=====================================")
    print("Tree:")
    print("-------------------------------------")
    print_tree(bst)
    print("-------------------------------------\n")
    print(f"Expected min: {min_user}, max: {max_user}")
    try:
        actual_min = bst.get_min()
        actual_max = bst.get_max()
        print(f"Actual min: {actual_min.user_name}, max: {actual_max.user_name}")
        if actual_max.user_name == max_user and actual_min.user_name == min_user:
            print("Pass \n")
            return True
        print("Fail \n")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


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


def print_tree(bst_node):
    lines = []
    format_tree_string(bst_node, lines)
    print("\n".join(lines))


def format_tree_string(bst_node, lines, level=0):
    if bst_node is not None:
        format_tree_string(bst_node.right, lines, level + 1)
        lines.append(" " * 4 * level + "> " + str(bst_node.val))
        format_tree_string(bst_node.left, lines, level + 1)


test_cases = submit_cases
if "__RUN__" in globals():
    test_cases = run_cases

main()

