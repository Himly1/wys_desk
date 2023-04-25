import tkinter as tk
import whisper
import torch


mainWindow = None

model = None


def initModel():
    model = whisper.load_model('medium', device='cuda')
    rs = model.transcribe('arTest.MP4')
    print(rs['segments'])


def initMainWindow():
    global mainWindow
    mainWindow = tk.Tk()
    heigh = mainWindow.winfo_screenheight()
    width = mainWindow.winfo_screenwidth()
    mainWindow.title("Wys! Say you want!")
    mainWindow.geometry(f'{width}x{heigh}+10+20')


def onFileDrop(event):
    file_path = event.data
    print(f'file path? ${file_path}')


def showFileUploader():
    canvas = tk.Canvas(mainWindow, width=300, height=200)
    canvas.pack()
    canvas.create_text(150, 100, text="Drop a file here")
    canvas.bind("<Drop>", onFileDrop)


print(f'cuda? {torch.cuda.is_available()}')
# initModel()
initMainWindow()
showFileUploader()
mainWindow.mainloop()
