import datetime
import tkinter as tk





def IOlogprint(logframe, re_text, loglevel):
    print("io print")
    if loglevel == "info":
        print("info")
        dt_now = datetime.datetime.now()
        logframe.insert(tk.END,dt_now.strftime('%H:%M:%S ') + "Info       |" + re_text + "\n", "info")
        logframe.see(tk.END)
    
    elif loglevel == "error":
        print("error")
        dt_now = datetime.datetime.now()
        logframe.insert(tk.END,dt_now.strftime('%H:%M:%S ') + "Error      |" + re_text + "\n", "error")
        logframe.see(tk.END)
    
    elif loglevel == "warning":
        print("warning")
        dt_now = datetime.datetime.now()
        logframe.insert(tk.END,dt_now.strftime('%H:%M:%S ') + "Warning    |" + re_text + "\n", "warning")
        logframe.see(tk.END)

    elif loglevel == "connection":
        print("connection")
        dt_now = datetime.datetime.now()
        logframe.insert(tk.END,dt_now.strftime('%H:%M:%S ') + "Connection |" + re_text + "\n", "connection")
        logframe.see(tk.END)

    elif loglevel == "server":
        print("server")
        dt_now = datetime.datetime.now()
        logframe.insert(tk.END,dt_now.strftime('%H:%M:%S ') + "Server     |" + re_text + "\n", "server")
        logframe.see(tk.END)
