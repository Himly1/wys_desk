import whisper
import torch
import os
from outputVideoSaver import getOutputFileFolder
import subprocess

model: whisper.Whisper = None


def initModel():
    torch.cuda.is_available()
    global model
    model = whisper.load_model(
        'medium', device='cuda' if torch.cuda.is_available() else 'cpu')


def getFileNameFromThePath(path, noSuffix):
    fileName = os.path.basename(path)
    if noSuffix:
        return fileName.split('.')[0]
    else:
        return fileName


def formatTiming(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def segmentsToSrtFormatFile(pathToSave, segments):
    srt = ''
    for i, item in enumerate(segments):
        start_time = formatTiming(item['start'])
        end_time = formatTiming(item['end'])
        text = item['text']
        srt += f"{i+1}\n{start_time} --> {end_time}\n{text}\n\n"

    with open(pathToSave, 'w', encoding='utf-8') as f:
        f.write(srt)


def audioToSrt(videoFilePath):
    rs = model.transcribe(audio=videoFilePath, verbose=False)
    segments = rs["segments"]
    srtFilePath = os.path.join(getOutputFileFolder(), getFileNameFromThePath(
        videoFilePath, noSuffix=True) + '.srt')
    segmentsToSrtFormatFile(srtFilePath, segments)
    return srtFilePath


def addSrtToVideo(videoPath, srtFilePath, outputPath):
    # srtFilePath = repr(srtFilePath).replace('\\\\', '/')
    # cmd = [
    #     'ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe',
    #     '-i', videoPath,
    #     '-vf',
    #     f"subtitles={srtFilePath}:force_style='Fontsize=24'",
    #     '-c:a', 'copy',
    #     outputPath
    # ]
    # print(f'cmd? ${cmd}')
    srtFilePath = srtFilePath.replace('\\', '\\\\\\\\')
    srtFilePath = srtFilePath.replace(':', '\\\\:')
    cmd = f'ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe -y -i {videoPath} -vf "subtitles={srtFilePath}:force_style=\'Fontsize=24\'" -c:a copy {outputPath}'
    print(f'cmd? ${cmd}')
    subprocess.run(cmd)


def addSubtitle(videoFilePath, results: list):
    if model is None:
        initModel()

    videoOutputPath = os.path.join(
        getOutputFileFolder(), getFileNameFromThePath(videoFilePath, False))
    srtFilePath = audioToSrt(videoFilePath)
    addSrtToVideo(videoFilePath, srtFilePath, videoOutputPath)
    results.append(videoOutputPath)
    return results
