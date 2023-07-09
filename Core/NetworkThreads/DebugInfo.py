#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :DebugInfo.py
# @Time :2023-7-7 上午 11:28
# @Author :Qiao
"""
传入的参数应该是字典类型
{
    level: str
    msg: str
    exit: bool
}
一共有七个消息等级
    TRACE
    DEBUG
    INFO
    SUCCESS
    WARNING
    ERROR
    CRITICAL
"""
import subprocess
import socket
import json


class DebugInfo:

    def __init__(self) -> None:
        pass

    def runDebugInfoTools(self):
        """启动调试工具"""
        pass

    @staticmethod
    def send_msg(msg: dict) -> None:
        """发送消息到输出端"""
        # 创建一个 IPv4 和 UDP 协议的套接字
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        # 消息处理
        msg = json.dumps(msg)
        # 发送消息
        server.sendto(msg.encode('utf-8'), ("127.0.0.1", 5000))


if __name__ == '__main__':
    DebugInfo.send_msg(
        {
            'level': 'CRITICAL',
            'msg': '111',
            'exit': True
        }
    )
