# -*- coding: utf-8 -*-
# @Time    : 2022/2/18 
# @Author  :
import asyncio, os
import websockets
import json
from colorama import init, Fore
from messages.chat import ChatMessage
import live_url as liveUrl
import requests as requests
# from __future__ import unicode_literals

from output.IOutput import IOutput


def downloadImg(url,path):
    if (os.path.exists(path)):
        print(f"文件已经存在: {path}")
        return
    
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        open(path, 'wb').write(r.content) # 将内容写入图片
        # print(f"CODE: {r.status_code} download {url} to {path}") # 返回状态码
        r.close()
        return path
    else:
        print(f"CODE: {r.status_code} download {url} Failed.")
        return "error"


RED = Fore.RED
GREEN = Fore.GREEN
BLUE = Fore.BLUE
CYAN = Fore.CYAN
MAGENTA = Fore.MAGENTA
YELLOW = Fore.YELLOW
WHITE = Fore.WHITE
RESET = Fore.RESET

class Websocket(IOutput):
    websocket = None

    loop = None

    clients = []

    message = []

    isTerminate = False

    async def onConnect(self, websocket, path):
        print("连接j进来了")
        self.clients.append(websocket)
        while True:
            if self.isTerminate:
                if self.loop != None:
                    self.loop.close()
                break
            if len(self.message) > 0:
                msg = self.message[0]
                self.message.pop(0)
                await websocket.send(json.dumps(msg, ensure_ascii=False))
        print('连接断开了')

    def open(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        print("开启连接")
        # eventLoop = asyncio.get_event_loop()
        print("开启连接222")
        self.websocket = websockets.serve(self.onConnect, "0.0.0.0", 8000)
        print("开启连接333")
        try:
            loop.run_until_complete(self.websocket)
            loop.run_forever()
            
        except KeyboardInterrupt:
            print("Closing the server")
            # loop.close()
            
        # print("开启连接r444")
        # eventLoop.run_forever()
        print("websocket结束了")

    def GetWs(self):
        return self.websocket
    
    def Close(self):
        self.isTerminate = True

    def Send(self, msg):
        self.message.append(msg)

    def chat_output(self, msg: ChatMessage):
        print(f"\nws --> {BLUE}[+] {msg} {RESET}")
        nickname = msg.user().nickname
        userID=msg.user().id
        userHeaderImg = msg.user().avatarThumb.urlList[0]
        downloadImg(userHeaderImg,f"{liveUrl.downloadDir()}{os.sep}{userID}.jpg")
        headImg = f"http://192.168.31.5:1002/{userID}.jpg"
        msg = {"id": msg.user().id, "nickname": nickname, "content": msg.instance.content, "headImg": headImg}
        data = {"t": "chat", "msg": msg}
        self.Send(data)

    def like_output(self, msg):
        print(f"\nws --> {CYAN}[+] {msg} {RESET}")

    def member_output(self, msg):
        print(f"\nws --> {RED}[+] {msg} {RESET}")

    def social_output(self, msg):
        print(f"\nws --> {GREEN}[+] {msg} {RESET}")

    def gift_output(self, msg):
        print(f"\nws --> {MAGENTA}[+] {msg} {RESET}")

    def userseq_output(self, msg):
        print(f"\n{YELLOW}[+] {msg} {RESET}")

    def control_output(self, msg):
        print(f"\nws --> {CYAN}[+] {msg} {RESET}")

    def fansclub_output(self, msg):
        print(f"\nws --> {GREEN}[+] {msg} {RESET}")
