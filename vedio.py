import tkinter as tk
import webbrowser
import requests
import re

root = tk.Tk()
root.geometry('600x260+200+200')
root.title('御用在线观看视频')

def show():
    num = num_int_var.get()
    word = input_va.get()
    if num == 1:
        print('选择1接口')
        print('输入的内容是：', word)
        link = 'https://jiexi.pengdouw.com/jiexi1/?url=' + word
        html_data = requests.get(url=link).text
        vedio_url = re.findall(
            '<iframe id="baiyug" scrolling="no" src="(.*?)"', html_data)[0]
        webbrowser.open(vedio_url)
    elif num == 2:
        print('选择2接口')
        print('输入的内容是：', word)
        link = 'https://jiexi.pengdouw.com/jiexi2/?url=' + word
        html_data = requests.get(url=link).text
        vedio_url = re.findall(
            '<iframe id="baiyug" scrolling="no" src="(.*?)"', html_data)[0]
        webbrowser.open(vedio_url)
    elif num == 3:
        print('选择3接口')
        print('输入的内容是：', word)
        link = 'https://jiexi.pengdouw.com/jiexi3/?url=' + word
        html_data = requests.get(url=link).text
        vedio_url = re.findall(
            '<iframe id="baiyug" scrolling="no" src="(.*?)"', html_data)[0]
        webbrowser.open(vedio_url)


#img
choose_frame = tk.LabelFrame(root)
choose_frame.pack(fill='x', padx=10, pady=10)

tk.Label(choose_frame, text='选择接口:', font=('楷体', 15)).grid(row=0,
                                                           column=0,
                                                           sticky='w')

num_int_var = tk.IntVar()
num_int_var.set(1)

tk.Radiobutton(choose_frame,
               text='通用引擎1',
               font=('楷体', 15),
               variable=num_int_var,
               value=1).grid(row=0, column=1, sticky='w')
tk.Radiobutton(choose_frame,
               text='通用引擎2',
               font=('楷体', 15),
               variable=num_int_var,
               value=2).grid(row=0, column=2, sticky='w')
tk.Radiobutton(choose_frame,
               text='通用引擎3',
               font=('楷体', 15),
               variable=num_int_var,
               value=3).grid(row=0, column=3, sticky='w')

input_frame = tk.LabelFrame(root)
input_frame.pack(fill='x', padx=10, pady=10)

#input
input_va = tk.StringVar()
tk.Label(input_frame, text='播放地址:', font=('楷体', 15)).pack(side=tk.LEFT)
tk.Entry(input_frame, width=100, relief='flat',
         textvariable=input_va).pack(side='left')

#button
tk.Button(root, text='播放', font=('楷体', 15), relief='flat', bg='#FFA500',
          command=show).pack(pady=10)

#mainloop
root.mainloop()