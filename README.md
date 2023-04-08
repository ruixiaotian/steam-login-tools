<div align="center">

# Steam Login Tools

[![](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![](https://img.shields.io/badge/PyQt-5.15-orange)](https://www.python.org/)
[![](https://img.shields.io/badge/license-GPL--3.0-green)](https://github.com/ruixiaotian/steam-login-tools/blob/main/LICENSE)

一个简单的Steam上号工具，支持跳过邮箱验证（需要正确的SSFN）

</div>

### 目前支持的功能

 + Steam账号管理
 + 快速切换账号登录
 + 支持绕过邮箱验证（此功能只能用大屏幕模式启动Steam）
 + 支持快速离线登录

### TODO
+ 网络加速功能（正常访问创意工坊等
+ 功能设置
+ 暗黑模式

### 如何自己编译
默认认为你已经将本项目git到了你的打包环境并且创建好了虚拟环境
```
# Python 3.10
pip install -r requirements.txt
pip install nuitka

# 带控制台输出版本
nuitka --mingw64  --enable-plugin=pyqt5 --standalone --show-progress --show-memory --windows-icon-from-ico=./img/icon/icon.ico --windows-company-name=Qiao --windows-product-name=SteamLogin --windows-file-version=3.0.0 --output-dir=out .\main.py

# 不带控制台版本
nuitka --mingw64 --windows-disable-console --enable-plugin=pyqt5 --standalone --show-progress --show-memory --windows-icon-from-ico=./img/icon/icon.ico --windows-company-name=Qiao --windows-product-name=SteamLogin --windows-file-version=3.0.0 --output-dir=out .\main.py
```

### LICENSE
本项目基于 [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.zh-cn.htmll) 许可协议，详细信息请查看 LICENSE 文件。

GPL-3.0 许可证要求任何以此代码为基础的派生作品，必须使用同样的协议发布和授权。这保证了代码的自由和保护了贡献者的权利。如果您想将本项目的代码用于商业用途，请确保您的产品也符合 GPL-3.0 许可证的要求。
