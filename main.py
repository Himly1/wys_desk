import tkinter as tk
from tkinter import Tk
import whisper
from tkinter.filedialog import askopenfilename
import customtkinter
import time
from threading import Thread
import cv2
from PIL import Image, ImageTk
from subTitleAdder import addSubtitle as addSub
import os
from outputVideoSaver import getOutputFileFolder

mainWindow: Tk = None
HEIGH = None
WIDTH = None
customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('blue')

globalStates = {
    "filePath": None,
    "outputFilePath": None
}

def initMainWindow():
    global mainWindow
    mainWindow = customtkinter.CTk()
    mainWindow.title("Wys? Say you want!")
    global HEIGH, WIDTH
    HEIGH = mainWindow.winfo_screenheight()
    WIDTH = mainWindow.winfo_screenwidth()
    mainWindow.geometry('960x520')
    # mainWindow.geometry(f'{960}x{520}+300+50')
    mainWindow.configure(bg='green')
    mainWindow.grid_columnconfigure(0, weight=1)
    mainWindow.grid_columnconfigure(1, weight=1)
    mainWindow.minsize(960, 520)
    mainWindow.maxsize(959, 519)


def getTheRandomFrameFromTheVideoToDisplayAsImage(filePath):
    cap = cv2.VideoCapture(filePath)
    ret, frame = cap.read()
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    photo = ImageTk.PhotoImage(image)
    return photo


def uploadFile(addSubtitleBtn, openOutputFileBtn):
    filename = askopenfilename(
        filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.flv;*.wmv")])

    if not filename:
        print(f'Use cancleed')
        return

    print(f'filename? ${filename}')
    global globalStates
    globalStates.update({"filePath": filename})

    img = getTheRandomFrameFromTheVideoToDisplayAsImage(filename)
    imgDisplay = None
    for child in videoDisplayArea.winfo_children():
        if isinstance(child, customtkinter.CTkLabel):
            imgDisplay = child
            break
    addSubtitleBtn.configure(state='normal')
    openOutputFileBtn.configure(state='disabled')
    if imgDisplay:
        imgDisplay.configure(image=img)
    else:
        videoDisplayArea.rowconfigure(0, weight=1)
        videoDisplayArea.columnconfigure(0, weight=1)
        imgDisplay = customtkinter.CTkLabel(
            videoDisplayArea, text="", image=img, width=600, height=520)
        imgDisplay.grid(row=0, column=0)


def showProgressBar(addSubtitleStateArea) -> list:
    progressFrame = customtkinter.CTkFrame(addSubtitleStateArea)
    progressFrame.grid(row=0, column=0)
    progressFrame.grid_propagate(0)
    progressFrame.columnconfigure(0, weight=1)
    progressFrame.columnconfigure(1, weight=1)

    progressLabel = customtkinter.CTkLabel(progressFrame, text="处理中...")
    progressLabel.grid(row=0, column=0)

    progress = customtkinter.CTkProgressBar(
        progressFrame, width=120, orientation="horizontal")
    progress.grid(row=0, column=1)
    progress.start()

    return [progressFrame, progress]


def addSubtitleOnTheVideo(addSubtitleStateArea, uploadFileBtn, addSubtitleBtn, openOutputFileBtn):
    global globalStates
    globalStates.update({"outputFilePath": None})
    list(map(lambda btn: btn.configure(state='disabled'),
         [uploadFileBtn, addSubtitleBtn, openOutputFileBtn]))
    [progressFrame, progress] = showProgressBar(addSubtitleStateArea)
    rs = []
    t = Thread(target=addSub, args=(globalStates.get('filePath'), rs))
    t.start()

    def check_thread():
        if t.is_alive():
            # Thread is still running
            addSubtitleStateArea.after(100, check_thread)
        else:
            global globalStates
            globalStates.update({"outputFilePath": rs[0]})
            progress.set(1)
            progress.stop()
            return None

    def checkOutput():
        if globalStates.get('outputFilePath') is None:
            progress.after(100, checkOutput)
        else:
            for child in progressFrame.winfo_children():
                if isinstance(child, customtkinter.CTkLabel):
                    child.configure(text="已完成")
            list(map(lambda btn: btn.configure(state='normal'),
                 [uploadFileBtn, openOutputFileBtn]))
            return None

    addSubtitleStateArea.after(100, check_thread)
    progress.after(100, checkOutput)


def showFunctionArea():
    functionArea = customtkinter.CTkFrame(mainWindow, width=300, height=520)
    functionArea.grid(row=0, column=0)
    functionArea.grid_propagate(0)

    functionArea.grid_rowconfigure(0, weight=1)
    functionArea.grid_rowconfigure(1, minsize=260, weight=1)
    functionArea.grid_rowconfigure(2, weight=1)
    functionArea.grid_columnconfigure(0, weight=1)
    functionArea.grid_columnconfigure(2, weight=1)

    title = customtkinter.CTkFrame(functionArea, )
    uploadButton = customtkinter.CTkFrame(functionArea)
    addSubtitle = customtkinter.CTkFrame(functionArea)
    title.grid_propagate(0)
    uploadButton.grid_propagate(0)
    addSubtitle.grid_propagate(0)

    title.grid(row=0, column=1)
    uploadButton.grid(row=1, column=1)
    addSubtitle.grid(row=2, column=1)

    uploadButton.grid_rowconfigure(0, weight=1)
    uploadButton.grid_rowconfigure(3, weight=1)
    uploadButton.grid_columnconfigure(0, weight=1)
    uploadButton.grid_columnconfigure(2, weight=1)

    openOutputFileBtn = customtkinter.CTkButton(uploadButton, state='disabled', text='打开视频', command=lambda: os.startfile(globalStates.get('outputFilePath')))
    openOutputFileBtn.grid(row=2, column=1)

    addSubtitleBtn = customtkinter.CTkButton(
        uploadButton, state='disabled', text="开始添加字幕")
    addSubtitleBtn.configure(command=lambda: addSubtitleOnTheVideo(
        addSubtitle, btn, addSubtitleBtn, openOutputFileBtn))
    addSubtitleBtn.grid(row=1, column=1)

    btn = customtkinter.CTkButton(uploadButton, text="上传视频")
    btn.grid(row=0, column=1)
    btn.configure(command=lambda: uploadFile(addSubtitleBtn, openOutputFileBtn))

    openOutputVideoFolder = customtkinter.CTkButton(uploadButton, text='打开目录', command=lambda: os.startfile(getOutputFileFolder()))
    openOutputVideoFolder.grid(row=3, column=1)


def showVideoDisplayArea():
    displayArea = customtkinter.CTkFrame(mainWindow, width=600, height=520)
    displayArea.grid(row=0, column=1)
    displayArea.grid_propagate(0)
    return displayArea


initMainWindow()
showFunctionArea()
videoDisplayArea = showVideoDisplayArea()
mainWindow.mainloop()
