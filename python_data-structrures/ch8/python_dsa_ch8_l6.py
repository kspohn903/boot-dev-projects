from queue import Queue

def matchmake(queue, user):
    # 1. Unpack the user tuple into name and action
    name, action = user

    # 2. Handle the "leave" action using the non-traditional method
    if action == "leave":
         queue.search_and_remove(name)

    # 3. Handle the "join" action by pushing the name onto the queue
    elif action == "join":
         queue.push(name)

    # 4. Check if the queue has at least 4 users in it
    if queue.size() >= 4:
        # Pop the first two users sequentially
        user1 = queue.pop()
        user2 = queue.pop()
        return f"{user1} matched {user2}!"

    # 5. If there are fewer than 4 users, no match can be made yet
    return "No match found"
