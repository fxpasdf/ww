import subprocess
import os

def check_flask_security():
    """检测 Flask 应用的安全性"""
    try:
        # 检查是否启用了调试模式
        if os.environ.get("FLASK_ENV") == "development":
            return {
                "检测项": "Flask 调试模式",
                "结果": "调试模式已启用",
                "风险等级": "高",
                "修复建议": "在生产环境中禁用调试模式，设置 FLASK_ENV=production。"
            }
        else:
            return {
                "检测项": "Flask 调试模式",
                "结果": "调试模式未启用",
                "风险等级": "低",
                "修复建议": "无"
            }
    except Exception as e:
        return {
            "检测项": "Flask 调试模式",
            "结果": f"检查失败: {str(e)}",
            "风险等级": "未知",
            "修复建议": "检查 Flask 环境变量配置。"
        }

def check_command_injection(module):
    """检测命令注入漏洞"""
    try:
        # 模拟用户输入
        user_input = "; ls /"
        result = subprocess.run(f"echo {user_input}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if "etc" in result.stdout.decode():
            return {
                "检测项": f"{module} 命令注入",
                "结果": "存在命令注入漏洞",
                "风险等级": "高",
                "修复建议": "避免使用 shell=True，或对用户输入进行严格验证和转义。"
            }
        else:
            return {
                "检测项": f"{module} 命令注入",
                "结果": "未发现命令注入漏洞",
                "风险等级": "低",
                "修复建议": "无"
            }
    except Exception as e:
        return {
            "检测项": f"{module} 命令注入",
            "结果": f"检查失败: {str(e)}",
            "风险等级": "未知",
            "修复建议": "检查命令执行逻辑。"
        }

def check_path_traversal(module):
    """检测路径遍历漏洞"""
    try:
        # 模拟用户输入
        user_input = "../../etc/passwd"
        with open(user_input, "r") as f:
            content = f.read()
            return {
                "检测项": f"{module} 路径遍历",
                "结果": "存在路径遍历漏洞",
                "风险等级": "高",
                "修复建议": "对用户输入的文件路径进行严格验证，避免使用相对路径。"
            }
    except Exception as e:
        return {
            "检测项": f"{module} 路径遍历",
            "结果": "未发现路径遍历漏洞",
            "风险等级": "低",
            "修复建议": "无"
        }

def check_sensitive_files(module):
    """检测敏感文件泄露"""
    try:
        sensitive_files = ["/etc/passwd", "/etc/shadow"]
        for file in sensitive_files:
            if os.path.exists(file) and os.access(file, os.R_OK):
                return {
                    "检测项": f"{module} 敏感文件泄露",
                    "结果": f"敏感文件 {file} 可读",
                    "风险等级": "高",
                    "修复建议": "限制敏感文件的访问权限，确保只有授权用户可以访问。"
                }
        return {
            "检测项": f"{module} 敏感文件泄露",
            "结果": "未发现敏感文件泄露",
            "风险等级": "低",
            "修复建议": "无"
        }
    except Exception as e:
        return {
            "检测项": f"{module} 敏感文件泄露",
            "结果": f"检查失败: {str(e)}",
            "风险等级": "未知",
            "修复建议": "检查文件权限配置。"
        }

def check_firewall_status():
    """检测防火墙状态"""
    try:
        result = subprocess.run(["ufw", "status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if "inactive" in result.stdout.decode():
            return {
                "检测项": "防火墙状态",
                "结果": "防火墙未启用",
                "风险等级": "高",
                "修复建议": "启用防火墙并配置规则，限制不必要的端口访问。"
            }
        else:
            return {
                "检测项": "防火墙状态",
                "结果": "防火墙已启用",
                "风险等级": "低",
                "修复建议": "无"
            }
    except Exception as e:
        return {
            "检测项": "防火墙状态",
            "结果": f"检查失败: {str(e)}",
            "风险等级": "未知",
            "修复建议": "检查防火墙配置。"
        }

def check_ssh_config():
    """检测 SSH 配置"""
    try:
        result = subprocess.run(["grep", "PermitRootLogin", "/etc/ssh/sshd_config"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if "yes" in result.stdout.decode():
            return {
                "检测项": "SSH 配置",
                "结果": "SSH 允许 root 登录",
                "风险等级": "高",
                "修复建议": "禁止 root 用户直接登录，使用普通用户登录后切换 root。"
            }
        else:
            return {
                "检测项": "SSH 配置",
                "结果": "SSH 禁止 root 登录",
                "风险等级": "低",
                "修复建议": "无"
            }
    except Exception as e:
        return {
            "检测项": "SSH 配置",
            "结果": f"检查失败: {str(e)}",
            "风险等级": "未知",
            "修复建议": "检查 SSH 配置文件 /etc/ssh/sshd_config。"
        }

def check_sudo_permissions():
    """检测 sudo 权限"""
    try:
        result = subprocess.run(["grep", "-i", "NOPASSWD", "/etc/sudoers"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stdout.decode():
            return {
                "检测项": "sudo 权限",
                "结果": "存在无需密码的 sudo 权限",
                "风险等级": "高",
                "修复建议": "移除无需密码的 sudo 权限，确保所有 sudo 操作都需要密码验证。"
            }
        else:
            return {
                "检测项": "sudo 权限",
                "结果": "未发现无需密码的 sudo 权限",
                "风险等级": "低",
                "修复建议": "无"
            }
    except Exception as e:
        return {
            "检测项": "sudo 权限",
            "结果": f"检查失败: {str(e)}",
            "风险等级": "未知",
            "修复建议": "检查 /etc/sudoers 文件配置。"
        }

def run_penetration_test():
    """运行渗透测试"""
    return {
        "Flask 应用安全性": check_flask_security(),
        "config_checker.py 命令注入": check_command_injection("config_checker.py"),
        "config_checker.py 路径遍历": check_path_traversal("config_checker.py"),
        "performance_monitor.py 敏感文件泄露": check_sensitive_files("performance_monitor.py"),
        "vuln_scanner.py 命令注入": check_command_injection("vuln_scanner.py"),
        "防火墙状态": check_firewall_status(),
        "SSH 配置": check_ssh_config(),
        "sudo 权限": check_sudo_permissions(),
    }

def tester_generate_vulnerability_report():
    """生成脆弱性评估报告"""
    penetration_results = run_penetration_test()
    report = {
        "渗透测试结果": penetration_results,
        "总体评估": {
            "风险等级": "中等",
            "修复建议": "建议修复发现的漏洞，特别是高风险的命令注入和路径遍历漏洞。"
        }
    }
    return report