from python_oop_ch5_l1 import *

run_cases = [
    ("Faramir", "Human", None),
    ("Bard", "Archer", 1),
]

submit_cases = run_cases + [
    ("Boromir", "Human", None),
    ("Aragorn", "Human", None),
    ("Legolas", "Archer", 93828),
]


def test_inheritance():
    print("---------------------------------")
    print("Inheritance Test:")
    if "Archer" not in globals():
        print("Archer class not found")
        return False
    if "Human" not in globals():
        print("Human class not found")
        return False
    if not issubclass(Archer, Human):
        print("Archer is not a child class of Human")
        return False
    print("Archer is a child class of Human")
    return True


def test(name, type, num_arrows):
    print("---------------------------------")
    print(f"Type:   {type}")
    print(f"Name:   {name}")
    if type == "Archer":
        print(f"Arrows: {num_arrows}")
    print("")
    try:
        if type == "Human":
            human = Human(name)
            print(f"Expecting name: {name}")
            print(f"Actual name:    {human.get_name()}")
            if human.get_name() == name:
                return True
            else:
                return False
        else:
            archer = Archer(name, num_arrows)
            print(f"Expecting name:   {name}")
            print(f"Actual name:      {archer.get_name()}")
            print(f"Expecting arrows: {num_arrows}")
            print(f"Actual arrows:    {archer.get_num_arrows()}")
            if archer.get_name() == name and archer.get_num_arrows() == num_arrows:
                return True
            else:
                return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    passed = 0
    failed = 0
    skipped = len(submit_cases) - len(test_cases)
    correct = test_inheritance()
    if correct:
        print("Pass")
        passed += 1
    else:
        print("Fail")
        failed += 1
    for test_case in test_cases:
        correct = test(*test_case)
        if correct:
            print("Pass")
            passed += 1
        else:
            print("Fail")
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

