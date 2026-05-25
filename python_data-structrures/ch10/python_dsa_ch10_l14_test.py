from python_dsa_ch10_l14 import BSTNode
from user import get_users, User


def populate_tree(nodes):
    if not nodes:
        return None
    tree = BSTNode(nodes[0])
    for node in nodes[1:]:
        tree.insert(node)
    return tree


run_cases = [
    (5, True),
    (3, False),
]

submit_cases = run_cases + [
    (1, True),
    (21, False),
    (17, True),
    (7, True),
]


def test(val_to_check, expected_output):
    print("---------------------------------")
    users = get_users(11)
    tree = populate_tree(users)
    user_to_find = User(val_to_check)
    print(f"Tree nodes:")
    for user in users:
        print(f" * {user}")
    print(f"Searching for: {user_to_find}")
    result = tree.exists(user_to_find)
    print(f"Expected: {expected_output}")
    print(f"Actual:   {result}")
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


test_cases = submit_cases
if "__RUN__" in globals():
    test_cases = run_cases

main()

