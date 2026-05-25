def print_status(player_health):
    if(player_health <= 0): 
       print("dead")
    print("status check complete")

# Don't edit below this line

def test(health):
    print(f"Player Health: {health}")
    print("Checking status...")
    print_status(health)
    print("=====================================")


def main():
    values = [0, 5, -1, 3]
    for val in values:
        test(val)


if __name__ == "__main__":
   main()

