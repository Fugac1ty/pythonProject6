import AI
from tkinter import *  # 导入tkinter模块的所有内容

token = None
speech = None
result = None


def getToken():
    temptoken = AI.getToken(AI.HOST)
    return temptoken


def speech2text():
    global token
    if token is None:
        token = getToken()
    speech = AI.get_audio(AI.FILEPATH)
    result = AI.speech2text(speech, token, dev_pid=1537)
    print(result)
    move(result)


def move(result):
    print(result)
    if "向上" in result:
        canvas.move(1, 0, -30)  # 移动的是 ID为1的事物【move（2,0,-5）则移动ID为2的事物】，使得横坐标加0，纵坐标减30
    elif "向下" in result:
        canvas.move(1, 0, 30)
    elif "向左" in result:
        canvas.move(1, -30, 0)
    elif "向右" in result:
        canvas.move(1, 30, 0)


tk = Tk()
tk.title("语音识别控制图形移动")
Button(tk, text="开始录音", command=AI.my_record).pack()
Button(tk, text="开始识别", command=speech2text).pack()
canvas = Canvas(tk, width=500, height=500)  # 设置画布
canvas.pack()  # 显示画布
r = canvas.create_rectangle(180, 180, 220, 220, fill="red")  # 事件ID为1
mainloop()