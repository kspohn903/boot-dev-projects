from python_dsa_ch12_l9 import *

run_cases = [
    (
        [
            ("Billy Beane", 1),
            ("Peter Brand", 2),
            ("Art Howe", 3),
            ("Scott Hatteberg", 4),
            ("David Justice", 5),
            ("Ron Washington", 6),
            ("Paul DePodesta", 7),
        ],
        [
            (1.0, 1),
            (0.2, 10),
            (0.03, 100),
            (0.04, 100),
            (0.05, 100),
            (0.006, 1000),
            (0.007, 1000),
        ],
    )
]

submit_cases = run_cases + [
    (
        [
            ("Billy Beane", 1),
            ("Peter Brand", 2),
            ("Art Howe", 3),
            ("Scott Hatteberg", 4),
            ("David Justice", 5),
            ("Ron Washington", 6),
            ("Paul DePodesta", 7),
            ("Chad Bradford", 8),
        ],
        [
            (1.0, 1),
            (0.2, 10),
            (0.03, 100),
            (0.04, 100),
            (0.05, 100),
            (0.006, 1000),
            (0.007, 1000),
            (0.008, 1000),
        ],
    )
]


def test(items, expected_outputs):
    hm = HashMap(0)
    print("=====================================")
    actual = []
    for i, item in enumerate(items):
        key = item[0]
        val = item[1]
        expected_load = expected_outputs[i][0]
        expected_size = expected_outputs[i][1]
        print(f"insert({key}, {val})")
        try:
            hm.insert(key, val)
            print(f"Expect Load: {expected_load}")
            print(f"Actual Load: {hm.current_load()}")
            print(f"Expect Size: {expected_size}")
            print(f"Actual Size: {len(hm.hashmap)}")
            print("---------------------------------")
            actual.append((hm.current_load(), len(hm.hashmap)))
        except Exception as e:
            print(f"Error: {e}")
            print("Fail")
    print("=====================================")
    if actual == expected_outputs:
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

