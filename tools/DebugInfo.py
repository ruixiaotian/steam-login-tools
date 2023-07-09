#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :DebugInfo.py
# @Time :2023-7-7 上午 10:33
# @Author :Qiao
"""
启动参数
    --port -p
        int: 程序在指定的端口运行
"""
import argparse
import json
import socket
import sys
from typing import Dict

from loguru import logger


class DebugInfo:
    def __init__(self):
        self.args = None
        self.arg_setup()
        self.create_server()

    def arg_setup(self) -> None:
        """程序启动参数设置"""
        # 创建ArgumentParser对象
        parser = argparse.ArgumentParser(description="调试程序")
        # 添加参数
        parser.add_argument("--port", "-p", type=int, help="端口号")
        # 解析参数
        self.args = parser.parse_args(self.args)
        if not self.args.port:
            logger.error("必须提供--port参数")
            sys.exit(1)  # 如果没有提供足够的参数，则退出程序
        logger.info("调试启动成功!")

    def create_server(self):
        # 创建一个 IPv4 和 UDP 协议的套接字
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

        # 使用 127.0.0.1 地址进行监听
        server.bind(("127.0.0.1", 5000))

        while True:
            data, address = server.recvfrom(4096)
            # 消息处理
            data = data.decode("utf-8")
            data = json.loads(data)
            # 如果客户端发送结束，就结束服务
            (server.close(), sys.exit(0)) if data["exit"] else None
            # 输出信息
            self.msg_opt(data)

    @staticmethod
    def msg_opt(msg: dict):
        """消息判断并输出"""
        match msg["level"].upper():
            case "TRACE":
                logger.trace(msg["msg"])
            case "DEBUG":
                logger.debug(msg["msg"])
            case "INFO":
                logger.info(msg["msg"])
            case "SUCCESS":
                logger.success(msg["msg"])
            case "WARNING":
                logger.warning(msg["msg"])
            case "ERROR":
                logger.error(msg["msg"])
            case "CRITICAL":
                logger.critical(msg["msg"])


if __name__ == "__main__":
    debug_info = DebugInfo()
