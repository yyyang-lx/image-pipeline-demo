# app/config.py
# 项目核心配置文件：统一管理路径、服务参数、环境变量等配置项
# 遵循 "环境变量优先，默认值兜底" 的配置原则，便于不同环境（开发/测试/生产）部署

# 导入Python内置的路径处理库，用于安全、便捷地处理文件路径（跨平台兼容）
from pathlib import Path
# 导入Python内置的操作系统交互库，用于读取环境变量、系统路径等
import os
# 导入第三方库python-dotenv的加载函数，用于读取.env文件中的环境变量
from dotenv import load_dotenv

# 加载项目根目录下的.env文件（如果存在），将其中的配置注入到系统环境变量中
# 若不存在.env文件，此操作无副作用，代码会使用默认值
load_dotenv()

# 定义项目根目录路径
# __file__: 当前config.py文件的路径
# .resolve(): 转换为绝对路径，避免相对路径歧义
# .parent.parent: 连续取两层上级目录（app/config.py -> app -> 项目根目录）
APP_DIR = Path(__file__).resolve().parent.parent  # 项目根目录：image-pipeline-demo/

# 定义数据存储根目录路径
# os.getenv("DATA_DIR", 默认值): 优先读取环境变量DATA_DIR，不存在则用默认值
# APP_DIR / "data": 拼接项目根目录和data文件夹（Path对象的便捷拼接方式）
# str(): 转换为字符串，兼容os.getenv的参数要求
# .resolve(): 最终转换为绝对路径，确保路径唯一性
DATA_DIR = Path(os.getenv("DATA_DIR", str(APP_DIR / "data"))).resolve()  # 数据存储根目录

# 定义文件存储子目录路径（基于DATA_DIR）
# 专门用于存放业务相关的文件（如上传的文件、处理后的文件等）
FILES_DIR = DATA_DIR / "files"  # 文件存储具体目录

# 定义服务监听的主机地址
# 优先读取环境变量HOST，默认值127.0.0.1（仅本机可访问），部署时可改为0.0.0.0（全网可访问）
HOST = os.getenv("HOST", "127.0.0.1")  # 服务监听地址

# 定义服务监听的端口号
# 优先读取环境变量PORT，默认值9002
# int(): 将环境变量读取的字符串转换为整数（端口号必须是整数类型）
PORT = int(os.getenv("PORT", "9002"))  # 服务监听端口

# 定义服务版本号
# 优先读取环境变量SERVICE_VERSION，默认值0.1
# 用于标识服务版本，便于运维、接口文档管理
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "0.1")  # 服务版本号