import subprocess
import psutil

def check_cpu_usage():
    """检查 CPU 使用率"""
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        return f"CPU 使用率: {cpu_usage}%"
    except Exception as e:
        return f"CPU 使用率检查失败: {str(e)}"

def check_memory_usage():
    """检查内存使用率"""
    try:
        memory = psutil.virtual_memory()
        return f"内存使用率: {memory.percent}%"
    except Exception as e:
        return f"内存使用率检查失败: {str(e)}"

def check_disk_usage():
    """检查磁盘使用率"""
    try:
        disk = psutil.disk_usage('/')
        return f"磁盘使用率: {disk.percent}%"
    except Exception as e:
        return f"磁盘使用率检查失败: {str(e)}"

def check_swap_usage():
    """检查交换分区使用率"""
    try:
        swap = psutil.swap_memory()
        return f"交换分区使用率: {swap.percent}%"
    except Exception as e:
        return f"交换分区使用率检查失败: {str(e)}"

def check_network_usage():
    """检查网络使用情况"""
    try:
        net_io = psutil.net_io_counters()
        return f"网络使用情况: 发送 {net_io.bytes_sent} 字节, 接收 {net_io.bytes_recv} 字节"
    except Exception as e:
        return f"网络使用情况检查失败: {str(e)}"

def check_disk_io():
    """检查磁盘 I/O"""
    try:
        disk_io = psutil.disk_io_counters()
        return f"磁盘 I/O: 读取 {disk_io.read_bytes} 字节, 写入 {disk_io.write_bytes} 字节"
    except Exception as e:
        return f"磁盘 I/O 检查失败: {str(e)}"

def check_running_processes():
    """检查运行中的进程数量"""
    try:
        processes = len(psutil.pids())
        return f"运行中的进程数量: {processes}"
    except Exception as e:
        return f"运行中的进程数量检查失败: {str(e)}"

def check_system_uptime():
    try:
        # 运行 uptime 命令
        uptime = subprocess.run(["uptime"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if uptime.returncode != 0:
            return "系统运行时间检查失败"

        # 解析 uptime 输出
        uptime_output = uptime.stdout.decode().strip()
        parts = uptime_output.split()

        # 提取运行时间部分
        uptime_str = parts[2]  # 例如 "1:33" 或 "2 days, 3:45"

        # 格式化运行时间
        if "days" in uptime_str:
            # 如果运行时间包含天数
            days, time_part = uptime_str.split("days,")
            days = days.strip()
            hours, minutes = time_part.strip().split(":")
            return f"系统已运行 {days} 天 {hours} 小时 {minutes} 分钟"
        else:
            # 如果运行时间只有小时和分钟
            hours, minutes = uptime_str.split(":")
            return f"系统已运行 {hours} 小时 {minutes} 分钟"

    except Exception as e:
        return f"系统运行时间检查失败: {str(e)}"

def check_system_errors():
    """检查系统错误日志"""
    try:
        with open("/var/log/syslog", "r") as f:
            errors = [line for line in f if "error" in line.lower()]
            return f"发现 {len(errors)} 条系统错误日志" if errors else "未发现系统错误日志"
    except Exception as e:
        return f"系统错误日志检查失败: {str(e)}"

def get_performance_checks():
    """返回所有系统性能检测结果"""
    return {
        "CPU 使用率": check_cpu_usage(),
        "内存使用率": check_memory_usage(),
        "磁盘使用率": check_disk_usage(),
        "交换分区使用率": check_swap_usage(),
        "网络使用情况": check_network_usage(),
        "磁盘 I/O": check_disk_io(),
        "运行中的进程数量": check_running_processes(),
        "系统运行时间": check_system_uptime(),
        "系统错误日志": check_system_errors(),
    }