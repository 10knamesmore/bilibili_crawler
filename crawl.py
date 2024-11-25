# 爬取B站的视频 Bilibili

import json
import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor
import os.path as op

import requests

FILE_PATH = op.dirname(op.abspath(__file__))
DOWNLOAD_DIR = op.join(FILE_PATH,"downloads")

# 请求头
header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com/", # 保证为b站内部跳转
}

logging.basicConfig(
    filename=op.join(FILE_PATH,"crawler.log"),
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)


def crawl(url, index):
    try:
        resp = requests.get(url=url, headers=header)
        resp.raise_for_status()

        # 这个baseUrl就是视频的地址

        obj = re.compile(r'window.__playinfo__=(.*?)</script>', re.S)
        html_data = obj.findall(resp.text)[0]  # 从列表转换为字符串
        # 转化为字典的形式
        json_data = json.loads(html_data)

        # video 和 audio分别是视频和音频 因此爬取下来以后，还需要将两个合并

        videos = json_data['data']['dash']['video']  # 这里得到的是一个列表
        video_url = videos[0]['baseUrl']  # 视频地址

        audios = json_data['data']['dash']['audio']
        audio_url = audios[0]['baseUrl']  # 音频地址

        if not op.exists(DOWNLOAD_DIR):
            os.mkdir(DOWNLOAD_DIR)
        # 下载视频和音频
        video_path = op.join(DOWNLOAD_DIR, f"{index}.mp4")
        video_file = open(file=video_path, mode='wb')
        video_file.write(requests.get(url=video_url, headers=header).content)

        audio_path = op.join(DOWNLOAD_DIR, f"{index}.mp3")
        audio_file = open(file=audio_path, mode='wb')
        audio_file.write(requests.get(url=audio_url,headers=header).content)

        # 合并视频和音频,linux终端命令
        # 需要下载ffmpeg终端工具
        combined_file_path = op.join(DOWNLOAD_DIR, f"_{index}.mp4")
        command = rf'ffmpeg -i {video_path} -i {audio_path} -acodec copy -vcodec copy {combined_file_path}'
        os.system(command=command)
        os.remove(audio_path)
        os.remove(video_path)

        os.rename(combined_file_path, video_path)

        logging.info(f"视频 {index} 下载完成")

        # 切割视频
        # index_dir = op.join(DOWNLOAD_DIR, f"{index}")
        # os.mkdir(index_dir)
        # segment_time = 20
        # command = rf'ffmpeg -i {combined_file_path} -c copy -map 0 -segment_time {segment_time} -f segment -reset_timestamps 1 {op.join(index_dir, "%03d.mp4")}'
        # os.system(command=command)

        return 0

    except IndexError:
        logging.error(f"视频 {url} 不存在")

    return 1


def main():
    # 读取视频链接
    with open(op.join(FILE_PATH,"urls.txt"), 'r') as file:
        urls = [line.strip() for line in file]

    # 使用多线程下载
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(crawl, url, index) for index, url in enumerate(urls)]

        # 等待线程完成
        for future in futures:
            future.result()  # 如果有异常，将在这里抛出


if __name__ == '__main__':
    main()
