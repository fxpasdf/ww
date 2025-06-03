import subprocess
import os

def check_ssh_config():
    """检查 SSH 配置"""
    try:
        result = subprocess.run(["sshd", "-T"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return "SSH 配置正常"
        else:
            return f"SSH 配置异常: {result.stderr.decode().strip()}"
    except Exception as e:
        return f"SSH 配置检查失败: {str(e)}"

def check_users():
    """检查用户账号"""
    try:
        with open("/etc/passwd", "r") as f:
            users = f.readlines()
            return f"用户账号正常，共 {len(users)} 个用户"
    except Exception as e:
        return f"用户账号检查失败: {str(e)}"

def check_file_permissions():
    """检查关键文件权限"""
    critical_files = ["/etc/passwd", "/etc/shadow", "/etc/group"]
    results = {}
    for file in critical_files:
        try:
            mode = os.stat(file).st_mode
            if oct(mode)[-3:] != "644":
                results[file] = f"权限异常: {oct(mode)[-3:]}"
            else:
                results[file] = "权限正常"
        except Exception as e:
            results[file] = f"检查失败: {str(e)}"
    return results

def find_777_files():
    """查找 777 权限文件"""
    try:
        result = subprocess.run(["find", "/", "-perm", "777"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        files = result.stdout.decode().splitlines()
        return f"找到 {len(files)} 个 777 权限文件" if files else "未找到 777 权限文件"
    except Exception as e:
        return f"查找 777 权限文件失败: {str(e)}"

def check_firewall():
    """检查防火墙状态"""
    try:
        result = subprocess.run(["ufw", "status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if "active" in result.stdout.decode():
            return "防火墙已启用"
        else:
            return "防火墙未启用"
    except Exception as e:
        return f"防火墙检查失败: {str(e)}"

def check_sudo_logs():
    """检查 sudo 命令日志"""
    try:
        with open("/var/log/auth.log", "r") as f:
            logs = f.read()
            return "sudo 命令日志正常" if "sudo" in logs else "未找到 sudo 命令日志"
    except Exception as e:
        return f"sudo 命令日志检查失败: {str(e)}"

def check_ssh_login_failures():
    """检查 SSH 登录失败记录"""
    try:
        result = subprocess.run(["grep", "Failed password", "/var/log/auth.log"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        failures = result.stdout.decode().splitlines()
        return f"找到 {len(failures)} 条 SSH 登录失败记录" if failures else "未找到 SSH 登录失败记录"
    except Exception as e:
        return f"SSH 登录失败记录检查失败: {str(e)}"

def check_hosts_file():
    """检查 /etc/hosts 文件"""
    try:
        with open("/etc/hosts", "r") as f:
            content = f.read()
            return "/etc/hosts 文件正常" if content else "/etc/hosts 文件为空"
    except Exception as e:
        return f"/etc/hosts 文件检查失败: {str(e)}"

def check_suid_sgid_files():
    """检查 SUID/SGID 文件"""
    try:
        result = subprocess.run(["find", "/", "-perm", "-4000", "-o", "-perm", "-2000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        files = result.stdout.decode().splitlines()
        return f"找到 {len(files)} 个 SUID/SGID 文件" if files else "未找到 SUID/SGID 文件"
    except Exception as e:
        return f"SUID/SGID 文件检查失败: {str(e)}"

def check_cron_jobs():
    """检查定时任务"""
    try:
        with open("/etc/crontab", "r") as f:
            jobs = f.readlines()
            return f"找到 {len(jobs)} 条定时任务" if jobs else "未找到定时任务"
    except Exception as e:
        return f"定时任务检查失败: {str(e)}"

def check_dns_resolvers():
    """检查 DNS 解析配置"""
    try:
        with open("/etc/resolv.conf", "r") as f:
            resolvers = f.read()
            return "DNS 解析配置正常" if "nameserver" in resolvers else "DNS 解析配置异常"
    except Exception as e:
        return f"DNS 解析配置检查失败: {str(e)}"

def check_selinux_status():
    """检查 SELinux 状态"""
    try:
        result = subprocess.run(["sestatus"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode().strip() if result.returncode == 0 else "SELinux 状态检查失败"
    except Exception as e:
        return f"SELinux 状态检查失败: {str(e)}"

def check_kernel_version():
    """检查内核版本"""
    try:
        result = subprocess.run(["uname", "-r"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return f"内核版本: {result.stdout.decode().strip()}"
    except Exception as e:
        return f"内核版本检查失败: {str(e)}"

def check_network_interfaces():
    """检查网络接口"""
    try:
        result = subprocess.run(["ip", "a"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "网络接口正常" if result.returncode == 0 else "网络接口异常"
    except Exception as e:
        return f"网络接口检查失败: {str(e)}"

def check_system_uptime():
    """检查系统运行时间"""
    try:
        result = subprocess.run(["uptime"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode().strip() if result.returncode == 0 else "系统运行时间检查失败"
    except Exception as e:
        return f"系统运行时间检查失败: {str(e)}"

def check_package_updates():
    """检查可更新的软件包"""
    try:
        result = subprocess.run(["apt", "list", "--upgradable"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        updates = result.stdout.decode().splitlines()
        return f"找到 {len(updates) - 1} 个可更新的软件包" if updates else "没有可更新的软件包"
    except Exception as e:
        return f"软件包更新检查失败: {str(e)}"

def check_swap_usage():
    """检查交换分区使用情况"""
    try:
        result = subprocess.run(["free", "-h"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode().strip() if result.returncode == 0 else "交换分区检查失败"
    except Exception as e:
        return f"交换分区检查失败: {str(e)}"

def check_system_logs():
    """检查系统日志"""
    try:
        with open("/var/log/syslog", "r") as f:
            logs = f.read()
            return "系统日志正常" if logs else "系统日志为空"
    except Exception as e:
        return f"系统日志检查失败: {str(e)}"

def get_config_checks():
    """返回所有配置检查结果"""
    return {
        "SSH 配置": check_ssh_config(),
        "用户账号": check_users(),
        "文件权限": check_file_permissions(),
        "777 权限文件": find_777_files(),
        "防火墙状态": check_firewall(),
        "sudo 命令日志": check_sudo_logs(),
        "SSH 登录失败记录": check_ssh_login_failures(),
        "Hosts 文件": check_hosts_file(),
        "SUID/SGID 文件": check_suid_sgid_files(),
        "定时任务": check_cron_jobs(),
        "DNS 解析配置": check_dns_resolvers(),
        "SELinux 状态": check_selinux_status(),
        "内核版本": check_kernel_version(),
        "网络接口": check_network_interfaces(),
        "系统运行时间": check_system_uptime(),
        "可更新的软件包": check_package_updates(),
        "交换分区使用情况": check_swap_usage(),
        "系统日志": check_system_logs(),
    }