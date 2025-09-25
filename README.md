# O-meter: C/C++ Time Complexity Analyzer

A sophisticated command-line tool that automatically analyzes C/C++ code snippets and determines their time complexity using advanced pattern recognition algorithms.

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## 🚀 Features

- **Automatic Time Complexity Detection**: Analyzes C/C++ code and determines Big O notation
- **Multiple Complexity Types**: Supports detection of O(1), O(log N), O(N), O(N log N), O(N²), O(N² log N), O(N³), O(N⁴), O(2^N), and O(N!)
- **Loop Analysis**: Detects nested loops, logarithmic patterns, and linear iterations
- **Recursion Detection**: Identifies recursive functions and classifies their complexity patterns
- **Smart Pattern Recognition**: Uses regex-based analysis to understand code structure
- **Real-time Analysis**: Provides instant feedback on code complexity

## 📋 Supported Complexity Classes

| Complexity | Description | Example Pattern |
|------------|-------------|-----------------|
| **O(1)** | Constant time | Simple assignments, arithmetic operations |
| **O(log N)** | Logarithmic time | Binary search, divide-and-conquer |
| **O(N)** | Linear time | Single loop, simple recursion |
| **O(N log N)** | Linear-logarithmic | Merge sort, efficient sorting algorithms |
| **O(N²)** | Quadratic time | Nested loops, bubble sort |
| **O(N² log N)** | Quadratic-logarithmic | Nested loops with logarithmic operations |
| **O(N³)** | Cubic time | Triple nested loops |
| **O(N⁴)** | Quartic time | Four nested loops |
| **O(2^N)** | Exponential time | Fibonacci recursion, subset generation |
| **O(N!)** | Factorial time | Permutation algorithms |

## 🛠️ Installation

### Prerequisites
- Python 3.6 or higher
- No additional dependencies required (uses only standard library)

### Setup
1. Clone or download the repository:
   ```bash
   git clone https://github.com/Sabit166/O-meter.git
   cd O-meter
   ```

2. Make the script executable (optional):
   ```bash
   chmod +x script.py
   ```

## 💻 Usage

### Basic Usage
Run the script and paste your C/C++ code:

```bash
python script.py
```

The program will prompt you to enter your code. After entering your code snippet:
- **Windows**: Press `Ctrl+Z` then `Enter`
- **Unix/Linux/macOS**: Press `Ctrl+D`

### Example Session

```bash
$ python script.py
Enter your C/CPP code below. Press Ctrl+D (Unix/macOS) or Ctrl+Z then Enter (Windows) to finish:

for(int i=0; i<n; i++) {
    for(int j=0; j<n; j++) {
        // some operation
    }
}
^Z

Worst-case complexity: O(N^2)
```

## 📝 Code Examples

### O(1) - Constant Time
```c
int sum = a + b;
int result = array[0];
```

### O(log N) - Logarithmic Time
```c
// Binary search pattern
for(int i=1; i<n; i*=2) {
    // code
}

// Or with while loop
while(i < n) {
    i *= 2;
}
```

### O(N) - Linear Time
```c
for(int i=0; i<n; i++) {
    // code
}

// Simple recursion
int factorial(int n) {
    if(n <= 1) return 1;
    return n * factorial(n-1);
}
```

### O(N²) - Quadratic Time
```c
for(int i=0; i<n; i++) {
    for(int j=0; j<n; j++) {
        // code
    }
}
```

### O(2^N) - Exponential Time
```c
int fibonacci(int n) {
    if(n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}
```

### O(N!) - Factorial Time
```c
void permute(int arr[], int n) {
    for(int i=0; i<n; i++) {
        permute(arr, n-1);  // Recursion inside loop
    }
}
```

## 🔍 How It Works

The analyzer uses three main analysis functions:

### 1. Loop Analysis (`analyze_exponential`)
- Detects nested loop structures
- Counts loop depth for polynomial complexity
- Identifies logarithmic patterns in loops
- Handles both `for` and `while` loops

### 2. Logarithmic Pattern Detection (`analyze_logarithmic`)
- Specifically designed for O(log N) detection
- Recognizes multiplication/division patterns: `i*=2`, `i/=2`
- Works with any variable names
- Supports both loop types

### 3. Recursion Analysis (`analyze_recursion`)
- Identifies recursive function calls
- Distinguishes between single and multiple recursion
- Detects recursion within loops (factorial complexity)
- Filters out C/C++ keywords to avoid false positives

## 🎯 Algorithm Details

### Pattern Recognition
The tool uses sophisticated regex patterns to identify:
- **Loop structures**: `for` and `while` loops with various increment patterns
- **Recursive calls**: Function calls within the same function body
- **Logarithmic operations**: Multiplication and division assignments
- **Nesting levels**: Proper brace counting for accurate depth analysis

### Complexity Determination
1. **Analyze all patterns** in the code simultaneously
2. **Combine results** from different analysis functions
3. **Return the highest complexity** found (worst-case scenario)
4. **Handle edge cases** like empty code or malformed input

## ⚡ Performance

- **Fast Analysis**: Processes code snippets in milliseconds
- **Memory Efficient**: Uses minimal memory for pattern matching
- **Scalable**: Handles code snippets of varying sizes effectively

## 🚫 Limitations

- **Code Snippets Only**: Designed for small to medium code segments
- **C/C++ Focus**: Optimized for C/C++ syntax patterns
- **Static Analysis**: Does not execute code, only analyzes structure
- **Approximation**: Provides Big O estimation based on common patterns

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Sabit166**
- GitHub: [@Sabit166](https://github.com/Sabit166)
- Repository: [O-meter](https://github.com/Sabit166/O-meter)

## 🙏 Acknowledgments

- Inspired by the need for quick algorithm complexity analysis
- Built with Python's powerful regex capabilities
- Designed for educational and professional development purposes

## 📞 Support

If you have any questions or run into issues, please:
1. Check the existing [Issues](https://github.com/Sabit166/O-meter/issues)
2. Create a new issue with detailed information
3. Include code examples and expected vs actual behavior

---

**Happy Coding!** 🎉
