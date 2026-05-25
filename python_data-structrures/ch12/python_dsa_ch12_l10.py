class HashMap:
    def __init__(self, size):
        self.hashmap = [None for i in range(size)]

    def __repr__(self):
        result = ""
        for v in self.hashmap:
            if v != None:
               result += f" - {str(v)}\n"
        return result
    
    def resize(self):
        size = len(self.hashmap)
        if size == 0: 
           # If empty, initialize it to a base scale and update the state
           self.hashmap = [None]
           return
           
        # Use self. to look up the instance method
        current_load = self.current_load()
        if current_load < 0.05:
           return
        
        prev_hashmap = self.hashmap
        # Initialize the expanded array state inside the object first
        # so key_to_index uses the new length during re-hashing
        self.hashmap = [None for _ in range(10 * size)]
        
        # Re-hash all existing items into the expanded layout
        for bucket in prev_hashmap: 
            if bucket is not None:
               key, value = bucket
               # Calculate the new index based on the 10x size
               new_index = self.key_to_index(key)
               self.hashmap[new_index] = (key, value)

        return

    def current_load(self) -> float:
        size = len(self.hashmap)
        if(size == 0): 
          return 1.0
        filled_buckets = 0
        # sum_occupied = sum(1 if not None else 0)
        for el in self.hashmap:
            if el is None:
               continue
            filled_buckets += 1
        return filled_buckets / size
    
    # don't touch below this line
    def get(self, key):
        try:
            index = self.key_to_index(key)
            original_index = index
            size = len(self.hashmap)        
            while self.hashmap[index] is not None:
                # If we find the key, return just the value
                if self.hashmap[index][0] == key:
                    return self.hashmap[index][1]
                
                index = (index + 1) % size

                # If we've looped all the way around, stop searching
                if index == original_index:
                    break
                    
            raise Exception("sorry, key not found")
            
        except Exception as ex:
            raise ex

    def key_to_index(self, key):
        # 1. Initialize an accumulator
        total = 0 
        # 2. Add the unicode point values of each character in the string key
        for c in key:
            total += ord(c)
        # 3. Use the modulo operator against the hashmap size to get a 
        # bounded index
        return total % len(self.hashmap)

    # don't touch below this line
    def insert(self, key, value):
        # REMOVE or comment out self.resize() for this linear probing exercise
        # self.resize() 
        
        # resized_hashmap = self.resize()

        size = len(self.hashmap)
        index = self.key_to_index(key)
        original_index = index
        
        first_iteration = True

        while self.hashmap[index] is not None:
            if self.hashmap[index][0] == key:
               self.hashmap[index] = (key, value)
               return
                
            index = (index + 1) % size
            
            if index == original_index:
               first_iteration = False 
               raise Exception("hashmap is full")
                
        self.hashmap[index] = (key, value)
