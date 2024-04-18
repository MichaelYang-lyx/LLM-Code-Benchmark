import sys
import psutil
import datetime
from prettytable import PrettyTable

# 检查指定PID的进程是否存在
def is_process_running(pid):
    return psutil.pid_exists(pid)

# 获取指定PID的进程对象
def get_process(pid):
    return psutil.Process(pid)

# 获取指定PID的进程状态
def get_process_status(pid):
    if is_process_running(pid):
        process = get_process(pid)
        process_time = get_process_uptime(pid)
        return {
            "pid": pid,
            "name": process.name(),
            "status": process.status(),
            "cpu_percent": process.cpu_percent(),
            "memory_percent": process.memory_percent(),
            "process_time": process_time
        }
    else:
        return {"pid": pid, "status": "不存在"}

def kill_process(pid):
    if is_process_running(pid):
        process = psutil.Process(pid)
        process.kill()
        print(f"进程PID为 {pid} 的进程已被终止.")
    else:
        print(f"进程PID为 {pid} 的进程不存在.")

def get_process_uptime(pid):
    # 获取进程创建的时间戳
    create_time = psutil.Process(pid).create_time()
    
    # 获取当前时间戳
    current_time = datetime.datetime.now().timestamp()
    
    # 计算进程运行时间
    uptime_seconds = current_time - create_time
    
    # 转换为更友好的格式
    uptime_str = str(datetime.timedelta(seconds=uptime_seconds))
    
    return uptime_str


# 监控指定PID的进程状态
def monitor_process(pid):
    while is_process_running(pid):
        process_status = get_process_status(pid)
        print(process_status)
        # 可以添加一些逻辑来处理进程状态，比如记录日志、发送警报等
        # 这里只是简单地打印出进程状态
        psutil.wait_procs([get_process(pid)], 3)  # 等待一段时间再继续检查进程状态



class Table:
    def __init__(self, tasks):
        # 初始化表格对象
        self.table = PrettyTable(["task", "status", "running_time"])
        self.tasks = {}

        for t in tasks:
            self.add_task(t, "/", "0")

        self.n = 3 + len(tasks) + 1
        

    def add_task(self, task, status, running_time):
        # 添加任务到表格
        self.table.add_row([task, status, running_time])
        self.tasks[task] = {"status": status, "running_time": running_time}

    def update_status(self, task, status):
        # 更新任务的状态
        if task in self.tasks:
            self.tasks[task]["status"] = status
            self._update_table()

    def update_running_time(self, task, running_time):
        # 更新任务的运行时间
        if task in self.tasks:
            self.tasks[task]["running_time"] = running_time
            self._update_table()

    def _update_table(self):
        # 更新表格内容
        self.table.clear_rows()
        for task, info in self.tasks.items():
            self.table.add_row([task, info["status"], info["running_time"]])

    def print_table(self, flush=False):
        print(self.table)

    def move_up_and_clear_lines(self):
        for _ in range(self.n):
            sys.stdout.write("\033[A")  # 向上移动一行
