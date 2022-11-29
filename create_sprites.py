# based on https://stackoverflow.com/a/71340017

import ffmpeg
import logging
from pathlib import Path
import os
from PIL import Image
from datetime import timedelta
import math

logger = logging.getLogger(__name__)

TMP_DIR = "/tmp/stream-demo"


class ScreenshotExtractor:
    def __init__(self):
        self.screenshot_folder = f"{TMP_DIR}/ss"
        self.gap = 10
        self.size = "177x100"
        self.col = 5
        self.ss_width = 177
        self.ss_height = 100

    def create_sprite_sheet(self, name):
        path, dirs, files = next(os.walk(self.screenshot_folder))
        file_count = len(files)
        img_width = self.ss_width * self.col
        img_height = self.ss_height * math.ceil(file_count / self.col)

        file_name = f"{name}.jpg"
        out_image = Image.new("RGB", (img_width, img_height))
        webvtt = "WEBVTT\n\n"
        for count, img_file in enumerate(files):
            img = Image.open(f"{self.screenshot_folder}/{img_file}")
            st_time = timedelta(seconds=count * self.gap)
            end_time = timedelta(seconds=(count + 1) * self.gap)

            # Adding img to out_file
            x_mod = int(count / self.col)
            x = 0 + (count - (self.col * x_mod)) * self.ss_width
            y = 0 + x_mod * self.ss_height
            out_image.paste(img, (x, y))

            sprite = f"{file_name}#xywh={x},{y},{self.ss_width},{self.ss_height}"
            webvtt += f"{count + 1}\n0{str(st_time)}.000 --> 0{str(end_time)}.000\n{sprite}\n\n"

        out_image.save("out.jpg", quality=90)
        with open("live-sprites.vtt", "w") as f:
            f.write(webvtt)
        return True

    def extract_screenshots(self, file_uri, name):
        try:
            Path(self.screenshot_folder).mkdir(parents=True, exist_ok=True)
            vod = ffmpeg.input(file_uri)
            vod.output(
                f"{self.screenshot_folder}/{name}_%04d.png", r=1 / self.gap, s=self.size
            ).run()
            return True
        except Exception as e:
            logger.warning(e)
            return False

    def run(self, file_uri, name):
        self.extract_screenshots(file_uri, name)
        self.create_sprite_sheet(name)


if __name__ == "__main__":
    ss = ScreenshotExtractor()
    ss.run(
        "https://ffmpeg-stream-demo.s3-eu-west-1.amazonaws.com/stream.m3u8", "roh-demo"
    )
