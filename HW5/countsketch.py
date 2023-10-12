import numpy as np
from numpy.random import zipf
import hashlib
from math import log
from statistics import median
import string
import random
from tqdm import tqdm


def is_power_of_two(n):
    """
    :param n: number to be checked
    :return: true if the number is power of two, false otherwise.
    """

    return (n != 0) and (n & (n-1) == 0)
    

def h(val, idx, k):
    """
    :param val: the value to be hashed
    :param idx: The index of the hash function
    :param k: the unvierse of each hash function 
    :return: A Unif(0,k-1) discrete random variable. However,
    if the same x is passed in, we will return the same exact
    Unif(0,k-1) rv.
    """

    assert(is_power_of_two(k))
    if (idx+1) * log(k, 2) > 256:
        print("Run out of bits in h() function")
        quit()
    bits = bin(int.from_bytes(hashlib.sha256(val.encode()).digest(), "little"))[2:].zfill(256)
    bits_for_h = bits[idx*(int(log(k, 2))):(idx+1)*(int(log(k, 2)))]
    assert(0 <= int(bits_for_h, 2) < k)
    return int(bits_for_h, 2)

def g(val, idx):
    """
    :param val: the value to be hashed
    :param idx: The index of the hash function 
    :return: A Unif{-1,1} discrete random variable.
    """
    if idx > 127:
        print("Run out of bits in g() function")
        quit()
    bits = bin(int.from_bytes(hashlib.md5(val.encode()).digest(), "little"))[2:].zfill(128)
    return int(bits[idx])*2-1

def countsketch(seq, t, k):
    """
    :param seq: the stream used to build the sketch. Each element in the stream is a pair (c,x)
    where c is a positive or negative number and x is the printable character (the value to be hashed).
    :param t: The number of the hash functions (number of rows in C)
    :param k: the unvierse of each hash function  (number of columns in C)
    :return: the sketch C and the new k as a data pair
    """
    k = next_power_of_2(k)  # Round up to the  next power of two
    print("k =", k)
    
    #pass # TODO: Your code here
    # add a line of code to initilaize your C sketch of the correct size to zero
    C = np.zeros((t, k))

    #Count Sketch
    # for pair in tqdm(seq): # the tqdm library will jsut siplay a progress bar when the code is running
    #     c, x = pair
        
    #     #pass # TODO: Your code here
    #     for j in range(t):
    #         C[j][h(x, j, k)] += c * g(x, j)
    #     # add lines of code to fill in the sketch according to algorithm in the lecture.
    #     # for the c_j in the algorithm, you can replace it with the vairable c defined in the line above.

    #CountMin Sketch
    for pair in tqdm(seq):
        c, x = pair
        
        for j in range(t):
            C[j][h(x, j, k)] += c
    return C, k

def next_power_of_2(x):
    """
    :param x: number to be checked
    :return: Round up to the  next power of two.
    """
    return 1 if x == 0 else 2**(x - 1).bit_length()



def createturnstilesequence(length):
    """
    :param length: the length of the stream to be generated
    :return: a stream of data pairs (c, x) of length long. For each pair in the stream
    c is a positive or negative number and x is the printable character.
    """
    a = 1.5
    weights = [1]+[x**(-a) for x in range(1, len(string.printable))]
    seq = []
    for _ in range(length):
        c = random.choice([-1, 1, 2]) # random counts
        l = random.choices(string.printable, weights=weights, k=1)[0]
        seq.append((c,l))
    return seq

def estimate(val, C, t, k):
    """
    :param val: the value to estimate the frequency for.
    :param C: the sketch created for the stream
    :param t: the number of hash functions used
    :param k: the universie of each hash function
    :return: the sketch C and the new k as a data pair
    
    Hint(s):
        1. Review the algorithm in the lecture on how to give an estimate of a value

    """
    #Count Sketch
    # freq_array = [None] * t
    # for x in range(t):
    #     freq_array[x] = g(val, x) * C[x][h(val, x, k)]
        
    # return median(freq_array)
    
    #Count Min
    freq_array = [None] * t
    for j in range(t):
        freq_array[j] = C[j][h(val, j, k)]
    return min(freq_array)
    #pass #TODO: Your code here
    
###### Main Program #######

stream_length = 10**5  #length of the generated stream
seq = createturnstilesequence(stream_length)

t = [1,2,3,4,5,6,7,8,9,10]
k_list = [32,64,128,256]
# t = 4       # the number of hash functions used
# k = 32      # the universe the of hash function

#iterate through values of k and t
for a in range(len(t)):
    for b in range(len(k_list)):
        C, k = countsketch(seq, t[a], k_list[b])  # compute the countsketch

        # find the true count of each printable character
        from collections import defaultdict
        truecounts = defaultdict(int)
        for (c, x) in seq:
            truecounts[x] += c


        # compare between the estimation and the true count
        error_ = 0
        i = 0
        for l in string.printable:
            est = estimate(l, C, t[a], k_list[b])
            true_count = truecounts[l]
            #print("*"+l+"*", "estimate", est, "true count", true_count)
            error_ += abs(true_count - est)
            i += 1

        print("for t = ", t[a], " k = ", k_list[b], " average absolute error = ", error_/i)