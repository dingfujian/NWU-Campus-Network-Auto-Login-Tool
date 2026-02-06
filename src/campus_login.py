"""
校园网自动登录脚本
登录地址: http://10.0.1.165/a70.htm
"""

import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import logging
import os
import sys
import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import json

# 获取程序运行目录（支持打包后的exe）
if getattr(sys, 'frozen', False):
    # 打包后的exe运行
    APP_DIR = os.path.dirname(sys.executable)
else:
    # 脚本直接运行
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

# 配置日志
log_file = os.path.join(APP_DIR, 'campus_login.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logging.info("程序启动成功，日志已初始化。")
logging.info("程序将在每日凌晨2点自动登录。")

# 登录配置
LOGIN_URL = "http://10.0.1.165/a70.htm"
# 以下为默认值，实际使用时通过界面输入
USERNAME = ""
PASSWORD = ""

# 登录间隔（天）
LOGIN_INTERVAL_DAYS = 2

CONFIG_FILE = os.path.join(APP_DIR, 'config.json')

def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"username": "", "password": ""}

def save_config(username, password):
    """保存配置到文件"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump({"username": username, "password": password}, f)

class CampusLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("校园网自动登录")
        self.root.geometry("500x400")

        # 加载配置
        self.config = load_config()

        # 用户名输入框
        tk.Label(root, text="用户名:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = tk.Entry(root, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.username_entry.insert(0, self.config.get("username", ""))

        # 密码输入框
        tk.Label(root, text="密码:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(root, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        self.password_entry.insert(0, self.config.get("password", ""))

        # 登录按钮
        self.login_button = tk.Button(root, text="登录", command=self.start_login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        # 日志显示区域
        self.log_text = scrolledtext.ScrolledText(root, width=60, height=15, state="disabled")
        self.log_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # 设置定时任务
        self.setup_scheduler()

    def log(self, message):
        """在日志区域显示信息"""
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")

    def setup_scheduler(self):
        """设置定时任务"""
        # 清除之前的定时任务
        schedule.clear()
        
        # 设置每天凌晨2点执行一次登录
        schedule.every().day.at("02:00").do(self.start_login)
        
        # 启动定时任务检查线程
        self.scheduler_thread = Thread(target=self.run_scheduler, daemon=True)
        self.scheduler_thread.start()

    def run_scheduler(self):
        """后台运行定时任务检查"""
        while True:
            schedule.run_pending()
            time.sleep(1)  # 每秒检查一次

    def start_login(self):
        """启动登录线程"""
        self.log("开始登录...")
        self.login_button.config(state="disabled")
        username = self.username_entry.get()
        password = self.password_entry.get()
        save_config(username, password)  # 保存用户输入的账号和密码
        Thread(target=self.auto_login, args=(username, password)).start()

    def auto_login(self, username, password):
        """自动登录函数"""
        driver = None
        try:
            self.log("启动浏览器...")
            
            # 配置Chrome选项
            chrome_options = Options()
            # 注释掉无头模式以显示浏览器窗口
            # chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            # 初始化浏览器
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)
            
            # 访问登录页面
            self.log(f"访问登录页面: {LOGIN_URL}")
            driver.get(LOGIN_URL)
            
            # 使用显式等待,确保页面完全加载
            wait = WebDriverWait(driver, 10)
            
            # 等待页面加载
            time.sleep(3)
            
            self.log("页面加载完成,开始查找输入框...")
            
            # 查找用户名输入框
            username_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder*='账号']")))
            self.log("找到用户名输入框")
            
            # 输入用户名
            username_input.click()
            time.sleep(0.2)
            username_input.send_keys(Keys.CONTROL + "a")
            username_input.send_keys(Keys.DELETE)
            for char in username:
                username_input.send_keys(char)
                time.sleep(0.03)
            self.log(f"✓ 已填充用户名")
            
            # 查找密码输入框
            password_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder*='密码']")))
            self.log("找到密码输入框")
            
            # 输入密码
            password_input.click()
            time.sleep(0.2)
            password_input.send_keys(Keys.CONTROL + "a")
            password_input.send_keys(Keys.DELETE)
            for char in password:
                password_input.send_keys(char)
                time.sleep(0.03)
            self.log("✓ 已填充密码")
            
            time.sleep(0.5)
            
            # 点击登录按钮
            login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
            login_button.click()
            self.log("✓ 已点击登录按钮")
            
            # 等待登录完成
            time.sleep(3)
            
            # 检查是否有alert弹窗
            try:
                alert = driver.switch_to.alert
                alert_text = alert.text
                self.log(f"检测到弹窗: {alert_text}")
                alert.accept()
                self.log(f"登录失败: {alert_text}")
            except:
                # 没有弹窗，检查URL
                current_url = driver.current_url
                self.log(f"登录后页面URL: {current_url}")
                if current_url != LOGIN_URL:
                    self.log("✓ 登录成功！")
                else:
                    self.log("登录完成，请检查网络连接状态")
            
            # 关闭浏览器
            driver.quit()
            self.log("浏览器已关闭")
            
        except Exception as e:
            self.log(f"登录过程出现错误: {str(e)}")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
        finally:
            self.login_button.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = CampusLoginApp(root)
    root.mainloop()
