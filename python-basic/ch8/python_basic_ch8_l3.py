def print_numbers_from_five_to(a=5, b=10):
    for i in range(a, b, 1):
        print(i)

# Don't edit below this line


def test(end, a=5):
    print(f"Using input end: {end}")
    print(f"Printing numbers from {a} to {end - 1}:")
    print_numbers_from_five_to(5, end)
    print("=====================================")


def main():
    values = [16, 6, 11]
    for value in values:
        test(value)
        
if __name__ == "__main__": 
   main()

