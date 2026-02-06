from campus_login import CampusLoginApp
import schedule
import tkinter as tk
from threading import Thread
import time

class CampusLoginTestApp(CampusLoginApp):
    def __init__(self, root):
        super().__init__(root)
        self.root.title("校园网自动登录 - 测试版（40秒间隔）")
        
        # 清除父类设置的定时任务
        schedule.clear()
        
        # 设置每40秒执行一次登录
        schedule.every(40).seconds.do(self.start_login)
        
        # 启动定时任务检查线程
        self.scheduler_thread = Thread(target=self.run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        self.log("测试模式：将每40秒自动登录一次")
    
    def run_scheduler(self):
        """后台运行定时任务检查"""
        while True:
            schedule.run_pending()
            time.sleep(1)  # 每秒检查一次

if __name__ == "__main__":
    root = tk.Tk()
    app = CampusLoginTestApp(root)
    root.mainloop()