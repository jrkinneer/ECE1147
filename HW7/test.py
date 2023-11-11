matrix = [
    [0, 1, 0, 1],
    [0, 1, 0, 0],
    [1, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [1, 0, 0, 0],
    
]

# List of hash functions (e.g., using different constants for hashing)
hash_functions = [
    lambda x: (2 * x + 1) % 6,
    lambda x: (3 * x + 1) % 6,
    lambda x: (5 * x + 2) % 6,
    # Add more hash functions here if needed
]

def apply_hash_to_matrix(matrix, hash_funcs):
    hashed_matrices = []
    for hash_func in hash_funcs:
        hashed_matrix = []
        for row in matrix:
            hashed_row = [hash_func(element) for element in row]
            hashed_matrix.append(hashed_row)
        hashed_matrices.append(hashed_matrix)
    return hashed_matrices

def create_signature_matrix(hashed_matrices):
    signature_matrix = []
    for i in range(len(hashed_matrices[0])):
        signature_row = []
        for j in range(len(hashed_matrices[0][0])):
            min_hash = min(hashed_matrix[i][j] for hashed_matrix in hashed_matrices)
            signature_row.append(min_hash)
        signature_matrix.append(signature_row)
    return signature_matrix

# Apply hash functions to the matrix
hashed_matrices = apply_hash_to_matrix(matrix, hash_functions)

# Create the signature matrix
signature_matrix = create_signature_matrix(hashed_matrices)

print("Original Matrix:")
for row in matrix:
    print(row)

print("\nSignature Matrix:")
for row in signature_matrix:
    print(row)