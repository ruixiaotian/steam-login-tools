<div align="center">

# Steam Login Tools

[![](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![](https://img.shields.io/badge/PyQt-5.15-orange)](https://www.python.org/)
[![](https://img.shields.io/badge/license-GPL--3.0-green)](https://github.com/ruixiaotian/steam-login-tools/blob/main/LICENSE)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

一个简单的Steam上号工具，支持跳过邮箱验证（需要正确的SSFN）

</div>

### 注意
由于Steam更新频繁，对SSFN跳过邮箱验证各种围堵持续👊🐔 ，在未来旧版接口被封锁后再无黑号可登，我已无力继续维护此项目，即日起停止对Steam Login Tools的维护，感谢各位的陪伴与支持

### 目前支持的功能

 + Steam账号管理
 + 批量导入账号
 + 快速切换账号登录
 + 支持绕过邮箱验证（此功能只能用大屏幕模式启动Steam）

### TODO
+ 离线登录
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
本项目基于 [GPL-3.0](https://www.gnu.org/licenses/quick-guide-gplv3.html) 许可协议，详细信息请查看 LICENSE 文件。

GPL-3.0 许可证要求任何以此代码为基础的派生作品，必须使用同样的协议发布和授权。这保证了代码的自由和保护了贡献者的权利。如果您想将本项目的代码用于商业用途，请确保您的产品也符合 GPL-3.0 许可证的要求。
