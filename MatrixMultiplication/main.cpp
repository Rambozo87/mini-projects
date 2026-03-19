#include <random>
#include <print>

using namespace std;

int main() {
    srand(time(NULL));

    int r = 1 + (rand() % 10);
    int c = 1 + (rand() % 10);

    int matrixOne[r][c];
    int matrixTwo[c][r];
    int finalMatrix[r][r];

    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            matrixOne[i][j] = 1 + (rand() % 10);
        }
    }

    for (int i = 0; i < c; i++) {
        for (int j = 0; j < r; j++) {
            matrixTwo[i][j] = 1 + (rand() % 10);
        }
    }

    for (int i = 0; i < r; i++) {
        for (int j = 0; j < r; j++) {
            finalMatrix[j][i] = 0;
        }
    }

    for(int i = 0; i < r; i++) {
        // for each row in matrixOne multiply and add together each column of one to each row for the current column.
        for (int k = 0; k < r; k++) {
            for(int j = 0; j < c; j++) {
                finalMatrix[i][k] += matrixOne[i][j] * matrixTwo[j][k];
            }
        }
    }

    print("[");
    for(int i = 0; i < r; i++) {
        for(int j = 0; j < r; j++) {
            print("{} ", finalMatrix[i][j]);
        }
        println();
    }
    print("]");

    return 0;
}
