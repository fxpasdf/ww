import subprocess
import os

def check_unpatched_software():
    """检查未修补的软件包"""
    try:
        result = subprocess.run(["apt-get", "update"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return "未发现未修补的软件包"
        else:
            return "发现未修补的软件包"
    except Exception as e:
        return f"未修补软件包检查失败: {str(e)}"

def check_open_ports():
    """检查开放端口"""
    try:
        result = subprocess.run(["netstat", "-tuln"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        open_ports = result.stdout.decode().splitlines()
        return f"发现 {len(open_ports) - 2} 个开放端口" if open_ports else "未发现开放端口"
    except Exception as e:
        return f"开放端口检查失败: {str(e)}"

def check_root_login():
    """检查是否允许 root 登录"""
    try:
        result = subprocess.run(["grep", "PermitRootLogin", "/etc/ssh/sshd_config"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if "no" in result.stdout.decode():
            return "root 登录已禁用"
        else:
            return "root 登录未禁用"
    except Exception as e:
        return f"root 登录检查失败: {str(e)}"

def check_password_policy():
    """检查密码策略"""
    try:
        result = subprocess.run(["grep", "PASS_MAX_DAYS", "/etc/login.defs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        policy = result.stdout.decode().strip()
        return f"密码策略: {policy}" if policy else "未找到密码策略"
    except Exception as e:
        return f"密码策略检查失败: {str(e)}"

def check_suid_sgid_files():
    """检查 SUID/SGID 文件"""
    try:
        result = subprocess.run(["find", "/", "-perm", "-4000", "-o", "-perm", "-2000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        files = result.stdout.decode().splitlines()
        return f"发现 {len(files)} 个 SUID/SGID 文件" if files else "未发现 SUID/SGID 文件"
    except Exception as e:
        return f"SUID/SGID 文件检查失败: {str(e)}"

def check_world_writable_files():
    """检查全局可写文件"""
    try:
        result = subprocess.run(["find", "/", "-perm", "-o+w"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        files = result.stdout.decode().splitlines()
        return f"发现 {len(files)} 个全局可写文件" if files else "未发现全局可写文件"
    except Exception as e:
        return f"全局可写文件检查失败: {str(e)}"

def check_ssh_protocol():
    """检查 SSH 协议版本"""
    try:
        result = subprocess.run(["grep", "Protocol", "/etc/ssh/sshd_config"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        protocol = result.stdout.decode().strip()
        return f"SSH 协议版本: {protocol}" if protocol else "未找到 SSH 协议配置"
    except Exception as e:
        return f"SSH 协议检查失败: {str(e)}"

def check_sudo_permissions():
    """检查 sudo 权限"""
    try:
        result = subprocess.run(["grep", "-i", "NOPASSWD", "/etc/sudoers"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        permissions = result.stdout.decode().splitlines()
        return f"发现 {len(permissions)} 个无需密码的 sudo 权限" if permissions else "未发现无需密码的 sudo 权限"
    except Exception as e:
        return f"sudo 权限检查失败: {str(e)}"

def check_umask():
    """检查 umask 配置"""
    try:
        result = subprocess.run(["umask"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        umask = result.stdout.decode().strip()
        return f"umask 配置: {umask}" if umask else "未找到 umask 配置"
    except Exception as e:
        return f"umask 检查失败: {str(e)}"

def check_selinux_status():
    """检查 SELinux 状态"""
    try:
        result = subprocess.run(["sestatus"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status = result.stdout.decode().strip()
        return f"SELinux 状态: {status}" if status else "SELinux 未启用"
    except Exception as e:
        return f"SELinux 状态检查失败: {str(e)}"

def check_firewall_status():
    """检查防火墙状态"""
    try:
        result = subprocess.run(["ufw", "status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status = result.stdout.decode().strip()
        return f"防火墙状态: {status}" if status else "防火墙未启用"
    except Exception as e:
        return f"防火墙状态检查失败: {str(e)}"

def check_cron_permissions():
    """检查定时任务权限"""
    try:
        result = subprocess.run(["ls", "-l", "/etc/cron.d"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        permissions = result.stdout.decode().splitlines()
        return f"定时任务权限: {permissions}" if permissions else "未找到定时任务"
    except Exception as e:
        return f"定时任务权限检查失败: {str(e)}"

def check_kernel_modules():
    """检查加载的内核模块"""
    try:
        result = subprocess.run(["lsmod"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        modules = result.stdout.decode().splitlines()
        return f"加载的内核模块: {len(modules) - 1} 个" if modules else "未加载内核模块"
    except Exception as e:
        return f"内核模块检查失败: {str(e)}"

def check_system_logs():
    """检查系统日志"""
    try:
        with open("/var/log/syslog", "r") as f:
            logs = f.read()
            return "系统日志正常" if logs else "系统日志为空"
    except Exception as e:
        return f"系统日志检查失败: {str(e)}"

def check_ssh_failed_logins():
    """检查 SSH 登录失败记录"""
    try:
        result = subprocess.run(["grep", "Failed password", "/var/log/auth.log"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        failures = result.stdout.decode().splitlines()
        return f"发现 {len(failures)} 条 SSH 登录失败记录" if failures else "未发现 SSH 登录失败记录"
    except Exception as e:
        return f"SSH 登录失败记录检查失败: {str(e)}"

def check_world_readable_files():
    """检查全局可读文件"""
    try:
        result = subprocess.run(["find", "/", "-perm", "-o+r"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        files = result.stdout.decode().splitlines()
        return f"发现 {len(files)} 个全局可读文件" if files else "未发现全局可读文件"
    except Exception as e:
        return f"全局可读文件检查失败: {str(e)}"

def check_system_updates():
    """检查系统更新"""
    try:
        result = subprocess.run(["apt", "list", "--upgradable"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        updates = result.stdout.decode().splitlines()
        return f"发现 {len(updates) - 1} 个可更新的软件包" if updates else "没有可更新的软件包"
    except Exception as e:
        return f"系统更新检查失败: {str(e)}"

def get_vuln_checks():
    """返回所有安全漏洞检测结果"""
    return {
        "未修补的软件包": check_unpatched_software(),
        "开放端口": check_open_ports(),
        "root 登录": check_root_login(),
        "密码策略": check_password_policy(),
        "SUID/SGID 文件": check_suid_sgid_files(),
        "全局可写文件": check_world_writable_files(),
        "SSH 协议版本": check_ssh_protocol(),
        "sudo 权限": check_sudo_permissions(),
        "umask 配置": check_umask(),
        "SELinux 状态": check_selinux_status(),
        "防火墙状态": check_firewall_status(),
        "定时任务权限": check_cron_permissions(),
        "内核模块": check_kernel_modules(),
        "系统日志": check_system_logs(),
        "SSH 登录失败记录": check_ssh_failed_logins(),
        "全局可读文件": check_world_readable_files(),
        "系统更新": check_system_updates(),
    }