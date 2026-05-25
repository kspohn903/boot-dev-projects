from python_dsa_ch12_l5 import *
from user import *

run_cases = [
    (
        4,
        get_users(2),
        [
            None,
            None,
            ("Dave#3", User(3, 50, "Clerk")),
            ("Shelley#2", User(2, 51, "Clerk")),
        ],
    ),
]

submit_cases = run_cases + [
    (
        16,
        [
            User(9, 44, "Designer"),
            User(0, 47, "Engineer"),
            User(11, 21, "Engineer"),
            User(5, 54, "Engineer"),
            User(17, 57, "Engineer"),
            User(19, 40, "Engineer"),
        ],
        [
            ("Burry#9", User(9, 44, "Designer")),
            None,
            ("Blake#0", User(0, 47, "Engineer")),
            ("Shipley#11", User(11, 21, "Engineer")),
            None,
            None,
            None,
            ("John#5", User(5, 54, "Engineer")),
            None,
            None,
            ("Lippmann#17", User(17, 57, "Engineer")),
            None,
            ("Blake#19", User(19, 40, "Engineer")),
            None,
            None,
            None,
        ],
    ),
]


def test(size, users, expected_hashmap):
    print("---------------------------------")
    print(f"Inputs:")
    print(f" * HashMap size: {size}")
    hm = HashMap(size)
    try:
        for user in users:
            hm.insert(user.user_name, user)
            print(f"Inserted ({user.user_name}, {user})")

        print(f"Expected:")
        i = 0
        for item in expected_hashmap:
            print(f"  [{i}] {item}")
            i += 1

        actual = hashmap_to_list(hm)
        print(f"Actual:")
        i = 0
        for item in actual:
            print(f"  [{i}] {item}")
            i += 1

        if actual == expected_hashmap:
            print("Pass \n")
            return True
        print("Fail \n")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def hashmap_to_list(hm):
    return [v for v in hm.hashmap]


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

