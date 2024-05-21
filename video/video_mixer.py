# Import everything needed to edit video clips
# pip install moviepy
# pip install scikit-image
# pip install -upgrade opencv-python @link issue: https://github.com/Zulko/moviepy/issues/2002

from moviepy.editor import *
from skimage.filters import gaussian
import random
import string
from pydantic import BaseModel
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional, 
    Tuple
)
from enum import Enum

class TextArgument(str, Enum):
    """ Text clip argument"""
    color = "color"
    font = "font"

class TextParameters(BaseModel):
    """ 文字浮层参数 """

    txt: Optional[str] = None
    color: str = 'black'
    bg_color: str = 'transparent'
    fontsize: Optional[Any] = None
    font: str = 'Microsoft-YaHei-Bold-&-Microsoft-YaHei-UI-Bold'
    kerning: Optional[Any] = None
    align: str = 'center'
    position: Optional[Any] = ('center', 'top')


# 视频混剪参数
class VideoParameters(BaseModel):
    """ 视频混剪参数"""

    video_files: List[str] 
    clip_duration: int = 5
    music_file: Optional[str] = None
    size_width: int = 720
    size_height: int = 1280
    text_params: Optional[List['TextParameters']] = None
    output_file: str = "output.mp4"
    output_count: int = 1


class VideoMixer():
    def __init__(self):
        ''' init method '''

    def list(self, arg):
        """ Returns the list of all valid entries for the argument of ``TextClip`` given (can be ``font``, ``color``)"""
        return TextClip.list(arg)

        
    # 随机截取
    def random_clip(self, input_video_path, clip_duration, size_width, size_height):
        """ 随机截取视频"""

        # 加载视频，禁用原始音频
        video_clip = VideoFileClip(input_video_path,audio=False)
        # 获取视频长度
        video_duration = video_clip.duration
        # 随机选择截取的起始时间,长度的随机截取
        start_time = random.uniform(0, video_duration - clip_duration)  
        # 截取视频片段
        clipped_video = video_clip.subclip(start_time, start_time + clip_duration)
        # 统一分辨率
        clipped_video = clipped_video.resize(width = size_width)

        # 返回视频
        return clipped_video

    # 虚化函数
    def blur(self, image):
        """ Returns a blurred (radius=2 pixels) version of the image """
        return gaussian(image.astype(float), sigma=4)

    def random_filename(self, filename, length = 4):
        """ 为输出文件添加随机字符串 """

        # 生成一个包含字母和数字的四位随机字符串
        characters = string.ascii_lowercase + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))

        # 分割文件名和扩展名
        name, ext = filename.rsplit('.', 1)
        # 创建新的文件名
        new_filename = f"{name}_{random_string}.{ext}"
        return new_filename

    # 混剪视频
    def mixing_clip(self, video_params: VideoParameters):
        """ 随机混剪视频，自动生成多个视频"""

        video_files = video_params.video_files
        clip_duration = video_params.clip_duration
        size_width = video_params.size_width
        size_height = video_params.size_height
        text_params = video_params.text_params
        bg_music_file = video_params.music_file
        output_file = video_params.output_file
        final_clips = []

        # 随机截取视频
        video_clips = []
        for file in video_files:
            clip = self.random_clip(file,clip_duration,size_width,size_height)
            video_clips.append(clip)
        
        # 把视频段拼接成一个完整视频
        video_clip = concatenate_videoclips(video_clips)
        video_clip= video_clip.set_position("center")
        video_duration = video_clip.duration

        # 生成虚化满屏背景
        background_clip = video_clip.set_fps(1)
        background_clip = background_clip.fl_image(self.blur)
        background_clip = background_clip.resize(width=size_width, height=size_height)

        final_clips.append(background_clip)
        final_clips.append(video_clip)

        # 生成文字浮层
        if text_params is not None:
            for text_param in text_params:
                text_clip = TextClip(text_param.txt,fontsize=text_param.fontsize,font=text_param.font,color=text_param.color,kerning=text_param.kerning,bg_color=text_param.bg_color)
                text_clip = text_clip.set_position(text_param.position)
                text_clip = text_clip.set_duration(video_duration)
                final_clips.append(text_clip)


        # 合并最终视频+音频
        final_clip = CompositeVideoClip(final_clips,size=(size_width,size_height))

        # 设置视频剪辑的音频，加载并截取长度
        if bg_music_file is not None:
            audio_clip = AudioFileClip(bg_music_file)
            audio_clip = audio_clip.set_duration(video_duration)
            final_clip = final_clip.set_audio(audio_clip)
        
        # 输出视频
        output_file = self.random_filename(output_file)
        final_clip.write_videofile(output_file)

