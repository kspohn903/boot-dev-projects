from python_dsa_ch10_l12 import *
from user import *
import random

run_cases = [
    (
        4,
        [User(0), User(8), User(11), User(7)],
    ),
    (
        6,
        [User(0), User(9), User(5), User(17), User(16), User(10)],
    ),
]

submit_cases = run_cases + [
    (
        12,
        [
            User(11),
            User(10),
            User(18),
            User(17),
            User(19),
            User(2),
            User(23),
            User(27),
            User(33),
            User(30),
            User(22),
            User(34),
        ],
    ),
]


def test(num_characters, expected):
    characters = get_users(
        num_characters
    )  # Ensure this reflects your project structure
    bst = BSTNode()
    for character in characters:
        bst.insert(character)
    print("=====================================")
    print("Tree:")
    print("-------------------------------------")
    print(print_tree(bst))
    print("-------------------------------------\n")
    print(f"Expected: {expected}")
    try:
        actual = bst.postorder([])
        print(f"Actual:   {actual}")
        if expected == actual:
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
    return "\n".join(lines)


def format_tree_string(bst_node, lines, level=0):
    if bst_node is not None:
        format_tree_string(bst_node.right, lines, level + 1)
        lines.append(" " * 4 * level + "> " + str(bst_node.val))
        format_tree_string(bst_node.left, lines, level + 1)


test_cases = submit_cases
if "__RUN__" in globals():
    test_cases = run_cases

main()

