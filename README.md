# O-meter: C/C++ Time Complexity Analyzer

A sophisticated tool that automatically analyzes C/C++ code snippets and determines their time complexity using advanced pattern recognition algorithms. Available both as a **command-line interface** and an **interactive web application**.

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## 🚀 Features

- **🎨 Interactive Web Interface**: Beautiful Streamlit-powered GUI with cyberpunk theme
- **⚡ Real-time Analysis**: Instant complexity detection as you type
- **📊 Visual Analytics**: Performance charts and complexity comparisons  
- **🔍 Detailed Breakdown**: Step-by-step analysis explanation
- **💻 Command Line Support**: Traditional terminal-based analysis
- **🎯 Multiple Complexity Types**: Supports O(1) through O(N!) complexities
- **🧠 Smart Pattern Recognition**: Advanced regex-based code analysis
- **📈 Performance Visualization**: Interactive charts and metrics

## 📋 Supported Complexity Classes

| Complexity | Description | Example Pattern | Performance |
|------------|-------------|-----------------|-------------|
| **O(1)** | Constant time | Simple assignments | 🟢 Excellent |
| **O(log N)** | Logarithmic time | Binary search, divide-and-conquer | 🔵 Very Good |
| **O(N)** | Linear time | Single loop, simple recursion | 🟦 Good |
| **O(N log N)** | Linear-logarithmic | Merge sort, heap sort | 🟣 Acceptable |
| **O(N²)** | Quadratic time | Nested loops, bubble sort | 🟠 Fair |
| **O(N² log N)** | Quadratic-logarithmic | Nested loops with logarithmic ops | 🟡 Poor |
| **O(N³)** | Cubic time | Triple nested loops | 🔴 Bad |
| **O(N⁴)** | Quartic time | Four nested loops | ⚫ Very Bad |
| **O(2^N)** | Exponential time | Fibonacci recursion | ⚫ Terrible |
| **O(N!)** | Factorial time | Permutation algorithms | ⚫ Impractical |

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.6+** (Python 3.8+ recommended)
- **pip** package manager

### Quick Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sabit166/O-meter.git
   cd O-meter
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **You're ready to go!** Choose your preferred interface below.

## 🎨 Usage Options

### Option 1: Interactive Web App (Recommended)

Launch the beautiful Streamlit web interface:

```bash
streamlit run app.py
```

**Features of Web Interface:**
- 🎯 **Real-time Analysis**: See results as you type
- 📊 **Visual Charts**: Performance comparison graphs
- 🎨 **Cyberpunk Theme**: Beautiful, modern UI
- 📱 **Responsive Design**: Works on all devices
- 🔍 **Detailed Breakdown**: Step-by-step analysis
- 📈 **Code Metrics**: Lines, functions, loops count

**Web Interface Preview:**
```
⚡ O-meter: Time Complexity Analyzer ⚡
🚀 Analyze your C/C++ code complexity in real-time!

[Code Input Box]               [Results Panel]
                              📊 Analysis Result
for(int i=0; i<n; i++) {        ━━━━━━━━━━━━━━━
    for(int j=0; j<n; j++) {      O(N²)
        // code                 ━━━━━━━━━━━━━━━
    }                          Quadratic time - Can be slow
}                              for large inputs
```

### Option 2: Command Line Interface

For traditional terminal usage:

```bash
python script.py
```

**Command Line Experience:**
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

## 🎯 Advanced Features

### 🔍 Detailed Analysis
The web interface provides comprehensive analysis including:
- **Pattern Detection**: Identifies specific algorithmic patterns
- **Recursion Analysis**: Detailed recursive call breakdown  
- **Loop Counting**: Tracks nested loop depths
- **Code Metrics**: Function and loop statistics
- **Performance Visualization**: Interactive complexity charts

### 📊 Visual Analytics
- **Complexity Comparison Charts**: See how different complexities scale
- **Real-time Code Metrics**: Live statistics as you type
- **Color-coded Results**: Easy-to-understand visual feedback
- **Interactive Graphs**: Hover and explore performance data

### 🎨 User Interface Features
- **Syntax Highlighting**: Code input with proper formatting
- **Dark/Cyberpunk Theme**: Easy on the eyes
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Example Library**: Pre-loaded code examples
- **Export Results**: Save analysis for later reference

## 🌐 Web App Screenshots

### Main Interface
```
┌─────────────────────────────────────────────────────────────┐
│  ⚡ O-meter: Time Complexity Analyzer ⚡                    │
│  🚀 Analyze your C/C++ code complexity in real-time!       │
├─────────────────────┬───────────────────────────────────────┤
│ 💻 Code Input      │ 📊 Analysis Results                   │
│                     │                                       │
│ [Text Area]         │   O(N²)                              │
│                     │   Quadratic time                      │
│ for(int i=0;i<n;i++){│   Can be slow for large inputs      │
│   for(int j=0;j<n;j++│                                      │
│     // code         │ 📈 Complexity Breakdown:             │
│   }                 │ ● O(1) - Detected                    │
│ }                   │ ● O(N²) - Main complexity            │
│                     │                                       │
│ [🔍 Analyze Button] │ 📈 Performance Chart                 │
└─────────────────────┴───────────────────────────────────────┘
```

## � Code Examples & Patterns

<details>
<summary><strong>🟢 O(1) - Constant Time</strong></summary>

```c
int sum = a + b;
int result = array[0];
return x * 2 + 5;
```
</details>

<details>
<summary><strong>🔵 O(log N) - Logarithmic Time</strong></summary>

```c
// Binary search pattern
for(int i=1; i<n; i*=2) {
    // code
}

// While loop variant
while(i < n) {
    i *= 2;
}

// Division pattern
while(i > 0) {
    i /= 2;
}
```
</details>

<details>
<summary><strong>🟦 O(N) - Linear Time</strong></summary>

```c
// Simple loop
for(int i=0; i<n; i++) {
    // code
}

// Linear recursion
int factorial(int n) {
    if(n <= 1) return 1;
    return n * factorial(n-1);
}
```
</details>

<details>
<summary><strong>🟠 O(N²) - Quadratic Time</strong></summary>

```c
// Nested loops
for(int i=0; i<n; i++) {
    for(int j=0; j<n; j++) {
        // code
    }
}

// Bubble sort example
for(int i=0; i<n-1; i++) {
    for(int j=0; j<n-i-1; j++) {
        if(arr[j] > arr[j+1]) {
            swap(arr[j], arr[j+1]);
        }
    }
}
```
</details>

<details>
<summary><strong>⚫ O(2^N) - Exponential Time</strong></summary>

```c
// Fibonacci recursion
int fibonacci(int n) {
    if(n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

// Subset generation
void generateSubsets(int arr[], int n, int index) {
    if(index == n) return;
    generateSubsets(arr, n, index+1);  // Include
    generateSubsets(arr, n, index+1);  // Exclude
}
```
</details>

<details>
<summary><strong>⚫ O(N!) - Factorial Time</strong></summary>

```c
// Permutation generation
void permute(int arr[], int n) {
    for(int i=0; i<n; i++) {
        permute(arr, n-1);  // Recursion inside loop
    }
}
```
</details>

## 🚀 Quick Start Guide

### 1. **Launch Web Interface**
```bash
streamlit run app.py
```
→ Opens `http://localhost:8501` in your browser

### 2. **Enter Code**
- Paste your C/C++ code in the text area
- Or use the provided examples

### 3. **Analyze**  
- Click "🔍 Analyze Complexity"
- Get instant results with visual feedback

### 4. **Explore Results**
- View complexity breakdown
- Check performance charts
- See code metrics and analysis details

## 🔬 Technical Details

### Algorithm Architecture
The analyzer uses **three specialized analysis engines**:

#### 1. **Loop Analysis Engine** (`analyze_exponential`)
- 🔍 **Nested Loop Detection**: Tracks loop depth for polynomial complexity
- 📊 **Pattern Recognition**: Identifies `for` and `while` loop structures  
- 🧮 **Logarithmic Detection**: Recognizes `*=`, `/=` operations in loops
- 🎯 **Smart Counting**: Accurate brace matching and scope tracking

#### 2. **Logarithmic Pattern Engine** (`analyze_logarithmic`)  
- ⚡ **Specialized O(log N) Detection**: Dedicated logarithmic pattern analysis
- 🔄 **Multi-Pattern Support**: Handles `i*=2`, `i/=2`, binary operations
- 🏷️ **Variable Agnostic**: Works with any variable names
- 🎮 **Loop Type Flexible**: Supports both `for` and `while` constructs

#### 3. **Recursion Analysis Engine** (`analyze_recursion`)
- 🔄 **Recursive Call Detection**: Identifies functions calling themselves  
- 🧠 **Pattern Classification**: Distinguishes single vs. multiple recursion
- 🚫 **Keyword Filtering**: Excludes C/C++ reserved words
- 🎯 **Context Awareness**: Detects recursion within loops for factorial complexity

### Pattern Recognition Technology
- **Advanced Regex**: Sophisticated regular expressions for code parsing
- **AST-like Analysis**: Structure-aware code interpretation  
- **Multi-pass Analysis**: Multiple analysis engines for comprehensive coverage
- **Smart Merging**: Intelligent combination of results from different engines

### Performance & Accuracy
- ⚡ **Fast Analysis**: Processes code snippets in milliseconds
- 🎯 **High Accuracy**: Tested across thousands of code patterns
- 💾 **Memory Efficient**: Minimal memory footprint
- 🔄 **Real-time Processing**: Instant feedback in web interface

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
