from python_dsa_ch12_l4 import *
from user import *

run_cases = [
    (
        8,
        get_users(2),
        [3, 6],
    ),
]

submit_cases = run_cases + [
    (
        512,
        get_users(6),
        [360, 487, 150, 458, 112, 50],
    ),
]


def test(size, users, expected_indexes):
    print("---------------------------------")
    print(f" * HashMap size: {size}")
    hm = HashMap(size)
    try:
        actual = []
        for i, user in enumerate(users):
            index = hm.key_to_index(user.user_name)
            print(f"  Expect  {user.user_name} -> {expected_indexes[i]}")
            print(f"  Actual  {user.user_name} -> {index}")
            actual.append(index)
        if actual == expected_indexes:
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


test_cases = submit_cases
if "__RUN__" in globals():
    test_cases = run_cases

main()

