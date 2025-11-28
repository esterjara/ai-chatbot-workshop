"""
Tool Functions for Exercise 3

Reusable tool implementations for the multi-agent exercises.
These functions are shared between 3a and 3b exercises.
"""

import re
import math


def calculator(input: str) -> str:
    """
    Performs basic mathematical calculations.
    
    Supports: addition (+, plus), subtraction (-, minus), multiplication (*, times), division (/, divided by)
    
    Args:
        input: Math expression like "5 + 3", "10 * 2", or "8 plus 4"
        
    Returns:
        Calculated result or error message
    """
    try:
        input = input.strip().lower()
        
        # Extract numbers from the input
        numbers = re.findall(r'\d+\.?\d*', input)
        if len(numbers) < 2:
            return "Invalid expression. Need two numbers."
        
        a = float(numbers[0])
        b = float(numbers[1])
        
        # Determine operation based on symbols or words
        if "+" in input or "plus" in input or "add" in input:
            result = a + b
            op_display = "+"
        elif "-" in input or "minus" in input or "subtract" in input:
            result = a - b
            op_display = "-"
        elif "*" in input or "times" in input or "multiply" in input or "multiplied" in input:
            result = a * b
            op_display = "*"
        elif "/" in input or "divided" in input or "divide" in input:
            if b == 0:
                return "Error: Cannot divide by zero"
            result = a / b
            op_display = "/"
        else:
            return "Invalid expression. Supported operations: +, -, *, / (or plus, minus, times, divided by)"
        
        # Format result
        if result == int(result):
            return f"{a} {op_display} {b} = {int(result)}"
        else:
            return f"{a} {op_display} {b} = {result:.2f}"
    except Exception as e:
        return f"Calculation error: {str(e)}"


def advanced_math(input: str) -> str:
    """
    Advanced mathematical operations.
    
    Supports: square root, power/exponentiation
    
    Args:
        input: Description like "square root of 16" or "2 to the power of 3"
        
    Returns:
        Calculated result
    """
    try:
        input = input.lower().strip()
        
        # Square root
        if "square root" in input or "sqrt" in input:
            numbers = re.findall(r'\d+\.?\d*', input)
            if numbers:
                num = float(numbers[0])
                result = num ** 0.5
                return f"√{num} = {result:.2f}"
        
        # Power
        if "power" in input or "^" in input:
            numbers = re.findall(r'\d+\.?\d*', input)
            if len(numbers) >= 2:
                base, exp = float(numbers[0]), float(numbers[1])
                result = base ** exp
                return f"{base}^{exp} = {result:.2f}"
        
        return "Unsupported input. Try: 'square root of 16' or '2 power 3'"
    except Exception as e:
        return f"Error: {str(e)}"
