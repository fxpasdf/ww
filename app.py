from flask import Flask, render_template, jsonify
from config_checker import get_config_checks
from vuln_scanner import get_vuln_checks
from performance_monitor import get_performance_checks
from penetration_tester import tester_generate_vulnerability_report
from code_auditor import generate_code_audit_report
from vulnerability_reporter import generate_vulnerability_report

from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route("/config")
def config_check():
    return jsonify(get_config_checks())

@app.route("/vuln")
def vuln_check():
    return jsonify(get_vuln_checks())

@app.route("/performance")
def performance_check():
    return jsonify(get_performance_checks())
@app.route('/penetration_test', methods=['GET'])
def penetration_test():
    """渗透测试"""
    return jsonify(tester_generate_vulnerability_report())

@app.route('/code_audit', methods=['GET'])
def code_audit():
    """代码审计"""
    return jsonify(generate_code_audit_report())

@app.route('/vulnerability_report', methods=['GET'])
def vulnerability_report():
    """生成系统脆弱性评估报告"""
    return jsonify(generate_vulnerability_report())
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
