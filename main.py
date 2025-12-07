from typing import Callable

from flask import Flask, jsonify, request

from src.calc import Calculator

app = Flask(__name__)
calculator = Calculator()

def parse_nums() -> tuple[float, float] | tuple[None, None]:
    lhs_str: str = request.args.get("lhs", "")
    rhs_str: str = request.args.get("rhs", "")

    try:
        lhs = float(lhs_str)
        rhs = float(rhs_str)
        return lhs, rhs
    except (ValueError, TypeError):
        return None, None

def handle(operation: Callable[[float, float], float]):
    lhs, rhs = parse_nums()
    if lhs is None or rhs is None:
        return jsonify(error="Invalid input"), 400

    try:
        result = operation(lhs, rhs)
        return jsonify(result=result)
    except ZeroDivisionError:
        return jsonify(error="Cannot divide by zero"), 400


@app.get("/add")
def add():
    return handle(calculator.add)

@app.get("/subtract")
def subtract():
    return handle(calculator.subtract)

@app.get("/multiply")
def multiply():
    return handle(calculator.multiply)

@app.get("/divide")
def divide():
    return handle(calculator.divide)


if __name__ == "__main__":
    app.run(debug=True)
