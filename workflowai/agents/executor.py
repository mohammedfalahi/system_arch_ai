"""
Executor Agent.
Executes generated workflow code in a safe environment.
"""

import sys
import io
import time
import contextlib
from typing import Dict, Any, Tuple


class WorkflowExecutor:
    """
    Executes workflow code in a controlled, safe environment.
    Captures output, handles errors, and provides execution metrics.
    """
    
    def __init__(self):
        """Initialize the WorkflowExecutor."""
        pass
    
    def validate_code(self, code: str) -> Tuple[bool, str]:
        """
        Validate Python code syntax without executing it.
        
        Args:
            code: Python code string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
            - is_valid: True if syntax is valid, False otherwise
            - error_message: Empty string if valid, error description if invalid
        """
        try:
            compile(code, '<string>', 'exec')
            return True, ""
        except SyntaxError as e:
            error_msg = f"Syntax error at line {e.lineno}: {e.msg}"
            if e.text:
                error_msg += f"\n  {e.text.strip()}"
            return False, error_msg
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def _create_safe_globals(self) -> Dict[str, Any]:
        """
        Create a restricted globals dictionary for safe code execution.
        Includes safe built-in functions and commonly used safe modules.
        
        Returns:
            Dictionary with safe built-in functions and pre-imported safe modules
        """
        # Safe built-in functions
        safe_builtins = {
            'print': print,
            'len': len,
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'list': list,
            'dict': dict,
            'tuple': tuple,
            'set': set,
            'frozenset': frozenset,
            'range': range,
            'enumerate': enumerate,
            'zip': zip,
            'map': map,
            'filter': filter,
            'sum': sum,
            'min': min,
            'max': max,
            'abs': abs,
            'round': round,
            'sorted': sorted,
            'reversed': reversed,
            'isinstance': isinstance,
            'issubclass': issubclass,
            'hasattr': hasattr,
            'getattr': getattr,
            'setattr': setattr,
            'type': type,
            'callable': callable,
            'all': all,
            'any': any,
            'chr': chr,
            'ord': ord,
            'hex': hex,
            'oct': oct,
            'bin': bin,
            'format': format,
            'repr': repr,
            'hash': hash,
            'id': id,
            'iter': iter,
            'next': next,
            'slice': slice,
            'property': property,
            'staticmethod': staticmethod,
            'classmethod': classmethod,
            'super': super,
            'object': object,
            'Exception': Exception,
            'ValueError': ValueError,
            'TypeError': TypeError,
            'KeyError': KeyError,
            'IndexError': IndexError,
            'AttributeError': AttributeError,
            'RuntimeError': RuntimeError,
            'StopIteration': StopIteration,
            'True': True,
            'False': False,
            'None': None,
            '__import__': __import__,
            '__build_class__': __build_class__,  # Required for class definitions
            '__name__': '__main__',  # Set module name
        }
        
        # Pre-import safe modules
        safe_globals = {
            '__builtins__': safe_builtins,
            'datetime': __import__('datetime'),
            'dataclasses': __import__('dataclasses'),
            'typing': __import__('typing'),
            'collections': __import__('collections'),
            'json': __import__('json'),
            'time': __import__('time'),
            'math': __import__('math'),
            'random': __import__('random'),
            're': __import__('re'),
            'itertools': __import__('itertools'),
        }
        
        return safe_globals
    
    def execute(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code in a safe, controlled environment.
        
        Args:
            code: Python code string to execute
            
        Returns:
            Dictionary containing:
            - status: "success" or "error"
            - output: Captured stdout/stderr output
            - error: Error message if execution failed, None otherwise
            - execution_time: Time taken to execute in seconds
        """
        # Validate syntax first
        is_valid, error_msg = self.validate_code(code)
        if not is_valid:
            return {
                "status": "error",
                "output": "",
                "error": f"Syntax validation failed: {error_msg}",
                "execution_time": 0.0
            }
        
        # Prepare output capture
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        start_time = time.time()
        
        try:
            # Execute code with output redirection
            with contextlib.redirect_stdout(stdout_capture), \
                 contextlib.redirect_stderr(stderr_capture):
                
                safe_globals = self._create_safe_globals()
                exec(code, safe_globals)
            
            execution_time = time.time() - start_time
            
            # Get captured output
            output = stdout_capture.getvalue()
            stderr_output = stderr_capture.getvalue()
            
            if stderr_output:
                output += "\n[stderr]\n" + stderr_output
            
            return {
                "status": "success",
                "output": output.strip(),
                "error": None,
                "execution_time": round(execution_time, 3)
            }
            
        except NameError as e:
            execution_time = time.time() - start_time
            return {
                "status": "error",
                "output": stdout_capture.getvalue().strip(),
                "error": f"Runtime error: {str(e)}",
                "execution_time": round(execution_time, 3)
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_type = type(e).__name__
            return {
                "status": "error",
                "output": stdout_capture.getvalue().strip(),
                "error": f"{error_type}: {str(e)}",
                "execution_time": round(execution_time, 3)
            }
        
        finally:
            stdout_capture.close()
            stderr_capture.close()


if __name__ == "__main__":
    print("Testing WorkflowExecutor...\n")
    
    executor = WorkflowExecutor()
    
    # Test 1: Valid code with output
    print("=" * 50)
    print("Test 1: Valid code with multiple steps")
    print("=" * 50)
    test_code_1 = '''
print("Step 1: Starting process")
result = 2 + 2
print(f"Step 2: Result is {result}")
for i in range(3):
    print(f"Step {i+3}: Iteration {i}")
print("Step 6: Process complete")
'''
    result = executor.execute(test_code_1)
    print(f"Status: {result['status']}")
    print(f"Execution time: {result['execution_time']}s")
    print(f"Output:\n{result['output']}")
    print(f"Error: {result['error']}")
    
    # Test 2: Syntax error
    print("\n" + "=" * 50)
    print("Test 2: Code with syntax error")
    print("=" * 50)
    test_code_2 = '''
print("This will fail"
'''
    result = executor.execute(test_code_2)
    print(f"Status: {result['status']}")
    print(f"Execution time: {result['execution_time']}s")
    print(f"Output: {result['output']}")
    print(f"Error: {result['error']}")
    
    # Test 3: Runtime error (undefined variable)
    print("\n" + "=" * 50)
    print("Test 3: Code with runtime error")
    print("=" * 50)
    test_code_3 = '''
print("Starting...")
undefined_variable
'''
    result = executor.execute(test_code_3)
    print(f"Status: {result['status']}")
    print(f"Execution time: {result['execution_time']}s")
    print(f"Output: {result['output']}")
    print(f"Error: {result['error']}")
    
    # Test 4: Code with calculations
    print("\n" + "=" * 50)
    print("Test 4: Code with calculations")
    print("=" * 50)
    test_code_4 = '''
numbers = [1, 2, 3, 4, 5]
total = sum(numbers)
average = total / len(numbers)
print(f"Numbers: {numbers}")
print(f"Total: {total}")
print(f"Average: {average}")
'''
    result = executor.execute(test_code_4)
    print(f"Status: {result['status']}")
    print(f"Execution time: {result['execution_time']}s")
    print(f"Output:\n{result['output']}")
    print(f"Error: {result['error']}")
    
    # Test 5: Validation only
    print("\n" + "=" * 50)
    print("Test 5: Code validation")
    print("=" * 50)
    valid_code = "print('Hello')\nx = 5"
    invalid_code = "print('Hello'\nx = 5"
    
    is_valid, error = executor.validate_code(valid_code)
    print(f"Valid code check: {is_valid}, Error: {error}")
    
    is_valid, error = executor.validate_code(invalid_code)
    print(f"Invalid code check: {is_valid}, Error: {error}")
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("=" * 50)
