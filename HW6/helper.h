#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <iomanip>
#include <fstream>
#include <math.h>
#include <ctime>
#include <random>
#include <map>
#include <vector> 
using std::vector;
//similar to large_mutliply but runs over a set of matrix sizes
//compile with g++ --std=c++11 -I ./eigen-3.4.0 test.cpp -o test


//helper functions
void multiply_vec(vector<vector<int>> &A, vector<vector<int>> &B, vector<vector<int>> &C, int size)
{
	//multiply two square matrices in brute force
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            for (int k = 0; k < size; k++)
            {
                C[i][j] += A[i][k]*B[k][j];
            }
        }
    }
}

float euclidean_norm_rows(vector<vector<int>> &matrix, int row)
{
	//get the euclidean norm of a matrix row
    float sum = 0;
    for (int i = 0; i < matrix.size(); i++)
    {
        sum += pow(matrix[i][row], 2);
    }
    return sqrt(sum);
}

float euclidean_norm_cols(vector<vector<int>> &matrix, int col)
{
	//get the euclidean norm of a matrix col
    float sum = 0;
    for (int i = 0; i < matrix.size(); i++)
    {
        sum += pow(matrix[col][i], 2);
    }
    return sqrt(sum);
}
void matrix_diff(vector<vector<float>> &matrix_a, vector<vector<float>> &matrix_b, vector<vector<float>> &output)
{
	//subtracte two matrices
    for (int i = 0; i < matrix_a.size(); i++)
    {
        for (int j = 0; j < matrix_a.size(); j++)
        {
            output[i][j] = matrix_a[i][j] - matrix_b[i][j];
        }
    }
}

float frobenius_norm(vector<vector<float>> &matrix)
{
	//get the forbenius norm of a matrix
    float sum = 0;
    for (int i = 0; i < matrix.size(); i++)
    {
        for (int j = 0; j < matrix.size(); j++)
        {
            sum += pow(matrix[i][j], 2);
        }
    }
    return sqrt(sum);
}

void strassen_add(vector<vector<int>> &matrix_a, vector<vector<int>> &matrix_b, vector<vector<int>> &output, int size)
{
	//add two matrices with a given size
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            output[i][j] = matrix_a[i][j] + matrix_b[i][j];
        }
    }
}

void strassen_sub(vector<vector<int>> &matrix_a, vector<vector<int>> &matrix_b, vector<vector<int>> &output,int size)
{
	//add two matrices with a given size
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            output[i][j] = matrix_a[i][j] - matrix_b[i][j];
        }
    }
}

//function to find the next higher power of two
int next_power_of_two(int size){
    int i = 1;
    while(i < size){
        i *= 2;
    }
    return i;
}

//check if a number is power of two ro not
bool is_power_of_two(int size){
    return size > 0 && !(size & (size - 1));
}
