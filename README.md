# video-mixing-cut

## 视频混剪
基于MoviePy的视频混剪小工具，事实上就是把许多视频剪辑放在一起，变成一个新剪辑。

这里我们采用MoviePy视频混剪，MoviePy在以下方面表现出色：

- **易于上手**：一行即可完成一项基本操作。对于新手来说，代码易学易懂。
- **灵活**：视频和音频的每一帧都尽在掌握，创作属于自己的特效就像Python一样简单。
- **便携**：代码使用十分常见的软件（Numpy和FFMPEG），而且可以在几乎所有版本的Python和几乎所有的机器上运行。

当然MoviePy也有局限性，目前还无法对流媒体进行处理（从摄像头或者远程设备获取视频），并且MoviePy并不是被设计成用来对电影的连续帧进行处理（例如视频去抖，你需要寻找另外的软件）。

所以以下情况中，MoviePy**并非**最好的选择：

- 你只需要对视频进行逐帧分析（如人脸识别或其他有趣的东西），使用MoviePy和别的库可以联合完成。但是事实上，仅使用 [imageio](https://imageio.github.io/)、 [OpenCV](http://opencv.org/) 或者SimpleCV这些专用库即可达到要求。
- 你只需要视频文件转换，或者将一系列图片文件转换成视频。在这种情况下，直接调用`ffmpeg`（或`avconv`、`mencoder`等）将比使用MoviePy更快速、更有效率地使用内存。

详情可以参考[MoviePy官网](https://zulko.github.io/moviepy/index.html)



## 核心步骤

1. 传入`video_files`文件路径列表，随机截取视频文件指定长度`clip_duration` 的视频片段，屏蔽原音频，将视频片段拼接成新视频`video_clip` ，新视频分辨率强制转为`size_width`并居中显示；
2. 拷贝一份新视频`video_clip`作为为背景模糊虚化并置底，生成`background_clip`；
3. 根据`text_params`参数生成文字浮层`text_clip` ，支持多个文字浮层；
4. 将`background_clip` 、`video_clip` 、`text_clip` 合并为新的视频，并添加背景音乐；
5. 生成视频到本地