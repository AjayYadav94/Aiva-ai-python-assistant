from datetime import datetime
import ast
import operator
import json
import requests
import os
from decimal import Decimal, InvalidOperation
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from dotenv import load_dotenv
  
load_dotenv()

# -----------------------------
# 1. Safe Calculator
# -----------------------------

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval(node):
    """Safely evaluate a mathematical expression."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](_safe_eval(node.operand))

    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)

        # Prevent absurd exponent calculations.
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("Exponent is too large.")

        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    raise ValueError("Unsupported mathematical expression.")


def calculate(expression: str) -> str:
    """Calculate a mathematical expression.

    Args:
        expression: A mathematical expression such as
            245 * 37 or (100 + 50) / 3.

    Returns:
        The calculated result.
    """
    try:
        expression = expression.strip()

        if not expression:
            return "Please provide a mathematical expression."

        tree = ast.parse(expression, mode="eval")
        result = _safe_eval(tree.body)

        return str(result)

    except ZeroDivisionError:
        return "Error: division by zero is not allowed."

    except Exception:
        return "I couldn't safely calculate that expression."


# -----------------------------
# 2. Date and Time
# -----------------------------

def get_current_datetime() -> str:
    """Get the current local date and time from the server."""
    now = datetime.now()

    return now.strftime(
        "%A, %d %B %Y at %I:%M:%S %p"
    )


# -----------------------------
# 3. Unit Converter
# -----------------------------

_CONVERSIONS = {
    ("km", "miles"): 0.621371,
    ("miles", "km"): 1.609344,
    ("meters", "feet"): 3.28084,
    ("feet", "meters"): 0.3048,
    ("kg", "pounds"): 2.2046226218,
    ("pounds", "kg"): 0.45359237,
    ("celsius", "fahrenheit"): lambda x: (x * 9 / 5) + 32,
    ("fahrenheit", "celsius"): lambda x: (x - 32) * 5 / 9,
}


def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """Convert a value between supported units.

    Args:
        value: Numeric value to convert.
        from_unit: Unit the value is currently in.
        to_unit: Unit to convert to.

    Returns:
        Converted value as a readable string.
    """
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()

    key = (from_unit, to_unit)

    if key not in _CONVERSIONS:
        supported = ", ".join(
            f"{a} -> {b}" for a, b in _CONVERSIONS.keys()
        )
        return f"Unsupported conversion. Supported conversions: {supported}"

    converter = _CONVERSIONS[key]

    try:
        if callable(converter):
            result = converter(value)
        else:
            result = value * converter

        return f"{value:g} {from_unit} = {result:.6g} {to_unit}"

    except Exception:
        return "I couldn't perform that conversion."
def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str
) -> str:
    """Convert money using the latest available Frankfurter exchange rate."""

    try:
        source = from_currency.strip().upper()
        target = to_currency.strip().upper()

        if len(source) != 3 or len(target) != 3:
            return "Please use three-letter currency codes such as USD, EUR, or INR."

        value = Decimal(str(amount))

        if value < 0:
            return "Please provide a non-negative amount."

        if source == target:
            return f"{value:.2f} {source} = {value:.2f} {target}"

        response = requests.get(
            f"https://api.frankfurter.dev/v2/rate/{source}/{target}",
            timeout=10,
        )

        if response.status_code == 404:
            return (
                f"I couldn't find an exchange rate for "
                f"{source} to {target}."
            )

        response.raise_for_status()

        data = response.json()

        rate = Decimal(str(data["rate"]))
        converted = value * rate
        rate_date = data.get("date", "unknown")

        return (
            f"{value:.2f} {source} = {converted:.2f} {target}. "
            f"Exchange rate: 1 {source} = {rate:.6f} {target}. "
            f"Rate date: {rate_date}."
        )

    except requests.Timeout:
        return "The currency service took too long to respond."

    except requests.RequestException as exc:
        print(f"Frankfurter request failed: {type(exc).__name__}: {exc}")
        return "I couldn't connect to the currency service right now."

    except (InvalidOperation, ValueError, TypeError, KeyError) as exc:
        print(f"Currency conversion failed: {type(exc).__name__}: {exc}")
        return "I couldn't process that currency conversion."

    except Exception as exc:
        print(f"Currency conversion failed: {type(exc).__name__}: {exc}")
        return "The currency conversion could not be completed."
def web_search(query: str) -> str:
    """Search the web using Tavily and return useful results."""
    try:
        from tavily import TavilyClient

        api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            return "Web search is not configured."

        if not query or not query.strip():
            return "Please provide a search query."

        client = TavilyClient(api_key=api_key)

        response = client.search(
            query=query.strip(),
            search_depth="basic",
            max_results=5,
            include_answer=False,
        )

        results = response.get("results", [])

        if not results:
            return "No useful web results were found."

        formatted = []

        for index, result in enumerate(results, start=1):
            title = result.get("title", "Untitled")
            url = result.get("url", "")
            content = result.get("content", "")

            formatted.append(
                f"{index}. {title}\n"
                f"URL: {url}\n"
                f"Snippet: {content[:700]}"
            )

        return "\n\n".join(formatted)

    except Exception as exc:
        print(f"Web search failed: {type(exc).__name__}: {exc}")
        return "Web search could not be completed."