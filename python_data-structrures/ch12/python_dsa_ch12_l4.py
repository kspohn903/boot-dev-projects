class HashMap:
    def key_to_index(self, key):

        # Proper Instructions Live-Testing
        #"""
        # 1. Take the built-in hash of the key string
        # hashed_value = hash(key)
        
        # 2. Modulo by the size of the hashmap array to get a valid index
        # index = hashed_value % len(self.hashmap)
        
        # 3. Return the calculated index
        # return index
        # """

        # 1. Initialize an accumulator
        total = 0
        
        # 2. Add the unicode point values of each character in the string key
        for c in key:
            total += ord(c)
            
        # 3. Use the modulo operator against the hashmap size to get a 
        # bounded index
        return total % len(self.hashmap)

    # don't touch below this line

    def __init__(self, size):
        self.hashmap = [None for i in range(size)]

    def __repr__(self):
        buckets = []
        for v in self.hashmap:
            if v != None:
                buckets.append(v)
        return str(buckets)
