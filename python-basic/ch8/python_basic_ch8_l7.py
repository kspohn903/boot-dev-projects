
def count_down(start, end):
    for i in range(start, end, -1):
        print(i)

# Don't edit below this line


def test(start, end):
    print(f"Using inputs start: {start} and end: {end}")
    print(f"Printing numbers from {start} to {end + 1}:")
    count_down(start, end)
    print("=====================================")


def main():
    start_values = [10,20,15]
    end_values = [0,10,11]
    for i in range(len(start_values)):
        test(start_values[i], end_values[i])

if __name__ == "__main__": 
   main()
