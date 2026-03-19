#include "matplotlibcpp.h"

namespace plt = matplotlibcpp;

double learningRate = 0.2;
double tolerance = 3E-4;
int startingPoint = -2.5;
double h = 1E-10;

// slope = (f(x + h) - f(x)) / h

// new x = x - learningRate * gradient

// plot that graph fnx

// plot each point until tolerence is met.

double fnx(double x) {
    return x * x;
}

double gradient(double x) {
    return 2 * x;
}

int main() {
    std::vector<double> x, y;
    for (double i = -5; i <= 5; i += 0.01) {
        x.push_back(i);
        y.push_back(fnx(i));
    }

    plt::plot(x, y, "b");

    double slope = (fnx(startingPoint + h) - fnx(startingPoint)) / h;
    double new_x = startingPoint;

    while(std::abs(slope) > tolerance) {
        new_x = new_x - learningRate * gradient(new_x);

        slope = (fnx(new_x + h) - fnx(new_x)) / h;

        std::println(std::cout, "{}", new_x);

        plt::plot(std::vector<double>{new_x}, std::vector<double>{fnx(new_x)}, "ro");
    }

    plt::show();
    return 0;
}
