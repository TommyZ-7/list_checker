
# -*- coding: utf-8 -*-

import socket
import pickle
from tkinter import messagebox
from multiprocessing import Process
import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter import filedialog
import csv
import threading
import datetime
import sys
import numpy as np
import os
import pandas as pd
import webbrowser

import IOlogger



TEXT_COLORS = {
    'MESSAGE' : 'black',
    'INPUT' : 'blue',
    'OUTPUT' : 'green',
    'DEBUG' : 'yellow'    
    }

global read_data
global CHECK_COUNT

CHECK_COUNT = 0

def app_break():
    sys.exit()
    


def run_server():
    global my_ip
    global my_port
    global server_state
    
    try:
        tmp = server_state
    except:
        server_state = False

    if check1.instate(['selected']) and server_state == True:
        check1.state(['!selected'])
        messagebox.showerror("エラー", "サーバーが既に起動しています。\n数秒おいてから再度実行してください。")
        return
    elif check1.instate(['!selected']) and server_state == True:
        return

    my_host = socket.gethostname()
    my_port = 12345

    # ipアドレスを取得、表示
    my_ip = socket.gethostbyname(my_host)


    print(my_ip) 
    
    while True:
        try:
            # ソケットを作成
            test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #タイムアウト設定
            test_sock.settimeout(10)
            # ホスト名
            host = my_ip
            
            # ソケットをバインド
            test_sock.bind((host, my_port))
            break
        except:
            my_port += 1
            print("ポート番号を変更しました。" + str(my_port - 1) + " => " + str(my_port))            
        
    
    test_sock.close()
    ip = str(ent1.get())
    port = ent2.get()
    
    
    if check1.instate(['selected']) and server_state == False: 
        messagebox.showinfo("情報", "サーバーを起動します。\n接続先のpcに次のipアドレスとポート番号を入力してください。\n" + my_ip + ":" + str(my_port))
        IOlogger.IOlogprint(logframe, "サーバーを起動しました。", loglevel="server")
        IOlogger.IOlogprint(logframe, my_ip + ":" + str(my_port)  , loglevel="server")
        thread1 = threading.Thread(target=server, args=())
        thread1.start()
        
    elif check1.instate(['selected']) and server_state == True:
        check1.state(['!selected'])
        messagebox.showerror("エラー", "サーバーが既に起動しています。\n数秒おいてから再度実行してください。")
        return
    else:
        pass

def server():
    global CHECK_COUNT
    global match_data
    global server_state
    server_state = True
    # ipアドレスを取得、表示
    print(my_ip) 
    

    
    # ソケットを作成
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #タイムアウト設定
    sock.settimeout(10)
    # ホスト名

    # ソケットをバインド
    sock.bind((my_ip, my_port))

    # 接続を待機
    sock.listen(1)
    while True:
        try:
            # クライアントからの接続を受け入れる
            conn, addr = sock.accept()
        except:
            print("タイムアウトしました。")
            if check1.instate(['selected']):
                print("接続再待機")
                pass
            else:
                print("サーバーを停止します。")
                server_state = False
                IOlogger.IOlogprint(logframe, "サーバーを停止しました。", loglevel="server")
                return
        else:
            break
    # データを受信
    data = conn.recv(1024)
    if data == b"ping":
        print("pingを受信しました。")
        IOlogger.IOlogprint(logframe, "pingを受信しました。", loglevel="server")
        sock.close()
        if check1.instate(['selected']):
            server()
        else:
            server_state = False
            return
        return
    
    list_data = pickle.loads(data)
    logframe.see("end")


    # 受信したデータを表示
    print('Received:', list_data)
    
    if len(list_data) == len(read_data):
        for i in range(0,len(list_data)):
            if read_data[i][0] == list_data[i][0]:
                same_data = True
                #if read_data[i][1] == list_data[i][1]:
                    #pass
                #else:
                    #read_data[i][1] = "O"
                    #tree.set(i, 1, "O")
            else:
                same_data = False
                #messagebox.showerror("エラー", "リストの内容が異なります。")
                #break
    else:
        messagebox.showerror("エラー", "リストの長さが一致しません。")
    match_data = {}
    match_count = 0
    if same_data == True:
        for i in range(0,len(list_data)):
            if (read_data[i][1] == list_data[i][1]) and read_data[i][1] != "O":
                pass

            elif (read_data[i][1] == list_data[i][1]) and read_data[i][1] == "O":
                pass

            elif (read_data[i][1] != list_data[i][1]) and list_data[i][1] != "O":
                pass

            else:
                read_data[i][1] = "O"
                tree.set(i, 1, "O")
                IOlogger.IOlogprint(logframe, "Received : " + str(read_data[i][0]), loglevel="connection")
                CHECK_COUNT += 1
                set_statistic()
                
                

    else:
        messagebox.showerror("エラー", "リストの内容が異なります。")
    if match_count != 0:
        for i in range(0,match_count):
            IOlogger.IOlogprint(logframe, "Received : " + str(read_data[match_data[i]][0]), loglevel="connection")


    # ソケットをクローズ
    sock.close()
    if check1.instate(['selected']):
        server()


def righttree(inputid):
    global CHECK_COUNT
    global read_data
    try:
        result =  str(inputid) in str(read_data)
    except NameError:
        messagebox.showerror("エラー", "リストが読み込まれていません。")
        return
    
    if result == True:
        print("照合成功")
        la31["text"] = inputid
        la31["foreground"] = "black"
        

        for y, row in enumerate(read_data):
            try:
                rawidx = (y, row.index(inputid))
                break
            except ValueError:
                pass
        idx = rawidx[0]
        print(idx)
        if read_data[idx][1] == "":
            read_data[idx][1] = "O" 
            up_item =  tree.set(idx, 1, "O")
            #指定したiidのアイテムを選択する
            tree.selection_set(idx)
            tree.see(idx)
            IOlogger.IOlogprint(logframe, "Checked : " + str(read_data[idx][0]), loglevel="info")
            CHECK_COUNT += 1


            try:
                if send_state == True:
                    threading.Thread(target=send_data, args=(read_data,read_data[idx][0]),).start()
            except:
                pass

        else:
            IOlogger.IOlogprint(logframe, "すでに出席済みです。 => " + str(read_data[idx][0]), loglevel="warning")

            up_item =  tree.set(idx, 1, "O")
            #指定したiidのアイテムを選択する
            tree.selection_set(idx)
            tree.see(idx)
        
        


        
    else:
        print("")
        la31["text"] = inputid
        la31["foreground"] = "red"
        messagebox.showerror("エラー", "リスト内に存在しません。=>" + inputid)
    set_statistic()

    print(str(read_data.count('O')))
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    data_time = now.strftime('%Y%m%d%H%M%S')
    
    fle = "backup/" + str(data_time)
    
    with open(fle + ".csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(read_data)
    


def th(event):
    if not os.path.exists("backup"):
        os.makedirs("backup")
        print("backupフォルダを作成しました。")
    
    input_id = imput_e1.get()  
    if len(input_id) != 0:
        threading.Thread(target=righttree, args=(input_id,)).start()
        imput_e1.delete(0, tk.END)
    else:
        messagebox.showerror("エラー", "テキストボックスに入力してください。" + input_id)
        imput_e1.delete(0, tk.END)

    
    imput_e1.focus_set()


def readcsv():
    global CHECK_COUNT
    global data
    global read_data
    global list_count
    global add_line
    
    add_line = []
    list_count = 0
    read_data = []
    
    tree.delete(*tree.get_children())
    typ = [('Excelファイル','*.xlsx')] 
    dir = 'C:\\pg'
    fle = filedialog.askopenfilename(filetypes = typ, initialdir = dir)
    
    read_file =pd.read_excel(fle, header=None)
    read_file.to_csv ("tmp.csv", index = None, header=None, encoding="utf-8-sig")

    
    with open("tmp.csv", encoding="utf-8-sig") as data:
        for row in data:
            tree.insert("", "end", iid=list_count, values=(row.split(',')))
            list_count += 1  
    
    with open("tmp.csv", encoding="utf-8-sig") as data:
        read_data = list(csv.reader(data))
    
    try:
        if read_data[0][1] == True:
            pass
    except IndexError:
        for i in range(0,list_count):
            add_line.append([""])
        nm_data = np.concatenate((read_data, add_line), axis=1)
        read_data = nm_data.tolist()
        print("リストの長さが不足していたため、補完しました。")

    print(read_data)
    print("読み込みました。")
    os.remove("tmp.csv")
    target = "O"
    for row in read_data:
        second_column = row[1]
        CHECK_COUNT += second_column.count(target)
    set_statistic()

    print("一時ファイルを削除しました。")

def statistics():
    pass

def writecsv():
    typ = [('xlsxファイル','*.xlsx')] 
    dir = 'C:\\pg'
    fle = filedialog.asksaveasfilename(filetypes = typ, initialdir = dir,defaultextension = ".xlsx") 
    df_sheet1 = pd.DataFrame(read_data)
    len1 = len(df_sheet1)
    len2 = df_sheet1.iloc[:, 1].str.contains('O').sum()
    len3 = len2 / len1 * 100
    print(len1)
    print(len2)
    print(len3)



    df_sheet2 = pd.DataFrame({'col_0': ['総数', str(len1)],
                                'col_1': ["出席数", str(len2)],
                                'col_2': ['出席率', str(len3)],},
                                index=['row_0', 'row_1'])

    print(df_sheet1)
    print(fle)
    with pd.ExcelWriter(fle) as writer:
        df_sheet1.to_excel(writer, sheet_name='new_sheet1',index=False, header=False)
        df_sheet2.to_excel(writer, sheet_name='new_sheet2',index=False, header=False)
    """
    with open(fle + ".csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(read_data)
    print("書き出しました。")
    """

def set_table(root):                         #テーブルの作成
    #tableの設定


    fontsize = 20
    font = tk.font.Font(size = fontsize)
    ttk.Style().configure("Treeview.Heading", font=('MS明朝', fontsize))
    ttk.Style().configure("Treeview", font=('MS明朝', fontsize), rowheight=font.metrics()['linespace'])

    #1列目の設定
    tree.column('#0',width=0, stretch='no')
    tree.column('ID', anchor='w', width=330)
    tree.column('status',anchor='w', width=100)

    tree.heading('#0',text='')
    tree.heading('ID', text='学籍番号',anchor='center')
    tree.heading('status', text='出席', anchor='w')

    #tableの設置
    tree.place(x = 450,y = 10)

def set_statistic():
    global CHECK_COUNT
    la34_text = "総数: " + str(len(read_data)) + " 出席数: " + str(CHECK_COUNT) + " 出席率: " + (str(CHECK_COUNT / len(read_data) * 100))[:4] + "%"
    la34["text"] = la34_text

def show_soft_info():
    infow = tk.Tk()
    infow.title("出席管理表")
    infow.geometry("450x200")
    infow.resizable(width=False, height=False)
    infow.focus_force()

    info_la = ttk.Label(infow, text = "このソフトについて", font=("MS明朝", 20))
    info_la.place(x = 10, y = 10)

    info_canvas = tk.Canvas(infow, bg="white", height=100, width=100)
    info_canvas.place(x = 10, y = 50)

    img = tk.PhotoImage(file="icon.png", width=100, height=100, master=infow)
    info_canvas.create_image(0, 0, image=img, anchor=tk.NW)

    info_la2 = ttk.Label(infow, text = "バージョン: ver1.0")
    info_la2.place(x = 120, y = 50)
    info_la3 = ttk.Label(infow, text = "製作者: TK")
    info_la3.place(x = 120, y = 80)
    info_la4 = ttk.Label(infow, text = "GitHub: ")
    info_la4.place(x = 120, y = 110)
    info_la5 = ttk.Label(infow, text = "https://github.com/TKsanX/list_checker")
    info_la5.place(x = 165, y = 110)
    info_la5.bind("<Button-1>", lambda e:link_click("https://github.com/TKsanX/list_checker"))


    infow.mainloop()

def link_click(url):
    webbrowser.open_new(url)


def set_menu(root):
    #rootメニューバーの設定
    menubar = tk.Menu(root)

    menu1 = tk.Menu(menubar, tearoff = False)
    menu1.add_command(label = "logウィンドウの表示",command = run_logwindow, state="disable")
    menu1.add_command(label = "終了",command = app_break)
    
    menu2 = tk.Menu(menubar, tearoff = False)
    menu2.add_command(label = "Excelファイルの読み込み",  command = readcsv)
    menu2.add_command(label = "Excelファイルの書き出し",  command = writecsv)

    menu3 = tk.Menu(menubar, tearoff = False)

    menu3.add_command(label = "このソフトについて",  command = show_soft_info)


    menubar.add_cascade(label="メニュー", menu=menu1)
    menubar.add_cascade(label="ファイル", menu=menu2)
    menubar.add_cascade(label="ヘルプ", menu=menu3)


    root.config(menu=menubar)

def  run_logwindow():
    pass

def clear_tree():
    tree.delete(*tree.get_children())

def com_push(event):                #画質設定用のコンボボックス切り替え用
    pass

def com2_push(event):
    pass

def send_data_rdy():
    global send_state
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ent1.get(), int(ent2.get())))
            print("pingを送信...")
            s.sendall(b"ping")
            IOlogger.IOlogprint(logframe, "pingの送信に成功しました。", loglevel="server")

    except:
        messagebox.showerror("エラー", "接続に失敗しました。")
        send_data_stop()
        IOlogger.IOlogprint(logframe, "pingの送信に失敗しました。", loglevel="warning")

        return
    
    send_state = True
    btn1["state"] = "disable"
    btn2["state"] = "normal"
    ent1["state"] = "disable"
    ent2["state"] = "disable"

def send_data_stop():
    global send_state
    send_state = False
    btn1["state"] = "normal"
    btn2["state"] = "disable"
    ent1["state"] = "normal"
    ent2["state"] = "normal"


def send_data(send_read_data,this_id):
    print(send_read_data)
    d_data = pickle.dumps(send_read_data)

# 送信先のホストとポート

    try:
        # ソケットを作成し、指定されたホストとポートに接続する
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ent1.get(), int(ent2.get())))

            # 変数をバイト列に変換して送信する
            s.sendall(d_data)
    except ConnectionRefusedError:
        IOlogger.IOlogprint(logframe, "送信に失敗しました。 => " + str(this_id), loglevel="warning")
        send_data_stop()
        return
    
def IOlogprint(logframe, re_text, loglevel):
    if loglevel == "info":
        dt_now = datetime.datetime.now()
        logframe.insert(tk.END,dt_now.strftime('%H:%M:%S ') + "Info       |" + re_text + "\n", "info")
        logframe.see(tk.END)
    
    elif loglevel == "error":
        dt_now = datetime.datetime.now()
        logframe.insert(tk.END,dt_now.strftime('%H:%M:%S ') + "Error      |" + re_text + "\n", "error")
        logframe.see(tk.END)
    
    elif loglevel == "warning":
        dt_now = datetime.datetime.now()
        logframe.insert(tk.END,dt_now.strftime('%H:%M:%S ') + "Warning    |" + re_text + "\n", "warning")
        logframe.see(tk.END)

    elif loglevel == "connection":
        dt_now = datetime.datetime.now()
        logframe.insert(tk.END,dt_now.strftime('%H:%M:%S ') + "Connection |" + re_text + "\n", "connection")
        logframe.see(tk.END)

    elif loglevel == "server":
        dt_now = datetime.datetime.now()
        logframe.insert(tk.END,dt_now.strftime('%H:%M:%S ') + "Server     |" + re_text + "\n", "server")
        logframe.see(tk.END)



root = tk.Tk()
root.title("出席管理表")
root.geometry("900x450")
root.resizable(width=False, height=False)



column = ('ID', 'status')
tree = ttk.Treeview(root, columns=column,height=14)

set_table(root)
set_menu(root)

notebook = ttk.Notebook(root)

note0 = ttk.Frame(notebook, width = 400, height = 345)
note1 = ttk.Frame(notebook, width = 400, height = 345)
note2 = ttk.Frame(notebook, width = 400, height = 345)



notebook.add(note0, text = "設定")
notebook.add(note1, text = "接続")
notebook.add(note2, text = "情報")
notebook.select(note2)




notebook.place(x = 10, y = 50)

#######ノートの内部設定#######

#全般ページ

co1 = "出席確認"
#co2 = "最高画質"
#co3 = "標準画質"
#co4 = "音声のみ"
#co5 = "音声ソース"
#co6 = "デバッグ"

v =tk.StringVar()


item_list = [co1] 
com1 = ttk.Combobox(                     
    master=note0,
    values=item_list,
    state="readonly",
    textvariable=v
    )

check1_set = tk.BooleanVar()
check1_set.set(False)

la11 = ttk.Label(note0, text = "・動作モード")


com1.current(0)


la11.place(x = 10, y = 10)
com1.place(x = 10, y = 30)

com1.bind('<<ComboboxSelected>>', com_push)

#接続
la3 = ttk.Label(note1, text = "・接続先ipアドレス")
ent1 = ttk.Entry(note1,width = 35)
la4 = ttk.Label(note1, text = "・接続先ポート番号")
ent2 = ttk.Entry(note1,width = 35)
check1 = ttk.Checkbutton(note1, text = "同期モード",command=run_server, variable=check1_set)



la3.place(x = 10, y = 10)
ent1.place(x = 10, y = 30)
la4.place(x = 10, y = 60)
ent2.place(x = 10, y = 80)
check1.place(x = 10, y = 300)


btn1 = ttk.Button(note1, text = "接続",command=send_data_rdy, state="normal")
btn2 = ttk.Button(note1, text = "切断",command=send_data_stop, state="disable")


btn1.place(x = 280, y = 30)
btn2.place(x = 280, y = 80)



#情報
la31 = ttk.Label(note2, text = "",font=("MS明朝", 70))


la31.place(x = 20, y = 20)

la32 = ttk.Label(note2, text = "・ログ")
la34 = ttk.Label(note2, text = "")

la32.place(x = 10, y = 130)
la34.place(x = 200, y = 130)

logframe = tk.Text(note2, width=54, height=14)


logframe.place(x = 10, y = 150)

logframe.tag_config('info', foreground="blue")
logframe.tag_config('warning', foreground="red")
logframe.tag_config('error', background="yellow", foreground="red")
logframe.tag_config('connection', foreground="green")
logframe.tag_config('server', foreground="black")


#######################################################

imput_e1 = ttk.Entry(root,width = 30,font=("MS明朝", 19))
imput_e1.place(x = 10,y = 10)
imput_e1.bind('<Return>', th)


#rootウィンドウの作成と設置
frame = tk.Frame(root)
frame.pack(padx=20,pady=10)


root.mainloop()
