# =============================================================
# You may define helper functions, but DO NOT MODIFY
# the parameters or names of the provided functions.

# Do NOT add any import statements.
# =============================================================

import mmh3
import numpy as np

class DistElts:
    def __init__(self, seed_offset:int=0):
        """
        :param seed_offset: Allows for multiple instances of this
        class to provide different results.
        
        We only use one variable, self.val, in our entire
        implementation.
        """
        self.seed_offset = seed_offset
        self.val = float("inf")

    def hashing(self, x:int) -> float:
        """
        :param x: The element to be hashed.
        :return: A Unif(0,1) continuous random variable. However,
        if the same x is passed in, we will return the same exact
        Unif(0,1) rv.
        """
        large_const = 2 ** 31
        h = mmh3.hash(x, self.seed_offset) % large_const + 1
        return h / large_const

    def update(self, x:int):
        """
        :param x: The new stream element.
        
        In this function, you'll update self.val as you described
        in the previous part.

        """
        #TODO one line
        self.val = min(self.val, self.hashing(x))

    def estimate(self) -> int:
        """        
        :return: Your estimate so far for the number of distinct
        elements you've seen. Make sure you round to the nearest
        integer!

        """
        return int((1/self.val) - 1)
        pass # TODO: Your code here (1 line)

class MultDistElts:
    def __init__(self, num_reps:int=1):
        """
        :param num_reps: How many copies of DistElts we have.

        Creates num_reps different DistElts objects, by passing in
        different seed_offsets.
        """
        self.num_reps = num_reps
        self.des = [DistElts(seed_offset=i) for i in range(num_reps)]

    def update(self, x:int):
        """
        :param x: The new stream element x.
        
        In this function, you'll call `update` for all the 
        DistElts objects in self.des.
        """
        pass # TODO: Your code here (2 lines)
        for i in self.des:
            i.update(x)

    def estimate(self) -> int:
        """        
        :return: Your estimate so far for the number of distinct
        elements you've seen. Here you will apply the DE* algorithm by taking
        the AVERAGE of the minsfrom your DistElts objects in self.des.

        """
        avg_distinct = 0
        for i in self.des:
            avg_distinct += i.val
        avg_distinct /= len(self.des)
        return int((1/avg_distinct) - 1)
        pass # TODO: Your code here (1-5 lines)

if __name__ == '__main__':
    # You can test out things here. Feel free to write anything below.
    stream = np.genfromtxt('./data/stream.txt', dtype='int')

    # 312 actual distinct Elements in the stream
    print("True Dist Elts: {}".format(312))

    # Create a DistElts object, and update for each element in the stream.
    # Finally, print out the estimate.
    de = DistElts()
    for x in stream:
        de.update(x)
    print("Dist Elts Estimate: {}".format(de.estimate()))

    # Create a MultDistElts object, and update for each element in the 
    # stream. Finally, print out the estimate.
    num_reps = 400   # You will be needing to vary this number to anwer question 2 in HW 3.
    mde = MultDistElts(num_reps=num_reps)
    for x in stream:
        mde.update(x)
    print("Mult Dist Elts Estimate with {} copies: {}".format(num_reps, mde.estimate()))
