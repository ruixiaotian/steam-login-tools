"""
启动器,承载着程序的更新以及启动功能
"""
# 导入其他库
import cgitb
import hashlib
import json
import shutil
import subprocess
import sys
import winreg
import zipfile
from pathlib import Path
from queue import Queue
from threading import Thread

import requests
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import (
    QCloseEvent,
    QColor,
    QFont,
    QFontDatabase,
    QIcon,
    QMouseEvent,
    QPixmap,
)

# 导入QT5
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QWidget,
)
from loguru import logger


class Launcher(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setup_window()
        self.setup_font()
        self.setup_form()
        self.setup_layout()
        self.read_qss_file()
        self.show()
        self.download_steam_login_tools()

    def setup_window(self) -> None:
        """设定窗体各类参数
        :return: None
        """
        self.setFixedSize(300, 400)  # 设定窗体大小
        self.setWindowTitle("Steam上号器 - Qiao")  # 设定窗口名
        self.setWindowIcon(QIcon("./img/icon/icon.ico"))  # 设定窗体图标
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗体属性为透明
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)  # 隐藏框架,并且设置为主窗体

    def read_qss_file(self) -> None:
        """读取QSS文件"""
        with open("./QSS/launcher.qss", "r", encoding="utf-8") as file:
            self.setStyleSheet(file.read())

    def setup_font(self) -> None:
        """窗体字体获取"""
        self.font_name = QFontDatabase.applicationFontFamilies(
            QFontDatabase.addApplicationFont(r"font/W03.ttf")
        )[0]

    def setup_form(self) -> None:
        """窗体设定"""
        # 透明窗体
        self.base_widget = QWidget()  # 创建透明窗口
        self.base_widget.setObjectName("base_widget")  # 设置对象名称
        self.base_layout = QGridLayout()  # 创建透明窗口布局
        self.base_widget.setLayout(self.base_layout)  # 设置布局
        self.base_widget.setAttribute(Qt.WA_TranslucentBackground)  # 隐藏背景

        # 主窗体
        self.main_widget = QWidget()  # 创建主窗体
        self.main_widget.setObjectName("main_widget")  # 设置主窗体对象名称
        self.base_layout.addWidget(self.main_widget)  # 添加到布局

        self.setCentralWidget(self.base_widget)  # 设置窗口主部件

        # 添加阴影
        effect_shadow = QGraphicsDropShadowEffect(self)
        effect_shadow.setOffset(0, 1)  # 偏移
        effect_shadow.setBlurRadius(12)  # 阴影半径
        effect_shadow.setColor(QColor("#1DBEF5"))  # 阴影颜色
        self.main_widget.setGraphicsEffect(effect_shadow)  # 将设置套用到widget窗口中

    def setup_layout(self) -> None:
        """窗体布局设置"""
        # 创建布局以及设置布局参数
        layout = QGridLayout()
        layout.setContentsMargins(0, 100, 0, 50)

        # 添加控件到布局
        layout.addWidget(self.setup_top_logo(), 0, 0, 1, 1, Qt.AlignHCenter)
        layout.addWidget(self.setup_label(), 1, 0, 1, 1, Qt.AlignHCenter)
        layout.addWidget(self.setup_bar(), 2, 0, 1, 1, Qt.AlignHCenter)

        self.main_widget.setLayout(layout)

    def setup_top_logo(self) -> QLabel:
        """顶部logo设置"""
        # 创建logo控件
        self.logo_widget = QLabel()

        # 设置logo控件
        self.logo_widget.setObjectName("logo_widget")
        self.logo_widget.setFixedSize(128, 128)
        self.logo_widget.setPixmap(QPixmap("./img/icon/steam.svg"))
        self.logo_widget.setScaledContents(True)

        return self.logo_widget

    def setup_label(self) -> QLabel:
        """设置启动时的文字提示"""
        # 创建label控件
        self.label_widget = QLabel()

        # 设置label控件
        self.label_widget.setText("正在启动 Steam Login Tools")
        self.label_widget.setFont(QFont(self.font_name, 12))
        self.label_widget.setObjectName("label_widget")

        return self.label_widget

    def setup_bar(self) -> QProgressBar:
        """设置进度条控件"""
        # 创建进度条控件
        self.bar_widget = QProgressBar()

        # 设置进度条控件
        self.bar_widget.setObjectName("bar_widget")
        self.bar_widget.setFont(QFont(self.font_name, 7))
        self.bar_widget.setFixedSize(200, 15)
        self.bar_widget.setRange(0, 100)
        self.bar_widget.setValue(0)

        # 设置默认隐藏
        self.bar_widget.setVisible(False)

        return self.bar_widget

    def get_path(self) -> None:
        """初始化所有必要路径"""
        try:
            # 获取系统文档路径
            shell_path = (
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
            )
            winreg_key = winreg.HKEY_CURRENT_USER
            open_reg = winreg.OpenKeyEx(winreg_key, shell_path)
            self.document_path = Path(winreg.QueryValueEx(open_reg, "Personal")[0])
            self.bridge_club_path = Path(self.document_path) / "Bridge Club"
            self.tmp_path = Path(self.document_path) / "Bridge Club" / "tmp"
            self.steam_login_data_path = (
                Path(self.document_path) / "Bridge Club" / "steam_login_data"
            )
            self.steam_login_tools_path = (
                Path(self.document_path) / "Bridge Club" / "steam_login_tools"
            )

        except Exception as e:
            logger.error(f"路径获取失败: {e}")
            self.label_widget.setText("路径获取失败！")

    def download_steam_login_tools(self) -> None:
        """监测是否要下载Steam Login Tools"""
        self.get_path()  # 初始化所有路径

        if not self.steam_login_data_path.exists():
            # 如果不存在steam_login_data_path文件夹,则创建
            self.steam_login_data_path.mkdir(parents=True, exist_ok=True)

        if not self.steam_login_tools_path.exists():
            # 如果不存在steam_login_tools文件夹,则开始下载
            self.download_run()

        else:
            # 如果存在steam_login_tools文件夹,则检查是否有更新
            self.update_steam_login_data()

    def update_steam_login_data(self) -> None:
        """检测是否更新Steam Login Tools"""
        with open(
            self.bridge_club_path / "steam_login_tools_data.json", "r", encoding="utf-8"
        ) as f:
            json_data = json.load(f)
        self.label_widget.setText("检测更新...")

        res = requests.get(
            "https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/SteamLoginTool/steam_login_tools.json"
        ).json()

        if json_data["ver"] != res["ver"]:
            self.label_widget.setText("检测到有新版本,开始下载...")
            shutil.rmtree(self.steam_login_tools_path)
            self.download_run()
        else:
            self.start_steam_login_tools()

    def start_steam_login_tools(self) -> None:
        """启动steam登录工具"""
        self.label_widget.setText("正在启动 Steam Login Tools")
        self.setVisible(False)
        subprocess.run(
            str(self.steam_login_tools_path / "Steam Login Tools.exe"),
            cwd=str(self.steam_login_tools_path),
        )
        sys.exit(0)

    def download_run(self) -> None:
        """下载steam登录工具"""
        # 初始化下载对象
        self.download_thread = Download(
            self.bridge_club_path, self.tmp_path, self.label_widget
        )

        # 绑定信号
        self.download_thread.bar_int_signal.connect(
            lambda num: self.bar_widget.setValue(num)
        )
        self.download_thread.bar_switch_signal.connect(
            lambda switch: self.bar_widget.setVisible(switch)
        )
        self.download_thread.bar_range_signal.connect(
            lambda start, end: self.bar_widget.setRange(start, end)
        )
        self.download_thread.download_state.connect(
            lambda state: self.update_steam_login_data()
        )
        # 运行线程
        self.download_thread.start()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """重构鼠标按下事件函数,进行鼠标跟踪以及获取相对位置
        :param event:
        :return: None
        """
        if event.button() == Qt.LeftButton:
            # 如果按下按钮为左键
            self._mouse_flag = True  # 设置鼠标跟踪开关为True
            self.m_pos = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """重构鼠标移动事件函数,进行监控鼠标移动并且判断是否拖动窗口
        :param event:
        :return: None
        """
        if Qt.LeftButton and self._mouse_flag:
            # 如果是左键按下鼠标且跟踪打开
            self.move(event.globalPos() - self.m_pos)  # 更改窗口位置
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """重构鼠标松开事件函数,进行监控鼠标状态
        :param event:
        :return: None
        """
        self._mouse_flag = False  # 设置鼠标跟踪为关

    def closeEvent(self, event: QCloseEvent) -> None:
        """退出事件重构"""
        self.close()  # 关闭窗口


class Download(QThread):
    # 定义信号
    bar_int_signal = pyqtSignal(int)
    bar_switch_signal = pyqtSignal(bool)
    bar_range_signal = pyqtSignal(int, int)

    download_state = pyqtSignal(bool)

    def __init__(self, file_path: Path, tmp_path: Path, label: QLabel) -> None:
        """初始化
        file_path_edit: 文件路径 (不包含文件名
        tmp_path: 临时文件路径

        """
        super(Download, self).__init__()
        self.file_path: Path = file_path
        self.tmp_path: Path = tmp_path
        self.contain_name_path = Path(file_path) / "steam_login_tools.zip"
        self.label: QLabel = label
        self.thread_num: int = 16

    def run(self) -> None:
        """运行函数"""
        self.label.setText("正在下载必要文件")
        self.path_check()

    def path_check(self) -> None:
        """路径检查"""
        self.label.setText("文件路径检查...")

        if not self.file_path.exists():
            self.file_path.mkdir(parents=True, exist_ok=True)
            self.label.setText("文件路径不存在,已自动创建")

        if self.tmp_path.exists():
            shutil.rmtree(str(self.tmp_path))
            self.label.setText("临时文件路径存在,已自动删除")

        # 检查完成,拉起下一步
        self.get_download_url()

    def get_download_url(self) -> None:
        """读取json文件，获取下载地址"""
        self.label.setText("读取json文件...")
        # 读取json文件
        json_url = r"https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/SteamLoginTool/steam_login_tools.json"
        response = requests.get(json_url).json()

        # 解析json文件到变量
        self.ver: str = response["ver"]
        self.url: str = response["url"]
        self.hash: str = response["hash"]
        self.update_log: str = response["update_log"]
        self.label.setText("json文件解析完成")

        # 完成操作,拉起下一步
        self.get_download_size()

    def get_download_size(self) -> None:
        """解析下载文件大小"""
        self.label.setText("解析下载文件大小...")
        with requests.get(self.url, stream=True, allow_redirects=True) as response:
            self.file_size = int(response.headers["Content-Length"])
            self.redirects_url = response.url

        self.label.setText(f"文件大小: {self.file_size} 字节")

        # 解析完成,拉起下一步
        self.get_download_block_size()

    def get_download_block_size(self) -> None:
        """解析下载块大小"""
        self.label.setText("解析下载块大小...")

        # 创建字节队列
        self.bytes_queue = Queue(self.thread_num)

        self.bar_range_signal.emit(0, self.thread_num - 1)  # 设置进度条大小
        self.bar_switch_signal.emit(True)  # 设置进度条可见

        # 创建队列
        start_bytes = -1  # 开始字节为-1
        for i in range(self.thread_num):
            bytes_size = int(self.file_size / self.thread_num) * i  # 计算目前字节
            # 最后一个时 末尾字节为文件大小 避免落下一些字节未下载
            if i == self.thread_num - 1:
                bytes_size = self.file_size
            # 字节范围
            # start_bytes用来保存上一次的字节末尾
            bytes_length = "{}-{}".format(start_bytes + 1, bytes_size)

            self.bytes_queue.put([i, bytes_length])  # 加入队列 并赋予编号（i）
            start_bytes = bytes_size  # 将开始字节重新赋值

            # 更新进度条
            self.bar_int_signal.emit(i)

        self.label.setText("解析下载块大小完成")

        # 创建完成,拉起下一步
        self.create_thread()

    def create_thread(self) -> None:
        """创建下载线程"""
        self.label.setText("创建下载线程...")

        # 重置进度条
        self.bar_int_signal.emit(0)

        thread_list = []  # 线程队列
        for i in range(self.thread_num):
            self.label.setText(f"线程编号: {i} 创建成功")
            # 循环创建线程
            thread = DownloadThread(self.bytes_queue, self.redirects_url, self.tmp_path)
            thread.start()
            thread_list.append(thread)

            self.bar_int_signal.emit(i)

        # 重置进度条
        self.bar_int_signal.emit(0)

        self.label.setText("正在下载...")

        for i, thread in enumerate(thread_list):
            # 等待执行结束
            thread.join()
            self.bar_int_signal.emit(i + 1)

        # 下载完成,拉起下一步
        self.merge_files()

    def merge_files(self) -> None:
        """合并文件"""
        self.label.setText("合并文件...")
        # 如果文件存在 先移除
        if self.contain_name_path.exists():
            self.label.setText("检测到存在相同文件名文件,已自动移除")
            self.contain_name_path.unlink()

        with open(self.contain_name_path, "ab") as f:  # 以追加模式打开文件
            for i in range(self.thread_num):
                # 根据id查找文件
                with open("{}/{}.tmp".format(self.tmp_path, i), "rb") as bytes_f:
                    # 写入文件
                    f.write(bytes_f.read())

        self.label.setText("合并文件完成")

        shutil.rmtree(str(self.tmp_path))

        # 合并完成,拉起下一步
        self.hash_check()

    def hash_check(self) -> None:
        """验证哈希"""
        self.label.setText("验证SHA256")

        # 创建一个hash对象，使用SHA-256哈希算法
        hash_256 = hashlib.sha256()
        # 以二进制读取文件
        with open(self.contain_name_path, "rb") as file:
            # 循环读取文件内容
            chunk = 0
            while chunk != b"":
                # 每次读取65536个字节（64KB）
                chunk = file.read(65536)
                # 更新hash对象
                hash_256.update(chunk)

        # 哈希计算完成,校验是否一致
        if self.hash.lower() != hash_256.hexdigest().lower():
            self.label.setText("哈希校验失败")
            # 删除文件重新下载
            self.contain_name_path.unlink()
            self.get_download_url()
            return
        else:
            self.label.setText("哈希校验成功")

        # 校验完成,拉起下一步
        self.unzip_file()

    def unzip_file(self) -> None:
        """解压文件"""
        self.label.setText("解压文件...")
        # 解压文件
        with zipfile.ZipFile(self.contain_name_path, "r") as zip_f:
            zip_f.extractall(self.file_path)
        self.contain_name_path.unlink()
        self.label.setText("解压文件完成")

        # 解压完成,拉起下一步
        self.write_data()

    def write_data(self) -> None:
        """写入版本信息"""
        with open(
            self.file_path / "steam_login_tools_data.json", "w", encoding="utf-8"
        ) as file:
            json_data = {
                "ver": self.ver,
                "hash": self.hash,
                "update_log": self.update_log,
            }
            json.dump(json_data, file, ensure_ascii=False, indent=4)

        # 完成所有操作,返回信号执行下一步函数

        self.download_state.emit(True)


class DownloadThread(Thread):
    """下载线程"""

    def __init__(self, bytes_queue: Queue, url: str, tmp_path: Path) -> None:
        super().__init__(daemon=True)
        self.bytes_queue: Queue = bytes_queue
        self.url: str = url
        self.tmp_path: Path = tmp_path

    def path_check(self) -> None:
        """路径检查"""
        if not self.tmp_path.exists():
            self.tmp_path.mkdir(parents=True, exist_ok=True)

    def run(self) -> None:
        """下载线程"""
        self.path_check()  # 检查路径
        while not self.bytes_queue.empty():  # 如果字节队列不为空
            bytes_range = self.bytes_queue.get()  # 读取范围信息
            headers = {
                "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
                "Range": "bytes={}".format(bytes_range[1]),  # Range 设置
            }
            response = requests.get(self.url, headers=headers)  # 请求发送
            with open("{}/{}.tmp".format(self.tmp_path, bytes_range[0]), "wb") as f:
                # 根据id生成临时文件
                f.write(response.content)


def rush_backtracking() -> None:
    """
    奔溃回溯,如果程序引发了崩溃,将会在桌面生成崩溃日志
    :return:
    """
    log_dir = Path.home() / "Desktop"
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
    cgitb.enable(display=0, format="log", logdir=str(log_dir), context=10)


if __name__ == "__main__":
    rush_backtracking()
    app = QApplication(sys.argv)
    window = Launcher()
    sys.exit(app.exec_())
