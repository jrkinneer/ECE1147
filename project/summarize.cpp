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

    //get raw dataset
    ifstream inFile;
    inFile.open("./project_data/Motor_Vehicle_Collisions_-_Crashes_20231127.csv");
    if (inFile.is_open()) {
        std::cout << "inFile has been opened" << endl;
    }
    else {
        std::cout << "NO FILE HAS BEEN OPENED" << endl;
        return -1;
    }


    //loop through all lines of original data
    string line;
    int dead = 0;
    int injured = 0;
    bool first_line = true;
    while (getline(inFile, line)){

        //prevent internal commas of the location column from messing up the parsing of data
        vector<string> cells = parseCSV(line);
        
        if (cells.size() < 26){
            continue; //avoid segmentation fault
        }
        else{
            if (!first_line){
                //get year
                string date = cells[0];
                date = date.substr(date.find("/")+1);
                int year = stoi(date.substr(date.find("/")+1));

                if (year==2023){
                    if (!cells[10].empty() && stoi(cells[10])>0){
                        injured += stoi(cells[10]);
                    }
                    if (!cells[11].empty() && stoi(cells[11])>0){
                        dead += stoi(cells[11]);
                    }
                }
            }
        }
        first_line = false;
        
    }
    std::cout << "injured = " << injured << " dead = " << dead << endl;
    inFile.close();
    return 0;
} 