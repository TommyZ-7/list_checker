import datetime
import tkinter as tk





def IOlogprint(logframe, re_text, loglevel):
    if loglevel == "info":
        dt_now = datetime.datetime.now()
        logframe.insert(tk.END,dt_now.strftime('%H:%M:%S|') + "Info       |" + re_text + "\n", "info")
        logframe.see(tk.END)
    
    elif loglevel == "error":
        dt_now = datetime.datetime.now()
        logframe.insert(tk.END,dt_now.strftime('%H:%M:%S|') + "Error      |" + re_text + "\n", "error")
        logframe.see(tk.END)
    
    elif loglevel == "warning":
        dt_now = datetime.datetime.now()
        logframe.insert(tk.END,dt_now.strftime('%H:%M:%S|') + "Warning    |" + re_text + "\n", "warning")
        logframe.see(tk.END)

    elif loglevel == "connection":
        dt_now = datetime.datetime.now()
        logframe.insert(tk.END,dt_now.strftime('%H:%M:%S|') + "Connection |" + re_text + "\n", "connection")
        logframe.see(tk.END)

    elif loglevel == "server":
        dt_now = datetime.datetime.now()
        logframe.insert(tk.END,dt_now.strftime('%H:%M:%S|') + "Server     |" + re_text + "\n", "server")
        logframe.see(tk.END)
