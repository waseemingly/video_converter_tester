from flask import Flask, jsonify, request, render_template
from test_runner import run_positive_test, run_negative_test_1, run_negative_test_2
import asyncio

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/run-positive-test', methods=['POST'])
def run_positive_test_case():
    test_result = asyncio.run(run_positive_test())
    return jsonify(test_result)

@app.route('/api/run-negative-test-1', methods=['POST'])
def run_negative_test_case_1():
    test_result = asyncio.run(run_negative_test_1())
    return jsonify(test_result)

@app.route("/api/run-negative-test-2", methods=["POST"])
def run_negative_test_case_2():
    test_result = asyncio.run(run_negative_test_2())
    return jsonify(test_result)

if __name__ == '__main__':
    app.run(debug=True)
