class HashMap:
    def __init__(self, size):
        self.hashmap = [None for i in range(size)]

    def __repr__(self):
        buckets = []
        for v in self.hashmap:
            if v != None:
                buckets.append(v)
        return str(buckets)
    
    # don't touch below this line
    def get(self, key):
        try:
            i = self.key_to_index(key)
            bucket = self.hashmap[i]
            
            # Check if the bucket has data and the key matches
            if bucket is None or bucket[0] != key:
               raise Exception("sorry, key not found")
            
            # Key wasn't found in the slot
            return bucket[1]
            
        except Exception as ex:
            print(f"[EXCEPTION]: [{ex}]")
            raise ex
        except Error as err:
            print(f"[ERROR]: [{err}]")
            raise err

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
    def insert(self, key, value):
        # 1. Find the target index bucket for this key
        index = self.key_to_index(key)
        
        # 2. If the bucket is completely empty, initialize it as a list
        current_pair = self.hashmap[index]

        # 3. Check if the slot is empty, OR if the key matches (for an update)
        if current_pair is None or current_pair[0] == key:
            self.hashmap[index] = (key, value)
        else:
            # If the lesson eventually wants you to handle linear probing 
            # or another collision style, it goes here. 
            # For this test's expectations, just setting it 
            # directly fixes the structure mismatch.
            self.hashmap[index] = (key, value)

        ## 3. Check if the key already exists in this bucket (to update it)
        #for i, pair in enumerate(self.hashmap[index]):
        #    stored_key, stored_value = pair
        #    if stored_key == key:
        #        # Key found! Update the value in place and exit
        #        self.hashmap[index][i] = (key, value)
        #        return
                
        ## 4. If the key wasn't found in the bucket, append it as a new pair
        ## NOTE: This must sit OUTSIDE the for loop, otherwise it triggers 
        ## on the first mismatch!
        #self.hashmap[index].append((key, value))
