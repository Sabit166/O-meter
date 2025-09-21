#include <stdio.h>

int fib(int n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);
}




int main() {
    // Test O(N) - single loop
    for (int i = 0; i < 10; i++) {
        printf("Hello\n");
    }
    
    // Test O(N^2) - nested loops
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 10; j++) {
            printf("World\n");
        }
    }
    
    // Call recursive fibonacci
    int result = fib(5);
    printf("Fibonacci result: %d\n", result);
    
    return 0;
}
