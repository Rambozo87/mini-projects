#include <complex>
#include <cstdint>
#include <cstdio>

#define WINDOW_WIDTH 640
#define WINDOW_HEIGHT 480

const double xmin = -2.0;
const double xmax = 1.0;
const double ymin = -1.5;
const double ymax = 1.5;

const int max_iter = 1000;

uint8_t buffer[WINDOW_HEIGHT][WINDOW_WIDTH][3] = {};

void generateMandelBrot();
int mandelbrot_iter(int x, int y);
std::complex<double> pixelToComplex(int px, int py);
void iterToColor(int iter, uint8_t &r, uint8_t &g, uint8_t &b);

int main() {
    generateMandelBrot();

    FILE *f = fopen("mandelbrot.ppm", "wb");
    fprintf(f, "P6\n%d %d\n255\n", WINDOW_WIDTH, WINDOW_HEIGHT);
    fwrite(buffer, 1, sizeof(buffer), f);
    fclose(f);

    return 0;
}

void generateMandelBrot() {
    for (int x = 0; x < WINDOW_WIDTH; x++) {
        for (int y = 0; y < WINDOW_HEIGHT; y++) {
            int iter = mandelbrot_iter(x, y);
            iterToColor(iter, buffer[y][x][0], buffer[y][x][1], buffer[y][x][2]);
        }
    }
}

int mandelbrot_iter(int x, int y) {
    std::complex<double> c = pixelToComplex(x, y);
    std::complex<double> z = 0;

    for (int itr = 0; itr < max_iter; itr++) {
        z = z * z + c;
        if (std::abs(z) > 2)
            return itr;
    }

    return -1;
}

void iterToColor(int iter, uint8_t &r, uint8_t &g, uint8_t &b) {
    if (iter == -1) {
        r = g = b = 0;
        return;
    }
    double t = (double)iter / max_iter;
    r = (uint8_t)(9   * (1 - t) * t * t * t * 255);
    g = (uint8_t)(15  * (1 - t) * (1 - t) * t * t * 255);
    b = (uint8_t)(8.5 * (1 - t) * (1 - t) * (1 - t) * t * 255);
}

std::complex<double> pixelToComplex(int px, int py) {
    double x = xmin + px * (xmax - xmin) / WINDOW_WIDTH;
    double y = ymax - py * (ymax - ymin) / WINDOW_HEIGHT;
    return std::complex<double>(x, y);
}
