#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <stdio.h>
#include <sstream>
#include <set>

using namespace std;

//parses one line of the csv to prevent internal commas from altering the amount of percieved cells
vector<string> parseCSV(const string& line) {
    vector<string> result;
    stringstream ss(line);
    string cell;
    char ch;
    bool insideParentheses = false;

    while (ss.get(ch)) {
        if (ch == '"') {
            insideParentheses = !insideParentheses;
        } else if (ch == ',' && !insideParentheses) {
            result.push_back(cell);
            cell.clear();
        } else {
            cell += ch;
        }
    }

    result.push_back(cell);  // Add the last cell

    return result;
}

int main()
{   
    //creates sets of the 40 most common values for vehicle one type and vehicle two type
    //this was done by first running this preprocess script and passing that data to python
    //where I then used a panda library function to find the 40 most common values of each column
    //I now rerun this script and check each line to see if both vehicle 1 type and vehicle 2 type
    //are one of the modes, if they are they get written to the data.csv file
    //if not they get skipped
    //this allows for more efficient one hot encoding for these values by eliminating spelling errors
    //and miscellaneous errors from the dataset

    //original one hot encoding size
    //2,044,896 x 3490
    //rows x features

    //optimized one hot encoding size
    //1,609,485, 206
    //rows x features

    //6.80511219×10^9 fewer elements

    ifstream vehicle1_types;
    vehicle1_types.open("vehicle1.txt");
    set<string> v1;
    string s;
    while(getline(vehicle1_types, s)){
        v1.insert(s);
    }
    vehicle1_types.close();
    cout << "set 1 finished" << endl;

    ifstream vehicle2_types;
    vehicle2_types.open("vehicle2.txt");
    set<string> v2;
    while(getline(vehicle2_types, s)){
        v2.insert(s);
    }
    vehicle1_types.close();
    cout << "set 2 finished" << endl;


    //get raw dataset
    ifstream inFile;
    inFile.open("./project_data/Motor_Vehicle_Collisions_-_Crashes_20231127.csv");
    if (inFile.is_open()) {
        cout << "inFile has been opened" << endl;
    }
    else {
        cout << "NO FILE HAS BEEN OPENED" << endl;
        return -1;
    }

    //open output data file
    ofstream outFile;
    outFile.open("./project_data/data_injuries.csv");
    if (outFile.is_open()) {
        cout << "outFile has been opened" << endl;
    }
    else {
        cout << "NO FILE HAS BEEN OPENED" << endl;
        return -2;
    }

    //loop through all lines of original data
    string line;
    string cell;
    int i = -1;
    bool first_line = true;
    int skipped = 0;
    while (getline(inFile, line)){
        i++;

        //prevent internal commas of the location column from messing up the parsing of data
        vector<string> cells = parseCSV(line);
        
        //check for valid vehicle1 and vehicle2 type
        //if either are invalid, we skip this row
        try{
            if (cells.size() < 26){
                continue; //avoid segmentation fault
            }
            if (((v1.find(cells[24]) == v1.end() || v2.find(cells[25]) == v2.end()) && !first_line)){
                skipped += 1;
                continue;
            }
        }
        catch(const std::exception& e){
            cout << "error " << e.what() << endl;
            cout << i << endl;
            continue;
        }
        

        //for each cell in the row
        for (int j = 0; j < cells.size(); j++){
            cell = cells[j];
            
            //get columns of interest
            //j=10 is injuries
            if (j == 1 || j == 3 || j==4 || j==5 || j == 10 || j==18 || j==19 || j==24 || j==25){
                //handle blank/empty cell
                if (cell.empty()){
                    if (j==18 || j==19 || j==24 || j==25){
                        outFile << "null";
                    }
                    else{
                        outFile << 0;
                    }
                }
                else{
                    if (j==1 and !first_line){//convert time to decimal
                        string hour = cell.substr(0, cell.find(":"));
                        double hour_ = stod(hour);
                        string minutes = cell.substr(cell.find(":") + 1);
                        hour_ += stod(minutes)/60;
                        outFile << hour_;
                    }
                    else if(j==3 and !first_line){ //handle zip code as multiple data types
                        try{
                            outFile << stoi(cell);
                        }
                        catch(const std::invalid_argument& e){
                            cout << "Invalid argument " << e.what() << endl;
                            cout << "cell = " << cell << endl;
                            outFile << 0;
                        }
                    }
                    else{
                        outFile << cell;
                    }
                }

                //write a new line and calculate value of new column
                if (j==25){
                    int sum_cars = 0;
                    if (first_line){
                        outFile << ",number of vehicles involved";
                    }
                    else{
                        for (int k = 24; k < cells.size(); k++){
                            if (!cells[k].empty()){
                                sum_cars+=1;
                            }
                        }
                        outFile << "," << sum_cars;
                    }
                    outFile << "\n";
                }
                else{
                    outFile << ",";
                }
            }
        }
        first_line = false;
    }
    cout << "skipped = " << skipped << endl;
    inFile.close();
    outFile.close();
    system("pause");
    return 0;
} 