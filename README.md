# bitcoinDataViewer
collect bitcoin price from several website and view.

使用说明：
设置chrome:	
    关闭chrome,运行一次 allow-chrome-cross-region-access.bat 文件自动设置chrome浏览器。如果chrome没有安装在默认路径，打开命令提示符窗口手动运行   安装路径\chrome.exe" --allow-file-access-from-files。
日常使用：
1.确保安装了Python 3.x,运行 src/getdata.py,脚本会在后台获取网站数据;
2.用chrome 打开index.html 就OK了！页面会定时更新（目前设置的更新频率为2s/次,数据的具体更新频率可能大于2s，受后台获取速度的影响）。


