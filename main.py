import asyncio
import atexit
import signal
import threading

from browser.manager import init_manager as init_browser_manager
from output.manager import OutputManager
from proxy.manager import init_manager as init_proxy_manager
from websocket import Websocket

websocket = Websocket()
output_manager = None

def openWs():
    websocket.open()


if __name__ == '__main__':
    t1 = threading.Thread(target=openWs)
    t1.daemon = True
    t1.start()

    proxy_manager = init_proxy_manager()
    proxy_manager.start_loop()
    browser_manager = init_browser_manager()


    output_manager = OutputManager()
    output_manager.setWs(websocket)


    def terminate(*_):
        print("terminate")
        websocket.Close()
        
        browser_manager.terminate()
        output_manager.terminate()
        proxy_manager.terminate()



    atexit.register(terminate)
    signal.signal(signal.SIGTERM, terminate)
    signal.signal(signal.SIGINT, terminate)

    output_manager.start_loop()

    try:
        proxy_manager.join()
    finally:
        terminate()

