from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
from ctypes import *
import pyautogui

def call_idle():
    global f
    global n_num
    duration = get_idle_duration()
    idle_time = str(round(duration, 2))
    if(float(n_num)<=float(idle_time)):
        pyautogui.moveRel(0, 50, duration = 1)
        pyautogui.click()
    f = jiggle.after(1000, call_idle)


class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_int),
    ]

def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    if windll.user32.GetLastInputInfo(byref(lastInputInfo)):
        millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
        return millis / 1000.0
    else:
        return 0

jiggle = Tk()
jiggle.title('Mouse Jiggler')
jiggle.iconbitmap('Mice.ico')
jiggle.geometry("400x230")

def input_check(text):
    text = text.rstrip()
    number, part, t_p = text.partition(' ')
    flag = 0
    n_num = 0
    mul_val = 60
    if(number.isdigit()):
        if(int(number)>0):
            if(t_p.lower() in ['minute', 'minutes'] and int(number)<60):
                mul_val = 60
                flag = 1
            if(t_p.lower() in ['hour', 'hours'] and int(number)<24):
                mul_val = 60 * 60
                flag = 1
            n_num = int(number) * mul_val

    return flag, n_num


def show():
    global label
    global mycombo
    global start_b
    global stop_b
    global n_num

    n_num = 0

    text = mycombo.get()
    condition, n_num = input_check(text)

    if(condition == 1):
        label.grid_forget()
        label = Label(jiggle, text = "Mouse will move if System is idle for " + mycombo.get(), fg = '#1E90FF')
        label.grid(row = 1, column = 0, pady = (70,10))
        stop_b = Button(jiggle, text = 'Stop', height = 1, width = 10, command = stop)
        start_b = Button(jiggle, text = 'Start', height = 1, width = 10, command = show, state = DISABLED)

        mycombo = ttk.Combobox(jiggle, value = [text], state = 'disabled')
        mycombo.current(0)
        mycombo.bind("<<ComboboxSelected>>")
        mycombo.grid(row = 1, column = 0, padx = 65, pady = (0, 40))

        start_b.grid(row = 3, column = 0, padx = (0,115))
        stop_b.grid(row = 3, column = 0, padx = (180,50))

        call_idle()

    else:
        label.grid_forget()
        label = Label(jiggle, text = "Time given is invalid", fg = '#FF0000')
        label.grid(row = 1, column = 0, pady = (70,10))
    

def stop():
    global label
    global mycombo
    global start_b
    global stop_b
    global f
    global n_num

    n_num = 0

    label.grid_forget()
    label = Label(jiggle, text = "Please Set the condition", fg = '#D2691E')
    label.grid(row = 1, column = 0, pady = (70,10))

    start_b = Button(jiggle, text = 'Start', height = 1, width = 10, command = show)
    start_b.grid(row = 3, column = 0, padx = (0,115))

    stop_b = Button(jiggle, text = 'Stop', height = 1, width = 10, command = stop, state = DISABLED)
    stop_b.grid(row = 3, column = 0, padx = (180,50))

    mycombo = ttk.Combobox(jiggle, value = options)
    mycombo.current(0)
    mycombo.bind("<<ComboboxSelected>>")
    mycombo.grid(row = 1, column = 0, padx = 65, pady = (0, 40))

    if f:
        jiggle.after_cancel(f)
        f = None

options = [
    "1 minute",
    "2 minutes",
    "5 minutes",
    "10 minutes",
    "1 hour"
]

text_label = Label(jiggle, text = "Move mouse whenever the computer is idle for")
text_label.grid(row = 0, column = 0, pady = (0,0))

clicked = StringVar()
clicked.set(options[0])

mycombo = ttk.Combobox(jiggle, value = options)
mycombo.current(0)
mycombo.bind("<<ComboboxSelected>>")
mycombo.grid(row = 1, column = 0, padx = 65, pady = (0, 40))

label = Label(jiggle, text = "Please Set the condition", fg = '#D2691E')
label.grid(row = 1, column = 0, pady = (70,10))

start_b = Button(jiggle, text = 'Start', height = 1, width = 10, command = show)
start_b.grid(row = 3, column = 0, padx = (0,115))

stop_b = Button(jiggle, text = 'Stop', height = 1, width = 10, command = stop, state = DISABLED)
stop_b.grid(row = 3, column = 0, padx = (180,50))

jiggle.resizable(False, False)


def main():
    jiggle.mainloop()

if(__name__ == '__main__'):
    main()
