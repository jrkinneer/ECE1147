import hashlib
import numpy as np

def hash_function(data):
    # You can use different hash functions based on your requirements
    hash_object = hashlib.sha256(data.encode())
    return int(hash_object.hexdigest(), 16)

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

def signature_matrix(shingles, permutations):
    signature_mat = np.zeros((permutations.shape[1], shingles.shape[1]))
    
    for shingle_column in range(shingles.shape[1]):    
        for perm_column in range(permutations.shape[1]):
            perm_row = 0
            while (shingles[ permutations[perm_row][perm_column] ][shingle_column] != 1):
                perm_row += 1
            signature_mat[perm_column][shingle_column] = perm_row
                 
    return signature_mat

# Example usage:

shingles_documents = np.array([[1,0,1,0],
                               [1,0,0,1],
                               [0,1,0,1],
                               [0,1,0,1],
                               [0,1,0,1],
                               [1,0,1,0],
                               [1,0,1,0]])

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

def jaccard_sim(shingles):
    jaccard_similarity = np.zeros((shingles.shape[1], shingles.shape[1]))
    for i in range(shingles.shape[1]):
        for j in range(i+1, shingles.shape[1]):
            set1 = set(shingles[:, i])
            set2 = set(shingles[:, j])
            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            similarity = intersection/union if union !=0 else 0
            jaccard_similarity[i,j] = similarity
            jaccard_similarity[j,i] = similarity
    return jaccard_similarity

print(jaccard_sim(shingles_documents))
# sig_mat = signature_matrix(shingles_documents, test_perm)
# print(sig_mat+1)
# perm = generate_permutations(shingles_documents, 3)
# print(perm)