#include "helper.h"
#include <iostream>
#include <vector>
#include <algorithm>
#include <math.h>
#include <thread>

void strassen(vector<vector<int>> &strassen_a, vector<vector<int>> &strassen_b, vector<vector<int>> &strassen_c, int size);
void test(vector<double> &times,int MATRIX_SIZE);

int main(){
//run the test functions with matrix sizes from 2^2 to 2^16

    int size = 0;
    vector<vector<double>> times;
    vector<int> sizes;
    for(int i=2; i<16;i++){
        vector<double> time_array;
        size=pow(2,i);
        sizes.push_back(size);
        std::cout << "Starting " << size << std::endl;
        test(time_array, size);
        std::cout << "Finished " << size << std::endl;
        times.push_back(time_array);
        std::cout << std::endl;
        std::cout << "----------------------------------------------------" << std::endl;
        std::cout << std::endl;
    }
    
    //print out the times vector
    for(int i=0; i<times.size(); i++){
        std::cout << "Size: " << sizes[i] << std::endl;
        for(int j=0; j<times[i].size(); j++){
            std::cout << times[i][j] << " ";
        }
        std::cout << std::endl;
    }

    return 0;

}

//cache efficient brute force multiplication to speed up run time of all matrix multiplication functions
void cache_efficient_mult(vector<vector<int>> &matrix_a, vector<vector<int>> &matrix_b, vector<vector<int>> &matrix_c, int n){
    //square matrices of ints, for strassen
    vector<int> Bcolj(n);
    for(int j = 0; j < n; j++){
        for (int k = 0; k < n; k++){
            Bcolj[k] = matrix_b[k][j];
        }
        for (int i = 0; i< n; i++){
            int s = 0;
            for (int k = 0; k < n; k++){
                s += matrix_a[i][k] * Bcolj[k];
            }
            matrix_c[j][i] = s;
        }
    }
    return;
}

void cache_efficient_mult(vector<vector<float>> &matrix_a, vector<vector<float>> &matrix_b, vector<vector<float>> &matrix_c){
    //uneven sized matrices for uniform and non uniform approximation
    int n = matrix_a.size();
    int s = matrix_a[0].size();
    int m = matrix_b[0].size();
    vector<float> Bcolj(s);
    for(int j = 0; j < m; j++){
        for (int k = 0; k < s; k++){
            Bcolj[k] = matrix_b[k][j];
        }
        for (int i = 0; i< n; i++){
            float sum = 0;
            for (int k = 0; k < s; k++){
                sum += matrix_a[i][k] * Bcolj[k];
            }
            matrix_c[j][i] = sum;
        }
    }
    return;
}

void cache_efficient_mult(vector<vector<int>> &matrix_a, vector<vector<int>> &matrix_b, vector<vector<float>> &matrix_c, int n){
    //square matrices of ints A and B into matrix of floats C, for brute force
    vector<int> Bcolj(n);
    for(int j = 0; j < n; j++){
        for (int k = 0; k < n; k++){
            Bcolj[k] = matrix_b[k][j];
        }
        for (int i = 0; i< n; i++){
            float s = 0;
            for (int k = 0; k < n; k++){
                s += matrix_a[i][k] * Bcolj[k];
            }
            matrix_c[j][i] = s;
        }
    }
    return;
}

void test(vector<double> &times,int MATRIX_SIZE){
    // multpliy two matrices of size MATRIX_SIZE and store the time taken for the operation in the times vector
    
    // Initialize the random number generator
    srand(time(NULL));

    //Declare three matrices
    vector<vector<int>> matrix_a(MATRIX_SIZE, vector<int>(MATRIX_SIZE));
    vector<vector<int>> matrix_b(MATRIX_SIZE, vector<int>(MATRIX_SIZE));
    vector<vector<float>> matrix_c(MATRIX_SIZE, vector<float>(MATRIX_SIZE));
    //Initialize the matrices with random numbers between 0 and 20
    for(int i = 0; i < MATRIX_SIZE; i++){
        for(int j = 0; j < MATRIX_SIZE; j++){
            matrix_a[i][j] = 1+ (rand() % 21);
            matrix_b[i][j] = 1+ (rand() % 21);
        }
    }
    
    std::cout << "----------------------------------------------------" << std::endl;
    std::cout <<"Brute Force\n";

    //Declare the result matrix

    //Multiply the matrices and time how long it take
    clock_t start = clock();

    // TODO
    // implement Brute Force matrix multiplication here
    //std::cout<<"matrix_c = " << std::endl;
    // for (int i = 0; i < MATRIX_SIZE; i++){
    //     for (int j = 0; j < MATRIX_SIZE; j++){
    //         matrix_c[i][j] = 0;
    //         for (int k = 0; k < MATRIX_SIZE; k++){
    //             matrix_c[i][j] += matrix_a[i][k] * matrix_b[k][j];
    //         }
    //     }
    // }
    cache_efficient_mult(matrix_a, matrix_b, matrix_c, MATRIX_SIZE);
    
    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    std::cout << "Time spent: " << time_spent << " seconds" << std::endl;
    times.push_back(time_spent);

    
    //print section
    std::cout << "----------------------------------------------------" << std::endl;
    std::cout <<"Approximate Uniform\n";
    // the smapling factor, how many submatrices will be chosen out
    double subsampling_factor = .8;
    int new_matrix_size = ceil(MATRIX_SIZE * subsampling_factor);
   
    //begin timining 
    start = clock();

	// TODO:
	// Generate a random vector of indices with the matrix size
	// look how to use std::random_shuffle
    vector<int> all_indices;
    for (int i = 0; i < MATRIX_SIZE; i++){
        all_indices.push_back(i);
    }
    vector<int> selected_ind;
    for (int i = 0; i < new_matrix_size; i++){
        std::random_shuffle(all_indices.begin(), all_indices.end());
        selected_ind.push_back(all_indices[0]);
    }
    
    //create new matrices C and R with the new samples cols and rows, and a new matrix CR to hold the approx product
    // don't forgoet to normalize as we did in the lecture.
    vector<vector<float>> vector_C(MATRIX_SIZE, vector<float>(new_matrix_size));
    vector<vector<float>> vector_R(new_matrix_size, vector<float>(MATRIX_SIZE));
    vector<vector<float>> CR(MATRIX_SIZE, vector<float>(MATRIX_SIZE));


    for (int i = 0; i < MATRIX_SIZE; i++){
        for (int j = 0; j < new_matrix_size; j++){
            double denom = 
            vector_C[i][j] = matrix_a[i][selected_ind[j]];
        }
    }

    for (int i = 0; i < new_matrix_size; i++){
        for (int j = 0; j < MATRIX_SIZE; j++){
            vector_R[i][j] = matrix_b[selected_ind[i]][j];
        }
    }
    
    //multiply C and R using Brute Force.
    //std::cout<<"CR = " << std::endl;
    // for (int i = 0; i < MATRIX_SIZE; i++){
    //     for (int j = 0; j < MATRIX_SIZE; j++){
    //         CR[i][j] = 0;
    //         for (int k = 0; k < new_matrix_size; k++){
    //             CR[i][j] += vector_C[i][k] * vector_R[k][j];
    //         }
    //         //std::cout<<CR[i][j]<<"\t";
    //     }
    //     //std::cout<<"\n";
    // }
    cache_efficient_mult(vector_C, vector_R, CR);
    
    //end timing
    end = clock();
    std::cout << "New matrix A\n";

    time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    times.push_back(time_spent);
    std::cout << "Time spent: " << time_spent << " seconds" << std::endl;
    
    //TODO:
    //Calcualte the frobenius norm of CR-AB which is the difference between the approximate matrix and the correct answer (you can use the answer from the brute force algorithm)
    //use the helper fucntion to help you out.
    //put the error in the error_uni varialbe defined below.
    
    float error_uni;
    vector<vector<float>> difference(MATRIX_SIZE, vector<float>(MATRIX_SIZE));
    
    matrix_diff(CR, matrix_c, difference);
    // std::cout<<"difference matrix = " << std::endl;
    // for (int i = 0; i < MATRIX_SIZE; i++){
    //     for (int j = 0; j < MATRIX_SIZE; j++){
    //         std::cout<<difference[i][j]<<"\t";
    //     }
    //     std::cout<<"\n";
    // }
    error_uni = frobenius_norm (difference);

    std::cout << "Uniform Error: " << error_uni << std::endl;

    std::cout << "----------------------------------------------------" << std::endl;
    std::cout <<"Approximate nonuniform\n";
    

    //begin timing
    start = clock();
    //generate the probability vector according to a probabilty distribution which is proportional to the spectral norm fo the matrices
    vector<float> A_prob(MATRIX_SIZE), rand_nonuniform(MATRIX_SIZE),B_prob(MATRIX_SIZE);
    float sum = 0.0;
    for(int i = 0; i < MATRIX_SIZE; i++){
        A_prob[i] = euclidean_norm_rows(matrix_a, i);
        B_prob[i] = euclidean_norm_cols(matrix_b, i);
        rand_nonuniform[i] =  A_prob[i] * B_prob[i];
        sum +=rand_nonuniform[i];
    }
    std::random_device rd;
    std::mt19937 gen(rd());
    std::discrete_distribution<> dist(rand_nonuniform.begin(), rand_nonuniform.end());
    vector<int> rand_arr(new_matrix_size);

    //print new_matrix_size
    std::cout << "New matrix size: " << new_matrix_size << std::endl;
    vector<vector<float>> A_rand(MATRIX_SIZE, vector<float>(new_matrix_size));
    vector<vector<float>> B_rand(new_matrix_size, vector<float>(MATRIX_SIZE));
    vector<vector<float>> C_rand(MATRIX_SIZE, vector<float>(MATRIX_SIZE));

    //if i is in the sampling vector, then set the value to the matrix B
    int b_index = 0;
    for(int i = 0; i < new_matrix_size; i++){
        rand_arr[i] = dist(gen);
        for(int j = 0; j < MATRIX_SIZE; j++){
            B_rand[i][j] = matrix_b[rand_arr[i]][j] / sqrt(((rand_nonuniform[rand_arr[i]]/sum) * (new_matrix_size)));
        }
        b_index++;
    }
        
    int a_index = 0;
    for(int i = 0; i < MATRIX_SIZE; i++){
        a_index = 0;
        for(int j = 0; j < new_matrix_size; j++){
            A_rand[i][j] = matrix_a[i][rand_arr[j]] / sqrt(((rand_nonuniform[rand_arr[j]]/sum) * (new_matrix_size)));;
            a_index++;
        }
    }

	//TODO:
    //multiply the new matrices using Brute Force.
    // for (int i = 0; i < MATRIX_SIZE; i++){
    //     for (int j = 0; j < MATRIX_SIZE; j++){
    //         C_rand[i][j] = 0;
    //         for (int k = 0; k < new_matrix_size; k++){
    //             C_rand[i][j] += A_rand[i][k] * B_rand[k][j];
    //         }
    //     }
    // }
    cache_efficient_mult(A_rand, B_rand, C_rand);
    //end timing
    end = clock();

    //print time spent
    time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    std::cout << "Time spent: " << time_spent << " seconds" << std::endl;
    times.push_back(time_spent);
    
	//TODO:
    //Calcualte the frobenius norm of CR-AB which is the difference between the approximate matrix and the correct answer (you can use the answer from the brute force algorithm)
    //use the helper fucntion to help you out.
    //put the error in the error_non_uni varialbe defined below.
    
    float error_non_uni;
    vector<vector<float>> difference_2(MATRIX_SIZE, vector<float>(MATRIX_SIZE));
    matrix_diff(C_rand, matrix_c, difference_2);
    error_non_uni = frobenius_norm (difference_2);
    std::cout << "Non-Uniform Error: " << error_non_uni << std::endl;
    
    //print section
    std::cout << "----------------------------------------------------" << std::endl;
    std::cout <<"Strassen\n";
   
    //Strassesn algorithm
    vector<vector<int>> strassen_a(MATRIX_SIZE, vector<int>(MATRIX_SIZE));
    vector<vector<int>> strassen_b(MATRIX_SIZE, vector<int>(MATRIX_SIZE));
    vector<vector<int>> strassen_c(MATRIX_SIZE, vector<int>(MATRIX_SIZE));

    //copy the matrices to the int matrices
    for(int i = 0; i < MATRIX_SIZE; i++){
        for(int j = 0; j < MATRIX_SIZE; j++){
            strassen_a[i][j] = matrix_a[i][j];
            strassen_b[i][j] = matrix_b[i][j];
        }
    }


    //begin timing
    start = clock();

    //TODO:
    // use the strassen fuction to multiply the strassen_a and strassen_b and put the result in strassen_c
    strassen(strassen_a, strassen_b, strassen_c, MATRIX_SIZE);

    //end timing
    end = clock();

    
    //print time spent
    time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    std::cout << "Time spent: " << time_spent << " seconds" << std::endl;
    times.push_back(time_spent);

    //print 
    std::cout << "----------------------------------------------------" << std::endl;
    
}

//matrix multiplication using strassen algorithm and divide and conquor
void strassen(vector<vector<int>> &strassen_a, vector<vector<int>> &strassen_b, vector<vector<int>> &strassen_c, int size)
{
	//TODO
	
	// strassen_a and strassen_b are teh amtrices to be multiplied and strassen_c is the output matrix.
	// all the matrices are of the same size which is the 4th parameter 
	
	// this will be the recursive algorithm discussed in the lecture. the following are some guidlines for you.
	// 1. check if the size of the matrix is below the threshold use a threshold of 85 and calcualte that in brute force.
	if (size <= 512){
        cache_efficient_mult(strassen_a, strassen_b, strassen_c, size);
        return;
    }
    else{
        // 2. otherwise, you need to make the 8 quadrants matrices out of a and b, fill them out
        int new_size = size/2;
        vector<vector<int>> A11(new_size, vector<int>(new_size));
        vector<vector<int>> A12(new_size, vector<int>(new_size));
        vector<vector<int>> A21(new_size, vector<int>(new_size));
        vector<vector<int>> A22(new_size, vector<int>(new_size));
        vector<vector<int>> B11(new_size, vector<int>(new_size));
        vector<vector<int>> B12(new_size, vector<int>(new_size));
        vector<vector<int>> B21(new_size, vector<int>(new_size));
        vector<vector<int>> B22(new_size, vector<int>(new_size));

        for (int i = 0; i < new_size; i++){
            for (int j = 0; j < new_size; j++){
                A11[i][j] = strassen_a[i][j];
                A12[i][j] = strassen_a[i][j+new_size];
                A21[i][j] = strassen_a[i + new_size][j];
                A22[i][j] = strassen_a[i + new_size][j + new_size];

                B11[i][j] = strassen_b[i][j];
                B12[i][j] = strassen_b[i][j+new_size];
                B21[i][j] = strassen_b[i + new_size][j];
                B22[i][j] = strassen_b[i + new_size][j + new_size];
            }
        }
	    // 3. you also need the various tempmatricess to hold the 7 terms M1 .. M7 from whcih you will construct matrix c quadrants
        vector<vector<int>> M1(new_size, vector<int>(new_size));
        vector<vector<int>> M2(new_size, vector<int>(new_size));
        vector<vector<int>> M3(new_size, vector<int>(new_size));
        vector<vector<int>> M4(new_size, vector<int>(new_size));
        vector<vector<int>> M5(new_size, vector<int>(new_size));
        vector<vector<int>> M6(new_size, vector<int>(new_size));
        vector<vector<int>> M7(new_size, vector<int>(new_size));

	    // 4. In total you will need 7 multiplications and 18 additions, use the helper functions.

        vector<vector<int>> temp1(new_size, vector<int>(new_size));
        vector<vector<int>> temp2(new_size, vector<int>(new_size));
        //m1
        strassen_add(A11, A22, temp1, new_size);
        strassen_add(B11, B22, temp2, new_size);
        strassen(temp1, temp2, M1, new_size);
        //m2
        strassen_add(A21, A22, temp1, new_size);
        strassen(temp1, B11, M2, new_size);
        //m3
        strassen_sub(B12, B22, temp1, new_size);
        strassen(temp1, A11, M3, new_size);
        //m4
        strassen_add(B21, B11, temp1, new_size);
        strassen(temp1, A22, M4, new_size);
        //m5
        strassen_add(A11, A22, temp1, new_size);
        strassen(temp1, B22, M5, new_size);
        //m6
        strassen_sub(A22, A11, temp1, new_size);
        strassen_add(B11, B21, temp2, new_size);
        strassen(temp1, temp2, M6, new_size);
        //m7
        strassen_sub(A12, A22, temp1, new_size);
        strassen_add(B21, B22, temp2, new_size);
        strassen(temp1, temp2, M7, new_size);
        
        
	    // // 5. finally put the 4 quadrant in strassen_c
        vector<vector<int>> c11(new_size, vector<int>(new_size));
        // vector<vector<int>> c12(new_size, vector<int>(new_size));
        // vector<vector<int>> c21(new_size, vector<int>(new_size));
        vector<vector<int>> c22(new_size, vector<int>(new_size));
        // //c11
        strassen_add(M1, M4, temp1, new_size);
        strassen_add(M5, M7, temp2, new_size);
        strassen_sub(temp1, temp2, c11, new_size);
        // //c12
        // strassen_add(M3, M5, c12, new_size);
        // //c21
        // strassen_add(M2, M4, c21, new_size);
        // //c22
        strassen_sub(M1, M2, temp1, new_size);
        strassen_add(M3, M6, temp2, new_size);
        strassen_add(temp1, temp2, c22, new_size);

        //add all together into c
        for (int i = 0; i < new_size; i++){
            for (int j = 0; j < new_size; j++){
                strassen_c[i][j] = c11[i][j];
                strassen_c[i][j + new_size] = M3[i][j] + M5[i][j];
                strassen_c[i + new_size][j] = M2[i][j] + M4[i][j];
                strassen_c[i + new_size][j + new_size] = c22[i][j];
            }
        }
    }
	

}
