import ast

class CodeAuditor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.issues = []

    def check_hardcoded_secrets(self, node):
        """检查硬编码的敏感信息（如密码、密钥）"""
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and isinstance(node.value, ast.Str):
                    if "password" in target.id.lower() or "secret" in target.id.lower():
                        self.issues.append({
                            "检测项": "硬编码敏感信息",
                            "结果": f"发现硬编码敏感信息: {target.id} = {node.value.s}",
                            "风险等级": "高",
                            "修复建议": "移除硬编码的敏感信息，使用环境变量或安全的配置管理工具。"
                        })

    def check_unsafe_functions(self, node):
        """检查不安全的函数调用（如 `os.system`、`subprocess.run` 的 `shell=True`）"""
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if node.func.attr == "system" and isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                    self.issues.append({
                        "检测项": "不安全的函数调用",
                        "结果": "发现不安全的函数调用: os.system",
                        "风险等级": "高",
                        "修复建议": "避免使用 os.system，改用 subprocess.run 并禁用 shell=True。"
                    })
                if node.func.attr == "run" and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
                    for keyword in node.keywords:
                        if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                            self.issues.append({
                                "检测项": "不安全的函数调用",
                                "结果": "发现不安全的函数调用: subprocess.run(shell=True)",
                                "风险等级": "高",
                                "修复建议": "避免使用 shell=True，或对用户输入进行严格验证和转义。"
                            })
            elif isinstance(node.func, ast.Name):
                if node.func.id == "eval":
                    self.issues.append({
                        "检测项": "不安全的函数调用",
                        "结果": "发现不安全的函数调用: eval",
                        "风险等级": "高",
                        "修复建议": "避免使用 eval，改用更安全的替代方案。"
                    })

    def check_unvalidated_input(self, node):
        """检查未验证的用户输入"""
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in ["input", "get"]:
                    self.issues.append({
                        "检测项": "未验证的用户输入",
                        "结果": f"发现未验证的用户输入: {node.func.id}",
                        "风险等级": "中",
                        "修复建议": "对用户输入进行严格验证和过滤，避免直接使用未经验证的输入。"
                    })

    def check_file_permissions(self, node):
        """检查文件权限相关操作"""
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if node.func.attr == "chmod" and isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                    self.issues.append({
                        "检测项": "文件权限操作",
                        "结果": "发现文件权限操作: os.chmod",
                        "风险等级": "中",
                        "修复建议": "确保文件权限操作的安全性，避免设置过于宽松的权限。"
                    })

    def check_imports(self, node):
        """检查导入的模块"""
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "pickle":
                    self.issues.append({
                        "检测项": "不安全的模块导入",
                        "结果": "发现不安全的模块导入: pickle",
                        "风险等级": "高",
                        "修复建议": "避免使用 pickle，改用更安全的序列化工具（如 json）。"
                    })
        elif isinstance(node, ast.ImportFrom):
            if node.module == "os" and "system" in [name.name for name in node.names]:
                self.issues.append({
                    "检测项": "不安全的模块导入",
                    "结果": "发现不安全的模块导入: from os import system",
                    "风险等级": "高",
                    "修复建议": "避免直接导入 os.system，改用更安全的替代方案。"
                })

    def analyze_file(self):
        """分析代码文件"""
        try:
            with open(self.file_path, "r") as f:
                tree = ast.parse(f.read(), filename=self.file_path)
                for node in ast.walk(tree):
                    self.check_hardcoded_secrets(node)
                    self.check_unsafe_functions(node)
                    self.check_unvalidated_input(node)
                    self.check_file_permissions(node)
                    self.check_imports(node)
        except Exception as e:
            self.issues.append({
                "检测项": "文件解析",
                "结果": f"文件解析失败: {str(e)}",
                "风险等级": "未知",
                "修复建议": "检查代码文件格式和语法。"
            })

def run_code_audit():
    """运行代码审计"""
    files_to_audit = ["app.py", "config_checker.py", "penetration_tester.py", "performance_monitor.py", "vuln_scanner.py","vulnerability_reporter.py"]
    results = {}

    for file in files_to_audit:
        auditor = CodeAuditor(file)
        auditor.analyze_file()
        results[file] = auditor.issues if auditor.issues else [{
            "检测项": "代码审计",
            "结果": "未发现问题",
            "风险等级": "低",
            "修复建议": "无"
        }]

    return results

def generate_code_audit_report():
    """生成代码审计报告"""
    audit_results = run_code_audit()
    report = {
        "代码审计结果": audit_results,
        "总体评估": {
            "风险等级": "中等",
            "修复建议": "建议修复发现的高风险问题，特别是硬编码敏感信息和不安全的函数调用。"
        }
    }
    return report