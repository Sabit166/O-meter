import re
import sys

def analyze_exponential(code: str) -> str:

    max_depth = 0
    current_depth = 0

    # Split by lines for loop detection
    for line in code.splitlines():
        # Detect loop start
        if re.search(r'\b(for|while)\s*\(.*<\s*.*\)', line):
            current_depth += 1
            max_depth = max(max_depth, current_depth)

        # Detect block ending
        if "}" in line:
            # decrement only if we are inside a loop block
            if current_depth > 0:
                current_depth -= 1

    # Decide complexity from max depth
    if max_depth == 0:
        return "Unknown"
    elif max_depth == 1:
        return "O(N)"
    else:
        return f"O(N^{max_depth})"
    
    
def analyze_logarithmic(code: str) -> str:

    # Detect logN loops (i *= 2 or i /= 2)
    if re.search(r'for\s*\(.*;.*[*/]=\s*2.*\)', code):
        return "O(log N)"
    if re.search(r'while\s*\(.*\)\s*{', code) and re.search(r'i\s*=\s*i\s*[/\*]=\s*2', code):
        return "O(log N)"

    return "Unknown"


def analyze_factorial(code: str) -> str:

    # Detect "permute" or recursion inside a loop (factorial growth)
    if re.search(r'void\s+permute', code, re.IGNORECASE):
        return "O(N!)"

    # Generic heuristic: recursive call inside a for/while loop
    if re.search(r'for\s*\(.*\)\s*{[^}]*\b\w+\s*\(.*\)', code, re.DOTALL):
        return "O(N!)"

    return "Unknown"

import re

def analyze_recursion(code: str) -> str:
    # Detect recursive calls (function calling itself)
    functions = re.findall(r'\b(\w+)\s*\([^)]*\)\s*{', code)  # function names
    detected = "Unknown"

    for func in functions:
        # Look for recursive calls inside the function
        pattern = rf'{func}\s*\(.*\)'
        matches = re.findall(pattern, code)

        if matches:
            # Case 1: Single recursive call -> O(N)
            if len(matches) == 1:
                detected = "O(N)"

            # Case 2: Multiple recursive calls -> O(2^N)
            if len(matches) >= 2:
                detected = "O(2^N)"

            # Case 3: Recursive call inside a loop -> O(N!)
            if re.search(r'for\s*\(.*\)\s*{[^}]*' + pattern, code, re.DOTALL):
                detected = "O(N!)"

    return detected


# Example usage:
if __name__ == "__main__":
    print("Enter your C/CPP code below. Press Ctrl+D (Unix/macOS) or Ctrl+Z then Enter (Windows) to finish:\n")
    code = sys.stdin.read()
    
    highest_time_complexity = "O(1)" #Initialize max time complexity to O(1)
    functions = [analyze_exponential, analyze_logarithmic, analyze_factorial] # Store functions in a list
    time_complexity_serial = {   #In the dictionary, the time complexities are organized in ascending order and initializedd to False
        "O(log N)": False,
        "O(N)": False,
        "O(N^2)": False,
        "O(N^3)": False,
        "O(N^4)": False,
        "O(N!)": False
    }
    
    for func in functions:
        result = func(code)
        if result in time_complexity_serial:
            time_complexity_serial[result] = True
            
    for complexity in ["O(log N)", "O(N)", "O(N^2)", "O(N^3)", "O(N^4)", "O(N!)"]:
        if time_complexity_serial[complexity]:
            highest_time_complexity = complexity        #Highest time complexity is updated if a higher complexity is found
            

    print("Worst-case complexity:", highest_time_complexity)
    print("Detailed complexities:", time_complexity_serial)
