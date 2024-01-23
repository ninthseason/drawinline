import time

from prompt_toolkit import *
from prompt_toolkit.completion import *
from prompt_toolkit.document import Document
from prompt_toolkit.validation import *
from PIL import ImageGrab
from lib import pil2cv, line_draft
from imgprocess import image2stroke
from mctl import draw_stroke
import cv2
import pyautogui

app_banner = "<b><yellow bg='black'>Draw</yellow><black bg='yellow'>Inline</black></b>\n" \
             "<gray>Version: 0.2.0</gray>\n" \
             "输入 <b>`help`</b> 获取帮助信息"
app_session = PromptSession()
app_completer = FuzzyCompleter(NestedCompleter({
    'show': None,
    "draw": None,
    "help": None,
    "quit": None,
    ":threshold1": None,
    ":threshold2": None,
    ":start-point": None
}))


def app_help(_):
    help_text = "DrawInline 使用剪切板内的图片作为目标图片\n" \
                "请搭配能将图片暂存至剪切板的截图软件使用\n\n" \
                "命令说明\n" \
                "`:threshold1` 查看当前 threshold1 值\n" \
                "`:threshold2` 查看当前 threshold2 值\n" \
                "`:threshold1 [整数]` 设置 threshold1 值\n" \
                "`:threshold2 [整数]` 设置 threshold2 值\n" \
                "threshold1 为弱边缘下界, threshold2为弱边缘上界，详见 Canny 算法双阈值设置\n" \
                "`:start-point` 将当前鼠标设置为画板原点\n" \
                "将鼠标移动至画布左上角执行:start-point\n" \
                "`show` 显示当前剪切板图片的线稿形态\n" \
                "用于查看当前 threshold 的效果，以便调整 threshold\n" \
                "`draw` 控制鼠标，进行绘图\n" \
                "`quit` 退出程序\n\n" \
                "源代码及问题反馈: <blue><u>https://github.com/ninthseason/drawinline</u></blue>"
    print_formatted_text(HTML(help_text))


threshold1 = 150
threshold2 = 200
start_point = [0, 0]


def app_threshold1(text):
    global threshold1
    if len(text) == 1:
        print_formatted_text(HTML(f"Now threshold1 is: <green>{threshold1}</green>"))
    else:
        threshold1 = int(text[1])
        print_formatted_text(HTML(f"Threshold1 set to: <green>{threshold1}</green>"))


def app_threshold2(text):
    global threshold2
    if len(text) == 1:
        print_formatted_text(HTML(f"Now threshold2 is: <green>{threshold2}</green>"))
    else:
        threshold2 = int(text[1])
        print_formatted_text(HTML(f"Threshold2 set to: <green>{threshold2}</green>"))


def app_start_point(_):
    global start_point
    p = pyautogui.position()
    start_point = [p.x, p.y]
    print_formatted_text(HTML(
        f"Now start point is: <green>{start_point}</green>"))


def app_show(_):
    im = ImageGrab.grabclipboard()
    if im is None:
        print_formatted_text(HTML("<red>There is no picture in clipboard.</red>"))
        return
    im = pil2cv(im)
    im = line_draft(im, threshold1=threshold1, threshold2=threshold2)
    cv2.imshow("image", im)
    cv2.waitKey(0)


def app_draw(_):
    im = ImageGrab.grabclipboard()
    if im is None:
        print_formatted_text(HTML("<red>There is no picture in clipboard.</red>"))
        return
    im = pil2cv(im)
    stroke = image2stroke(im, preprocess=True, threshold1=threshold1, threshold2=threshold2)
    for t in [3, 2, 1]:
        print(f"{t}...", end="", flush=True)
        time.sleep(1)
    print("")
    try:
        draw_stroke(stroke, start_point, min=1)
    except pyautogui.FailSafeException:
        print_formatted_text(HTML("<red>Painting stop.</red>"))


app_callback = {
    "help": app_help,
    "quit": lambda _: exit(0),
    ":threshold1": app_threshold1,
    ":threshold2": app_threshold2,
    ":start-point": app_start_point,
    "show": app_show,
    "draw": app_draw,
}


class AppValidator(Validator):
    def validate(self, document: Document) -> None:
        text = document.text.split()
        if len(text) == 0:
            raise ValidationError(message="Powered by Kl1nge5")
        if text[0] not in app_callback:
            raise ValidationError(message="Unknown command")
        if (text[0] == ":threshold1" or text[0] == ":threshold2") and len(text) > 1:
            if not text[1].isdigit():
                raise ValidationError(message="Argument must be digit")
            if int(text[1]) > 255 or int(text[1]) < 0:
                raise ValidationError(message="Argument must be >=0 and <=255")


def mainloop():
    text = app_session.prompt("> ", completer=app_completer, validator=AppValidator()).strip().split()
    callback = app_callback.get(text[0], None)
    callback(text)


if __name__ == '__main__':
    print_formatted_text(HTML(app_banner))
    while True:
        mainloop()
