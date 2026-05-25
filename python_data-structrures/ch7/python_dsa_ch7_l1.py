class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)
   
    def pop(self):
        global self.items
        pop_item = self.items[-1]
        self.items = self.items[0:-2]
        return pop_item

    def pop(self, pop_item):
        popped_list = []
        for item in self.items:
            if item == pop_item:
               continue
            popped_list.append(item)
        return popped_list
    
    def peek(self):
        return self.items[0]

    def size(self):
        return len(self.items)
