import ast
import operator
import logging

logger = logging.getLogger(__name__)

# supported operators mapping
_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _OPS:
            result = _OPS[op_type](left, right)
            logger.debug("Eval BinOp: %s %s %s -> %s", left, node.op, right, result)
            return result
        raise ValueError(f"Unsupported operator: {op_type}")
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        val = _eval_node(node.operand)
        return +val if isinstance(node.op, ast.UAdd) else -val
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants allowed")
    if isinstance(node, ast.Num):
        return node.n
    raise ValueError(f"Unsupported expression node: {type(node)}")


def evaluate_expression(expr: str):
    """Safely evaluate a simple arithmetic expression containing + - * / and numbers.

    Returns a number (int/float). Raises ValueError on invalid input.
    """
    logger.info("Evaluating expression: %s", expr)
    try:
        node = ast.parse(expr, mode="eval")
        result = _eval_node(node)
        logger.info("Evaluated expression result: %s -> %s", expr, result)
        return result
    except Exception as e:
        logger.error("Failed to evaluate expression '%s': %s", expr, e)
        raise


def calculate(first: float, last: float, operator_symbol: str):
    """Perform a basic calculation between two numbers using the operator symbol."""
    logger.info("Calculate: %s %s %s", first, operator_symbol, last)
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }
    if operator_symbol not in ops:
        logger.error("Unsupported operator: %s", operator_symbol)
        raise ValueError('only simple math requiert')
    try:
        result = ops[operator_symbol](first, last)
        logger.info("Calculation result: %s", result)
        return result
    except Exception:
        logger.exception("Error during calculation")
        raise
