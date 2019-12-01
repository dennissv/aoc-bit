#include <fstream>
#include <iostream>

using namespace std;

int fuel_tot(const int& fuel) {
    int curr_fuel = (fuel/3)-2;
    if (curr_fuel > 0) {
        return curr_fuel + fuel_tot(curr_fuel);
    }
    return 0;
}

int main() {
    ifstream infile("data/input.txt");
    int fuel;
    int fuel_sum1 = 0;
    int fuel_sum2 = 0;
    while (infile >> fuel) {
        fuel_sum1 += (fuel/3)-2;
        fuel_sum2 += fuel_tot(fuel);
    }

    cout << "D1P1: " << fuel_sum1 << endl;
    cout << "D1P2: " << fuel_sum2 << endl;
    return 0;
}
