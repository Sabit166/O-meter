import re
import sys


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
                # Print the recursive calls found (for debugging)
                print(f"Found recursive calls in {func}: {matches}")
                print(f"Function body (no comments): {func_body_no_comments.strip()[:200]}...")
                
                # Case 3: Recursive call inside a loop -> O(N!) (check this first)
                if re.search(r'for\s*\([^)]*\)[^}]*{[^}]*' + pattern, func_body_no_comments, re.DOTALL):
                    detected = "O(N!)"
                    print(f"  -> Found recursive call inside loop: O(N!)")
                
                # Case 1: Single recursive call -> O(N)
                elif len(matches) == 1:
                    detected = "O(N)"
                    print(f"  -> Single recursive call: O(N)")

                # Case 2: Multiple recursive calls -> O(2^N) (like Fibonacci)
                elif len(matches) >= 2:
                    detected = "O(2^N)"
                    print(f"  -> Multiple recursive calls: O(2^N)")

    return detected


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


# Example usage:
if __name__ == "__main__":
    print("Enter your C/CPP code below. Press Ctrl+D (Unix/macOS) or Ctrl+Z then Enter (Windows) to finish:\n")
    code = sys.stdin.read()
    
    highest_time_complexity = "O(1)" #Initialize max time complexity to O(1)
    functions = [analyze_exponential, analyze_logarithmic, analyze_recursion] # Store functions in a list
    time_complexity_serial = {   #In the dictionary, the time complexities are organized in ascending order and initializedd to False
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
    
    for func in functions:
        result = func(code)
        if result in time_complexity_serial:
            time_complexity_serial[result] = True
            
    for complexity in ["O(log N)", "O(N)", "O(NLogN)", "O(N^2)", "O(N^2LogN)", "O(N^3)", "O(N^4)", "O(2^N)", "O(N!)"]:
        if time_complexity_serial[complexity]:
            highest_time_complexity = complexity        
            

    print("Worst-case complexity:", highest_time_complexity)
    # print("Detailed complexities:", time_complexity_serial)
