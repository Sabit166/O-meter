import re
import sys





def analyze_exponential(code: str) -> str:
    
    FOR_LOOP_O_N = r'for\s*\(\s*(int|char|float|double)?\s*(\w+)\s*=.*?[<>=!]+.*?(\+\+|--|[\+-]+=)'
    FOR_LOOP_O_LOGN = r'for\s*\(\s*(int|char|float|double)?\s*(\w+)\s*=.*?[<>=!]+.*?(\*|/)=\s*\d+'

    WHILE_LOOP_O_N = r'while\s*\(\s*(\w+)(?:\s*[<>=!]+.*?)?\s*\)'
    WHILE_LOOP_O_LOGN = r'(\w+)\s*(\*|/)=\s*\d+'
    
    
    max_depth = 0
    current_depth = 0
    log_n_detected = False
    inside_while = False
    while_variable = None

    for line in code.splitlines():
        line = line.strip()  # Remove leading/trailing whitespace
        
        for_match = re.search(FOR_LOOP_O_N, line)
        log_match = re.search(FOR_LOOP_O_LOGN, line)
        
        if for_match or log_match:
            current_depth += 1
            max_depth = max(max_depth, current_depth)
            
            # Check if this loop is logarithmic
            if log_match:
                log_n_detected = True
        
        # Detect while loop start
        elif re.search(WHILE_LOOP_O_N, line):
            while_match = re.search(WHILE_LOOP_O_N, line)
            if while_match:
                while_variable = while_match.group(1)
                inside_while = True
                current_depth += 1
                max_depth = max(max_depth, current_depth)
        
        # Check for logarithmic operations inside while loop
        if inside_while and while_variable:
            log_match = re.search(WHILE_LOOP_O_LOGN, line)
            if log_match and log_match.group(1) == while_variable:
                log_n_detected = True

        # Detect block ending - only on closing braces
        if "}" in line:
            if current_depth > 0:
                current_depth -= 1
                if inside_while and current_depth == 0:
                    inside_while = False
                    while_variable = None

    # Decide complexity from max depth
    if max_depth == 0:
        return "O(1)"
    else:
        time_complexity = ""
        if max_depth == 1:
            if log_n_detected:
                time_complexity = "LogN"  # Single logarithmic loop
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
    
    


def analyze_factorial(code: str) -> str:
    # Detect permutation/combination functions
    if re.search(r'(permut|factorial|combinations?|arrangements?)', code, re.IGNORECASE):
        return "O(N!)"
    
    # Detect recursive calls inside loops (more specific)
    functions = re.findall(r'\b(\w+)\s*\([^)]*\)\s*{', code)
    
    for func in functions:
        # Look for function calling itself inside a loop
        pattern = rf'for\s*\([^)]*\)\s*{{[^}}]*{func}\s*\([^)]*\)[^}}]*}}'
        if re.search(pattern, code, re.DOTALL):
            return "O(N!)"
    
    # Detect multiple recursive calls in same function (like generating all subsets/permutations)
    for func in functions:
        func_body_pattern = rf'{func}\s*\([^)]*\)\s*{{([^{{}}]*(?:{{[^{{}}]*}}[^{{}}]*)*)}}'
        func_match = re.search(func_body_pattern, code, re.DOTALL)
        
        if func_match:
            func_body = func_match.group(1)
            recursive_calls = len(re.findall(rf'{func}\s*\([^)]*\)', func_body))
            
            # If multiple recursive calls + loop, likely factorial
            if recursive_calls > 1 and re.search(r'for\s*\(', func_body):
                return "O(N!)"
    
    return "O(1)"


def analyze_recursion(code: str) -> str:
    # Detect recursive calls (function calling itself)
    functions = re.findall(r'\b(\w+)\s*\([^)]*\)\s*{', code)  # function names
    detected = "O(1)"  # Default if no recursion found

    for func in functions:
        # Look for the function body
        func_pattern = rf'{func}\s*\([^)]*\)\s*{{([^{{}}]*(?:{{[^{{}}]*}}[^{{}}]*)*)}}'
        func_match = re.search(func_pattern, code, re.DOTALL)
        
        if func_match:
            func_body = func_match.group(1)
            
            # Look for recursive calls inside the function
            pattern = rf'{func}\s*\([^)]*\)'
            matches = re.findall(pattern, func_body)

            if matches:
                # Skip if this is already detected as log N (divide and conquer)
                if re.search(r'(n\s*/\s*2|mid\s*[-+]\s*1|left.*mid.*right|\w+\s*/\s*2)', func_body):
                    continue  # Let analyze_logarithmic handle this
                
                # Case 1: Single recursive call -> O(N)
                if len(matches) == 1:
                    detected = "O(N)"

                # Case 2: Multiple recursive calls -> O(2^N) (like Fibonacci)
                if len(matches) >= 2:
                    detected = "O(2^N)"

                # Case 3: Recursive call inside a loop -> O(N!)
                if re.search(r'for\s*\(.*\)\s*{[^}]*' + pattern, func_body, re.DOTALL):
                    detected = "O(N!)"

    return detected


# Example usage:
if __name__ == "__main__":
    print("Enter your C/CPP code below. Press Ctrl+D (Unix/macOS) or Ctrl+Z then Enter (Windows) to finish:\n")
    code = sys.stdin.read()
    
    highest_time_complexity = "O(1)" #Initialize max time complexity to O(1)
    functions = [analyze_exponential, analyze_factorial, analyze_recursion] # Store functions in a list
    time_complexity_serial = {   #In the dictionary, the time complexities are organized in ascending order and initializedd to False
        "O(log N)": False,
        "O(N)": False,
        "O(N^2)": False,
        "O(N^3)": False,
        "O(N^4)": False,
        "O(2^N)": False,
        "O(N!)": False
    }
    
    for func in functions:
        result = func(code)
        if result in time_complexity_serial:
            time_complexity_serial[result] = True
            
    for complexity in ["O(log N)", "O(N)", "O(N^2)", "O(N^3)", "O(N^4)", "O(2^N)", "O(N!)"]:
        if time_complexity_serial[complexity]:
            highest_time_complexity = complexity        #Highest time complexity is updated if a higher complexity is found
            

    print("Worst-case complexity:", highest_time_complexity)
    print("Detailed complexities:", time_complexity_serial)
