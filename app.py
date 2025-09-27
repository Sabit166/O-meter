import streamlit as st
import re
import io
import sys
from contextlib import redirect_stdout


def analyze_exponential(code: str) -> str:
    
    # Updated patterns to better detect logarithmic loops
    FOR_LOOP_O_N = r'for\s*\([^)]*(\+\+|--|[\+-]=)[^)]*\)'
    FOR_LOOP_O_LOGN = r'for\s*\([^)]*(\*=|/=)[^)]*\)'
    
    WHILE_LOOP_O_N = r'while\s*\(\s*(\w+)(?:\s*[<>=!]+.*?)?\s*\)'
    WHILE_LOOP_O_LOGN = r'(\w+)\s*(\*|/)=\s*\d+'
    
    max_depth = 0
    current_depth = 0
    log_n_detected = False
    inside_while = False
    while_variable = None
    inside_for_loop = False

    for line in code.splitlines():
        line = line.strip()  # Remove leading/trailing whitespace
        
        # Check for for loops
        for_n_match = re.search(FOR_LOOP_O_N, line)
        for_log_match = re.search(FOR_LOOP_O_LOGN, line)
        
        if for_n_match or for_log_match:
            current_depth += 1
            max_depth = max(max_depth, current_depth)
            inside_for_loop = True
            
            # Check if this loop is logarithmic
            if for_log_match:
                log_n_detected = True
        
        # Detect while loop start
        elif re.search(WHILE_LOOP_O_N, line):
            while_match = re.search(WHILE_LOOP_O_N, line)
            if while_match:
                while_variable = while_match.group(1)
                inside_while = True
                current_depth += 1
                max_depth = max(max_depth, current_depth)
        
        # Check for logarithmic operations inside while loop or for loop
        if inside_while and while_variable:
            log_match = re.search(WHILE_LOOP_O_LOGN, line)
            if log_match and log_match.group(1) == while_variable:
                log_n_detected = True
        
        # Also check for logarithmic operations inside for loop body
        if inside_for_loop:
            log_match = re.search(WHILE_LOOP_O_LOGN, line)
            if log_match:
                log_n_detected = True

        # Detect block ending - only on closing braces
        if "}" in line:
            if current_depth > 0:
                current_depth -= 1
                if inside_while and current_depth == 0:
                    inside_while = False
                    while_variable = None
                if inside_for_loop and current_depth == 0:
                    inside_for_loop = False

    # Decide complexity from max depth
    if max_depth == 0:
        return "O(1)"
    else:
        time_complexity = ""
        if max_depth == 1:
            if log_n_detected:
                time_complexity = "log N"  # Single logarithmic loop
            else:
                time_complexity = "N"     # Single linear loop
        else:
            # If logarithmic detected, reduce the power by 1
            if log_n_detected:
                if max_depth == 2:
                    time_complexity = "NLogN"  # N^2 becomes N*LogN when one loop is logarithmic
                else:
                    time_complexity = f"N^{max_depth-1}LogN"  # Reduce power by 1 and add LogN
            else:
                time_complexity = f"N^{max_depth}"

        return f"O({time_complexity})"
    

def analyze_logarithmic(code: str) -> str:
    """
    Simplified function to detect O(log N) complexity patterns.
    Detects these patterns:
    1. for(type var=init; var<n; var*=2)
    2. while(var<n) { var*=2; }
    3. while(var) { var/=2; }
    """
    
    # Pattern 1: for loop with multiplication in increment
    for_logn_pattern = r'for\s*\([^;]*;\s*[^;]*;\s*\w+\s*\*=\s*\d+\s*\)'
    
    # Pattern 2 & 3: while loops
    while_pattern = r'while\s*\([^)]+\)'
    mult_div_pattern = r'\w+\s*(\*=|/=)\s*\d+'
    
    lines = code.splitlines()
    found_for_logn = False
    in_while_loop = False
    found_while_logn = False
    current_depth = 0
    
    for line in lines:
        line = line.strip()
        
        # Check for logarithmic for loop (Pattern 1)
        if re.search(for_logn_pattern, line):
            found_for_logn = True
            current_depth += 1
        
        # Check for while loop start (Pattern 2 & 3)
        elif re.search(while_pattern, line):
            in_while_loop = True
            current_depth += 1
        
        # Check for multiplication/division inside while loop
        if in_while_loop and re.search(mult_div_pattern, line):
            found_while_logn = True
        
        # Track closing braces
        if '}' in line and current_depth > 0:
            current_depth -= 1
            if current_depth == 0:
                in_while_loop = False
    
    # Return O(log N) if we found any logarithmic pattern and no nested loops
    if (found_for_logn or found_while_logn) and current_depth == 0:
        return "O(log N)"
    else:
        return "O(1)"


def analyze_recursion(code: str) -> str:
    # Detect recursive calls (function calling itself)
    # Exclude C/C++ keywords from being treated as function names
    c_keywords = {'for', 'while', 'if', 'else', 'switch', 'case', 'do', 'return', 'break', 'continue', 'goto'}
    
    all_matches = re.findall(r'\b(\w+)\s*\([^)]*\)\s*\n?\s*\{', code)
    functions = [func for func in all_matches if func not in c_keywords]
    detected = "O(1)"  # Default if no recursion found
    
    debug_output = []

    for func in functions:
        # Extract function body using brace counting
        func_body = extract_function_body(code, func)
        
        if func_body:
            # Remove comments to avoid false positives
            func_body_no_comments = remove_comments(func_body)
            
            # Look for recursive calls inside the function (excluding comments)
            pattern = rf'{func}\s*\([^)]*\)'
            matches = re.findall(pattern, func_body_no_comments)

            if matches:
                # Store debug info instead of printing
                debug_output.append(f"Found recursive calls in {func}: {matches}")
                debug_output.append(f"Function body (no comments): {func_body_no_comments.strip()[:200]}...")
                
                # Case 3: Recursive call inside a loop -> O(N!) (check this first)
                if re.search(r'for\s*\([^)]*\)[^}]*{[^}]*' + pattern, func_body_no_comments, re.DOTALL):
                    detected = "O(N!)"
                    debug_output.append(f"  -> Found recursive call inside loop: O(N!)")
                
                # Case 1: Single recursive call -> O(N)
                elif len(matches) == 1:
                    detected = "O(N)"
                    debug_output.append(f"  -> Single recursive call: O(N)")

                # Case 2: Multiple recursive calls -> O(2^N) (like Fibonacci)
                elif len(matches) >= 2:
                    detected = "O(2^N)"
                    debug_output.append(f"  -> Multiple recursive calls: O(2^N)")

    return detected, debug_output


def remove_comments(code: str) -> str:
    """Remove C/C++ style comments from code"""
    # Remove single-line comments //
    code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
    # Remove multi-line comments /* */
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    return code


def extract_function_body(code: str, func_name: str) -> str:
    """
    Extract the body of a function using brace counting.
    For: int factorial(int n) { ... }
    Returns: the content between the outermost braces
    """
    # Find the function declaration
    func_pattern = rf'\b{func_name}\s*\([^)]*\)\s*'
    func_match = re.search(func_pattern, code)
    
    if not func_match:
        return ""
    
    # Find the opening brace after the function declaration
    start_pos = func_match.end()
    
    # Skip whitespace and newlines to find the opening brace
    while start_pos < len(code) and code[start_pos] in ' \t\n\r':
        start_pos += 1
    
    if start_pos >= len(code) or code[start_pos] != '{':
        return ""
    
    # Count braces to find the matching closing brace
    brace_count = 0
    body_start = start_pos + 1  # Position after opening brace
    
    for i in range(start_pos, len(code)):
        if code[i] == '{':
            brace_count += 1
        elif code[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                # Found the matching closing brace
                return code[body_start:i]
    
    return ""  # No matching closing brace found


def get_complexity_color(complexity):
    """Return appropriate color for each complexity"""
    color_map = {
        "O(1)": "#28a745",      # Green
        "O(log N)": "#17a2b8",  # Cyan
        "O(N)": "#007bff",      # Blue
        "O(NLogN)": "#6f42c1",  # Purple
        "O(N^2)": "#fd7e14",    # Orange
        "O(N^2LogN)": "#e83e8c", # Pink
        "O(N^3)": "#dc3545",    # Red
        "O(N^4)": "#6c757d",    # Gray
        "O(2^N)": "#343a40",    # Dark
        "O(N!)": "#000000"      # Black
    }
    return color_map.get(complexity, "#6c757d")


def get_complexity_description(complexity):
    """Return description for each complexity"""
    descriptions = {
        "O(1)": "Constant time - Best performance",
        "O(log N)": "Logarithmic time - Very efficient",
        "O(N)": "Linear time - Good performance",
        "O(NLogN)": "Linear-logarithmic time - Acceptable",
        "O(N^2)": "Quadratic time - Can be slow for large inputs",
        "O(N^2LogN)": "Quadratic-logarithmic time - Slow for large inputs",
        "O(N^3)": "Cubic time - Slow performance",
        "O(N^4)": "Quartic time - Very slow performance",
        "O(2^N)": "Exponential time - Extremely slow",
        "O(N!)": "Factorial time - Impractically slow"
    }
    return descriptions.get(complexity, "Unknown complexity")


# Streamlit App Configuration
st.set_page_config(
    page_title="O-meter: Time Complexity Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for cyberpunk theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #00ff41, #ff0080);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .complexity-result {
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .code-input {
        border: 2px solid #00ff41;
        border-radius: 10px;
    }
    
    .sidebar-content {
        background-color: #1e1e1e;
        padding: 1rem;
        border-radius: 10px;
    }
    
    .complexity-table {
        background-color: #1e1e1e;
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Main App
def main():
    # Header
    st.markdown('<div class="main-header">⚡ O-meter: Time Complexity Analyzer ⚡</div>', unsafe_allow_html=True)
    st.markdown("### 🚀 Analyze your C/C++ code complexity in real-time!")
    
    # Sidebar with information
    with st.sidebar:
        st.markdown("### 🎯 Supported Complexities")
        complexity_info = {
            "O(1)": "🟢 Constant",
            "O(log N)": "🔵 Logarithmic", 
            "O(N)": "🟦 Linear",
            "O(N log N)": "🟣 Linear-log",
            "O(N²)": "🟠 Quadratic",
            "O(N² log N)": "🟡 Quad-log",
            "O(N³)": "🔴 Cubic",
            "O(N⁴)": "⚫ Quartic",
            "O(2^N)": "⚫ Exponential",
            "O(N!)": "⚫ Factorial"
        }
        
        for complexity, description in complexity_info.items():
            st.markdown(f"**{description}**: {complexity}")
        
        st.markdown("---")
        st.markdown("### 📝 Example Patterns")
        
        with st.expander("Loop Examples"):
            st.code("""
// O(1)
int x = 5;

// O(N)
for(int i=0; i<n; i++) {
    // code
}

// O(N²)
for(int i=0; i<n; i++) {
    for(int j=0; j<n; j++) {
        // code
    }
}
            """, language="c")
        
        with st.expander("Recursion Examples"):
            st.code("""
// O(N)
int factorial(int n) {
    if(n <= 1) return 1;
    return n * factorial(n-1);
}

// O(2^N)
int fibonacci(int n) {
    if(n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}
            """, language="c")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💻 Enter your C/C++ Code:")
        
        # Code input with example
        default_code = """for(int i=0; i<n; i++) {
    for(int j=0; j<n; j++) {
        // Your algorithm here
    }
}"""
        
        user_code = st.text_area(
            label="Code Input",
            value=default_code,
            height=300,
            help="Enter your C/C++ code snippet here",
            label_visibility="collapsed"
        )
        
        # Analyze button
        if st.button("🔍 Analyze Complexity", type="primary", use_container_width=True):
            if user_code.strip():
                # Run analysis
                with st.spinner("Analyzing your code..."):
                    highest_time_complexity = "O(1)"
                    functions = [analyze_exponential, analyze_logarithmic]
                    
                    # Modified to handle recursion analysis separately
                    recursion_result, debug_output = analyze_recursion(user_code)
                    functions_results = [func(user_code) for func in functions] + [recursion_result]
                    
                    time_complexity_serial = {
                        "O(1)": False,
                        "O(log N)": False,
                        "O(N)": False,
                        "O(NLogN)": False,
                        "O(N^2)": False,
                        "O(N^2LogN)": False,
                        "O(N^3)": False,
                        "O(N^4)": False,
                        "O(2^N)": False,
                        "O(N!)": False
                    }
                    
                    for result in functions_results:
                        if result in time_complexity_serial:
                            time_complexity_serial[result] = True
                    
                    # Find highest complexity
                    for complexity in ["O(log N)", "O(N)", "O(NLogN)", "O(N^2)", "O(N^2LogN)", "O(N^3)", "O(N^4)", "O(2^N)", "O(N!)"]:
                        if time_complexity_serial[complexity]:
                            highest_time_complexity = complexity
                
                # Display results in col2
                with col2:
                    st.markdown("### 📊 Analysis Result")
                    
                    # Main result
                    color = get_complexity_color(highest_time_complexity)
                    st.markdown(
                        f'<div class="complexity-result" style="background-color: {color};">'
                        f'{highest_time_complexity}'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    
                    # Description
                    description = get_complexity_description(highest_time_complexity)
                    st.info(description)
                    
                    # Detailed breakdown
                    st.markdown("### 📈 Complexity Breakdown")
                    detected_complexities = [k for k, v in time_complexity_serial.items() if v]
                    
                    for complexity in detected_complexities:
                        color = get_complexity_color(complexity)
                        st.markdown(
                            f'<span style="color: {color}; font-weight: bold;">●</span> {complexity}',
                            unsafe_allow_html=True
                        )
                    
                    # Show debug output if recursion was detected
                    if debug_output:
                        st.markdown("### 🔍 Analysis Details")
                        for output in debug_output:
                            st.text(output)
                
                # Performance visualization
                st.markdown("---")
                st.markdown("### 📈 Performance Comparison")
                
                import pandas as pd
                import numpy as np
                
                # Generate sample data for visualization
                n_values = [10, 50, 100, 500, 1000]
                complexities = {
                    "O(1)": [1] * 5,
                    "O(log N)": [np.log2(n) for n in n_values],
                    "O(N)": n_values,
                    "O(N log N)": [n * np.log2(n) for n in n_values],
                    "O(N²)": [n**2 for n in n_values],
                    "O(N³)": [n**3 for n in n_values]
                }
                
                df = pd.DataFrame(complexities, index=n_values)
                st.line_chart(df)
                
                # Code metrics
                col3, col4, col5 = st.columns(3)
                
                with col3:
                    st.metric("Lines of Code", len(user_code.splitlines()))
                
                with col4:
                    functions_found = len(re.findall(r'\b(\w+)\s*\([^)]*\)\s*\{', user_code))
                    st.metric("Functions Found", functions_found)
                
                with col5:
                    loops_found = len(re.findall(r'(for|while)\s*\(', user_code))
                    st.metric("Loops Found", loops_found)
            
            else:
                st.warning("Please enter some code to analyze!")


if __name__ == "__main__":
    main()