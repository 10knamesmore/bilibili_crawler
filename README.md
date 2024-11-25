# 一个简单的bilibili爬视频脚本

## 功能特性

- 多线程下载
- 多系统支持
- 直接获取mp4文件
- 将视频分段(可配置,可用于视频数据集的制作)

## 用法

下载到任何地方

需要下载requests库

```shell
pip install requests
```

需要下载ffmpeg并添加到环境变量中

```shell
sudo apt install ffmpeg
```

直接运行即可

```bash
python crawl.py
```

## TODO:

* [ ] 增加cookie认证以下载更高清视频
* [ ] 点赞
* [ ] 收藏
* [ ] 硬币
* [ ] 弹幕
* [ ] 评论
* [ ] up
* [ ] up关注
