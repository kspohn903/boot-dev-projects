from python_dsa_ch10_l15 import *
from user import *

run_cases = [
    (2, 2),
    (6, 3),
]

submit_cases = run_cases + [
    (0, 0),
    (1, 1),
    (16, 7),
]


def test(num_users, expected_output):
    users = get_users(num_users)
    if not users:
        root = BSTNode()
    else:
        root = BSTNode(users[0])
        for user in users[1:]:
            root.insert(user)

    print("---------------------------------")
    print(f"Users: {[str(user) for user in users]}")
    print_tree(root)
    print(f"Expecting height: {expected_output}")
    result = root.height()
    print(f"Actual height: {result}")
    if result == expected_output:
        print("Pass")
        return True
    print("Fail")
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

