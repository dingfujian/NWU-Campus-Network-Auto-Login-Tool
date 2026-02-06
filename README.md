# 西北大学校园网自动登录工具

## 项目简介

本项目是一个自动登录西北大学校园网的工具，使用 Python 和 Selenium 实现。通过图形用户界面（GUI），用户可以输入校园网的账号和密码，程序会自动保存这些信息，并在每天凌晨2点自动登录校园网，确保网络连接的持续性。

## 功能特点

- **自动登录**：每天凌晨2点自动登录校园网
- **图形界面**：提供简单易用的图形用户界面，用户可以输入和保存账号密码
- **记住密码**：首次输入账号密码后会自动保存，下次启动自动填充
- **日志记录**：程序运行日志会记录在 `campus_login.log` 文件中，方便查看登录状态
- **自动管理驱动**：程序会自动下载和管理 ChromeDriver，无需手动配置

## 使用方法

### 1. 环境依赖

- Windows 操作系统
- Google Chrome 浏览器

### 2. 下载与运行

1. 从 [Releases]下载最新的 `campus_login.exe` 文件
2. 双击运行 `campus_login.exe`
3. 首次运行时，程序会自动下载 ChromeDriver（需要网络连接）

### 3. 使用说明

1. 启动程序后，会弹出一个图形界面
2. 在界面中输入校园网的账号和密码
3. 点击"登录"按钮，程序会自动打开浏览器并登录校园网
4. 程序会将账号和密码保存到本地的 `config.json` 文件中，方便下次自动填充
5. 保持程序运行，它会在每日凌晨2点自动登录校园网

### 4. 日志查看

程序运行日志会记录在程序所在目录的 `campus_login.log` 文件中，包括：
- 程序启动信息
- 每次登录的详细过程
- 登录成功或失败的状态

## 开发与打包

### 1. 开发环境

- Python 3.9+
- 依赖库：
  - selenium
  - schedule
  - tkinter（Python 内置）

### 2. 安装依赖

```bash
pip install selenium schedule
```

### 3. 运行源码

```bash
python campus_login.py
```

### 4. 打包命令

使用以下命令将项目打包为单个可执行文件：

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole campus_login.py
```

打包完成后，生成的可执行文件位于 `dist/campus_login.exe`。

## 项目结构

```
src/
├── campus_login.py      # 主程序源码
├── campus_login_test.py # 测试脚本
build/
├── config.json          # 配置文件（运行后自动生成）
├── campus_login.log     # 日志文件（运行后自动生成）
└──campus_login.exe # 打包后的可执行文件
```

## 注意事项

1. **保持程序运行**：程序需要保持运行才能在凌晨2点自动登录，建议将程序设置为开机启动
2. **网络要求**：首次运行需要网络连接以下载 ChromeDriver
3. **Chrome 浏览器**：请确保电脑上已安装 Google Chrome 浏览器
4. **修改登录时间**：如需修改自动登录时间，可在源码中调整 `schedule.every().day.at("02:00")` 的时间

## 设置开机启动（可选）

1. 按 `Win + R` 打开运行对话框
2. 输入 `shell:startup` 并回车，打开启动文件夹
3. 将 `campus_login.exe` 的快捷方式复制到该文件夹中

## 贡献

欢迎提交 Issue 和 Pull Request 来改进本项目！

## 许可证

本项目基于 MIT 许可证开源。
