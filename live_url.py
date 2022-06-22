import os

def url():
    return "https://live.douyin.com/2510883151"

def downloadDir():
    return getScriptDir()+f"{os.sep}..{os.sep}..{os.sep}nginxRoot{os.sep}download"

def getScriptDir():
    return os.path.split(os.path.realpath(__file__))[0]

def douyinLiveDir():
    return getScriptDir()+f"{os.sep}douyinLiveFile"