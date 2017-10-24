## AndroidSdkSync4Mirror

Android SDK Sync for Mirror.site  
一个为镜像站所用的Android SDK 更新脚本  
(话说境外也用不上这玩意儿,就没英文说明了)

* * *

<del>首次测试可用 (Commits on May 7, 2016)(c69f8d2)</del>
已停止维护并弃用，可以尝试站长用dotNet实现的 https://github.com/honkerqifan/AndroidSDKPull
* * *

## 功能

*   支持从国内其他镜像站更新'/Android/repository/'下的数据
*   支持定时检测上游源是否有更新
*   支持日志管理
*   目前仅支持python2.7

* * *

## 如何使用

*   1. 下载 assm.conf、assm.py、loger.py、parser.py (satus.list为首次运行验证,请勿下载)
*   2. 手动配置assm.conf(凡地址结尾不要加"\")
*   3. ```python "/home/user/assm/assm.py"```

* * *

## TODO

*   1.新版本针对dl.google.com拉取数据
*   2.增加代理设置

* * *
## 关于我们

郑州大学开源镜像站维护小组  
Flicker: ffflicker#gmail.com  
dangge: i#dangge.moe  
