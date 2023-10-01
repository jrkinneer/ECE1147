# Do NOT add any import statements.
# =============================================================

import numpy as np
import mmh3

class BloomFilter:
    def __init__(self, k:int = 10, m:int=100000):
        """
        :param k: The number of hash functions (rows).
        :param m: The number of buckets (cols).

        Initializes the bloom filter to all zeros, as a
        boolean array where True = 1 and False = 0.
        
        """
        self.k = k
        self.m = m
        # self.t = np.zeros((k, m), dtype=bool)
        self.t = np.zeros(m, dtype=bool)

    def hashing(self, x, i:int) -> int:
        """
        :param x: The element x to be hashed.
        :param i: Which hash function to use, for i=0,...,self.k-1.
        :return: h_i(x) the ith hash function applied to x. We take the hash value and mod
        it by our table size. This consistent hashing function doesn't rely on
        randomness, and will uniformly distribute a set of n inputs across m buckets
        (even with different values of m, the distribution of inputs will still be
        roughly uniform)
        """
        return mmh3.hash(str(x), i) % self.m

    def insert(self, x):
        """
        :param x: The element to add to the bloom filter.
        
        In this function, we add x to our bloom filter.

        Hint(s):
        1. You will want to use self.hashing(...).
        2. We initialized our bit array to be of type
        boolean, so 1 should be represented as True, and 0 as 
        False.
        """
        for i in range(self.k):
            hash_result = self.hashing(x, i)
            # self.t[i][hash_result] = 1
            self.t[hash_result] = 1
            
            

    def check(self, x) -> bool:
        """
        :param x: The element to check whether or not it belongs
        to the bloom filter.
        :return: True or False; whether or not it is in the bloom filter.

        """
        is_present = True
        for i in range(self.k):
            # if (self.t[i][self.hashing(x, i)] == 0):
            #     is_present = False
            #     break
            if (self.t[self.hashing(x, i)] == 0):
                is_present = False
                break
            
        return is_present

if __name__ == '__main__':
    # You can test out things here. Feel free to write anything below.

    # Create a new bloom filter structure.
    bf = BloomFilter(k=10, m=79000) # 10 * 8,000 = 80,000 bits = 10 KB

    print("Adding malicious URLS to Bloom Filter")

    # Create our bloom filter of malicious URLs
    mal_urls = np.genfromtxt('data/mal_urls.txt', dtype='str')
    i = 0
    for mal_url in mal_urls:
        bf.insert(mal_url)
        i += 1
        assert bf.check(mal_url) # After adding, should definitely be in

    print("Computing False Positive Rate (FPR) on 10000 Unseen URLs")
    # Check contains on 10000 different URLs to see what percentage
    # incorrectly are marked as being contained.
    fpr = 0
    test_urls = np.genfromtxt('data/test_urls.txt', dtype='str')
    for test_url in test_urls:
        if bf.check(test_url): # Should ideally return False
            fpr += 1
    fpr /= len(test_urls)
    print("FPR: {}".format(fpr))
