"""This module evaluates mathematical expressions that are contained in strings

Import:
    from helper import Math_Evaluator

Example:

    usage:
        Math_Evaluator.evaluate_math_expression("1+1")

@Author: Bradley Knorr
@Date: 1/22/2024
@Credit: jfs
@Links:
    https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string
@Credit:
"""
import ast
import numbers
import operator

# math operators
math_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.BitXor: operator.xor,
    ast.USub: operator.neg,
}

def evaluate_math_expression(expression: str) -> numbers.Number:
    """Calculates the result of a mathematical expression that is in string form

    Args:
        expression (string): expression to calculate

    Returns:
        number: Result of calculation
    """
    expression = expression.replace("^", "**")
    return evaluate_math_node_recursive(ast.parse(expression, mode="eval").body)

def evaluate_math_node_recursive(node: ast.Expression) -> numbers.Number:
    """Recursively calculates the result of a mathematical expression

    Args:
        node (ast.Expression): expression to calculate

    Raises:
        TypeError: not an ast node

    Returns:
        numbers.Number: Result of calculation
    """
    if isinstance(node, ast.Constant):  # <number>
        return node.n

    if isinstance(node, ast.BinOp):  # <left> <operator> <right>
        return math_operators[type(node.op)](
            evaluate_math_node_recursive(node.left),
            evaluate_math_node_recursive(node.right),
        )

    if isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        return math_operators[type(node.op)](
            evaluate_math_node_recursive(node.operand)
        )

    raise TypeError(node)
