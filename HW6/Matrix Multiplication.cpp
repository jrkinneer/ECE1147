#include "helper.h"
#include <iostream>

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


void test(vector<double> &times,int MATRIX_SIZE){
    // multpliy two matrices of size MATRIX_SIZE and store the time taken for the operation in the times vector
    
    // Initialize the random number generator
    srand(time(NULL));

    //Declare three matrices
    vector<vector<int>> matrix_a(MATRIX_SIZE, vector<int>(MATRIX_SIZE));
    vector<vector<int>> matrix_b(MATRIX_SIZE, vector<int>(MATRIX_SIZE));
    vector<vector<int>> matrix_c(MATRIX_SIZE, vector<int>(MATRIX_SIZE));
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
    
    //create new matrices C and R with the new samples cols and rows, and a new matrix CR to hold the approx product
    // don't forgoet to normalize as we did in the lecture.

    //multiply C and R using Brute Force.

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
	
	// 2. otherwise, you need to make the 8 quadrants matrices out of a and b, fill them out
	// 3. you also need the various tempmatricess to hold the 7 terms M1 .. M7 from whcih you will construct matrix c quadrants
	// 4. In total you will need 7 multiplications and 18 additions, use the helper functions.
	// 5. finally put the 4 quadrant in strassen_c

}
