# Video-Thumbnails-Create
Create Video Thumbnails. 创建视频缩略图，网格状，可自定义列数及分辨率

用pycharm、vscode或其他IDLE软件打开运行，输入需要生成缩略图的路径，自动遍历目录下所有视频文件并生成缩略图。
该脚本所需核心模块有：PIL、ffmpeg，运行前请确保已安装。

以下为默认设置
一行4张图片，宽度为3840px，高度随视频时间而自动增加。
缩略图间隔：小于2分钟2秒一张，2-10分钟5秒一张，10-30分钟15秒一张，30-60分钟30秒一张，大于60分钟1分钟一张。

设置如需要调整可自定定位到所在位置。

本人并不精通python，该脚本是闲暇之余写的，有不完善或不合理的地方可告知，各位大佬请轻虐🙌🙌

如遇到报错可能为视频不完整所致，具体视报错情况自行调试。

效果图如下：
![image](https://github.com/Amii-Henin/Video-Thumbnails-Creater/blob/main/FormD%20T1%20-%20The%20Ultimate%20Sub-10L%20Case!_thumb.jpg)
