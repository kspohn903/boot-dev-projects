import random
from python_dsa_ch11_l3 import *
from user import *
from ref import *  # ref module is hidden because it has the solution!

run_cases = [
    (4),
    (8),
]

submit_cases = run_cases + [
    (10),
]


def print_tree(node):
    lines = []
    format_tree_string(node.root, lines)
    print("\n".join(lines))


def format_tree_string(node, lines, level=0):
    if node.val is not None:
        format_tree_string(node.right, lines, level + 1)
        lines.append(
            " " * 4 * level
            + "> "
            + str(node.val)
            + " "
            + ("[red]" if node.red else "[black]")
        )
        format_tree_string(node.left, lines, level + 1)


def test(num_users):
    users = get_users(num_users)
    ref_tree = RBTree()
    for user in users:
        ref_implementation(ref_tree, user)
    print("============ NEW TEST ===============")
    actual_tree = RBTree()
    for user in users:
        print(f"Inserting {user} into tree...")
        actual_tree.insert(user)
    print("-------------------------------------")
    print("Expecting Tree:")
    print("-------------------------------------")
    print_tree(ref_tree)
    print("-------------------------------------")
    print("Actual Tree:")
    print("-------------------------------------")
    print_tree(actual_tree)
    print("-------------------------------------")
    if ref_inorder(actual_tree.root, []) == ref_inorder(ref_tree.root, []):
        print("Pass")
        return True
    print("Fail")
    return False


def main():
    passed = 0
    failed = 0
    skipped = len(submit_cases) - len(test_cases)
    for test_case in test_cases:
        correct = test(test_case)
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

