from fastapi import FastAPI
from video import VideoMixer,VideoParameters,TextArgument

app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/video/{arg}")
def list(arg: TextArgument):
    clip = VideoMixer()
    return clip.list(arg)

@app.post("/video/cut")
async def video_cut(param: VideoParameters):
    """ 视频混剪 """
    
    """
    请求报文范例：
    {
        "video_files": [
            "https://intoss.polyic.cn/cwzt-public-int/festival/video1_1715912134362.mp4",
            "https://intoss.polyic.cn/cwzt-public-int/festival/video2_1715912099913.mp4",
            "https://intoss.polyic.cn/cwzt-public-int/festival/video3_1715912050364.mp4",
            "https://intoss.polyic.cn/cwzt-public-int/festival/video4_1715911888776.mov"
        ],
        "clip_duration": 5,
        "music_file": "https://intoss.polyic.cn/cwzt-public-int/festival/bg_m_1715912160129.mp3",
        "size_width": 720,
        "size_height": 1280,
        "text_params": [
            {
                "txt": "保利和颂",
                "color": "blue",
                "fontsize": 80,
                "font": "Microsoft-YaHei-Bold-&-Microsoft-YaHei-UI-Bold",
                "kerning": 4,
                "align": "center",
                "position": [
                    "center",
                    "top"
                ]
            },
            {
                "txt": "市区豪宅，购房首选",
                "color": "blue",
                "bg_color": "yellow",
                "fontsize": 60,
                "font": "Microsoft-YaHei-Bold-&-Microsoft-YaHei-UI-Bold",
                "kerning": 4,
                "align": "center",
                "position": [
                    "center",
                    128
                ]
            },
            {
                "txt": "地铁上盖一线江景",
                "color": "white",
                "bg_color": "SkyBlue4",
                "fontsize": 40,
                "font": "华文行楷",
                "kerning": 4,
                "align": "center",
                "position": [
                    "center",
                    1150
                ]
            }
        ],
        "output_file": "output.mp4",
        "output_count": 2
    }

    """

    clip = VideoMixer()
    # 生成多个混剪视频
    for i in range(param.output_count):
         clip.mixing_clip(param)
   
