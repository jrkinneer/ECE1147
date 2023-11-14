import hashlib
import numpy as np

#hash functions for random permutations
def hash_function(data):
    hash_object = hashlib.sha256(data.encode())
    return int(hash_object.hexdigest(), 16)

#generates permutations matrix
def generate_permutations(shingles, num_functions):
    permutations = np.zeros((shingles.shape[0], num_functions)).astype('uint8')
    rows = [i for i in range(shingles.shape[0])]
    
    for i in range(num_functions):
        hash_key = np.sum(shingles[i, :])
        hashed_list = [(index, hash_function(str(i) + str(hash_key) + str(index))) for index in rows]
        hashed_list.sort(key=lambda x: x[1])
        permutation = [item[0] for item in hashed_list]
        permutations[:,i] = np.array(permutation)

    return permutations

#creates signature matrix from shingles and permutations matrices
def signature_matrix(shingles, permutations):
    signature_mat = np.zeros((permutations.shape[1], shingles.shape[1]))
    
    for shingle_column in range(shingles.shape[1]):    
        for perm_column in range(permutations.shape[1]):
            perm_row = 0
            while (shingles[ permutations[perm_row][perm_column] ][shingle_column] != 1):
                perm_row += 1
            signature_mat[perm_column][shingle_column] = perm_row
                 
    return signature_mat

#gets jaccard similartiy of each column pair
def jaccard_sim(signature_matrix):
    jaccard_similarity = np.zeros((signature_matrix.shape[1], signature_matrix.shape[1]))
    for i in range(signature_matrix.shape[1]):
        for j in range(i+1, signature_matrix.shape[1]):
            set1 = signature_matrix[:, i]
            set2 = signature_matrix[:, j]
            intersection = 0
            union = len(set1)
            for k in range(len(set1)):
                if set1[k] == set2[k]:
                    intersection += 1
                    
            similarity = intersection/union if union !=0 else 0
            jaccard_similarity[i,j] = similarity
            jaccard_similarity[j,i] = similarity
    return jaccard_similarity

#returns the false positive rate and false negative rate, in that order
def FPR_FNR(b, r, s, t):
    
    #prob that at least one band is identical using t
    x = 1 - (1-(t**r))**b
    #prob that at least one band is identical using s
    y = 1 - (1-(s**r))**b
    
    FPR = 1 - y
    FNR = y
    
    return (FPR, FNR)
   
shingles_documents = np.array([[1,0,1,0],
                               [1,0,0,1],
                               [0,1,0,1],
                               [0,1,0,1],
                               [0,1,0,1],
                               [1,0,1,0],
                               [1,0,1,0]], dtype='uint8')

# test_perm = np.array([[1,3,2],
#                       [2,1,3],
#                       [6,0,6],
#                       [5,2,1],
#                       [0,5,5],
#                       [4,6,0],
#                       [3,4,4]
#                       ])
test_perm = np.array([[4,2,5],
                      [0,1,3],
                      [1,3,0],
                      [6,0,1],
                      [5,6,6],
                      [3,4,4],
                      [2,5,2]
                      ]) 
    
#coding question 1a result
sig_mat = signature_matrix(shingles_documents, test_perm)
print(sig_mat)
#coding question 1b result
print(jaccard_sim(sig_mat))

#coding question 1c result
print(FPR_FNR(20,5,.8,.8))
# print(sig_mat+1)
# perm = generate_permutations(shingles_documents, 3)
# print(perm)