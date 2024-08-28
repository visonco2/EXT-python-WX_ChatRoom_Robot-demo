import requests
import asyncio
import websockets
import json
from typing import Optional,Literal



class 小天接口():

    def __init__(self):
        KEY_INI=requests.get("http://127.0.0.1:8203/ext/www/key.ini")

        print(KEY_INI.text)
        KEY_INI=KEY_INI.json()

        self.websocket_url ="ws://127.0.0.1:8202/wx?name="+KEY_INI["name"]+"&key="+KEY_INI["key"]
        
    
    
        
    async def 推送(self,data):
        async with websockets.connect(self.websocket_url) as websocket:
            await websocket.send(json.dumps(data))
            res=await websocket.recv()
            print(res)
            
            res=json.loads(res)
            return res
        
    async def 发送消息(self,信息内容,目标ID,艾特列表:list=None):
        
        # 艾特列表转|分割字符串
        if 艾特列表:
            atid = "|".join(艾特列表)
        else:
            atid = ""
        data={
            "method": "sendText",
            "wxid": 目标ID,
            "msg": 信息内容,
            "atid": atid,
            "pid": 0
        }

        return await self.推送(data)

        
    
    async  def 发送文件(self,文件路径,目标ID,file_type:Optional[Literal['url','file']]='file'):

        data={
            "method": "sendFile",
            "wxid": 目标ID,
            "file": 文件路径,
            "fileType": file_type,
            "pid": 0
        }


        return await self.推送(data)
    
    async def 发送图片(self,图片路径,目标ID,file_type:Optional[Literal['url','file','base64']]='file'):
        data={
            "method": "sendImage",
            "wxid": 目标ID,
            "img": 图片路径,
            "imgType": file_type,
            "pid": 0
        }


        return await self.推送(data)
    
    async def 发送视频(self,视频路径,目标ID,file_type:Optional[Literal['url','file']]='file'):
        data={
            "method": "sendFile",
            "wxid": 目标ID,
            "file": 视频路径,
            "fileType": file_type,
            "pid": 0
        }


        return await self.推送(data)
    

# async def test():
#     import aiohttp
#     import random
#     import tempfile
#     # import ssl

#     # ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
#     # ssl_context.options |= ssl.OP_NO_TLSv1_3
#     # ssl_context.options |= ssl.OP_NO_TLSv1_2
#     # ssl_context.options |= ssl.OP_NO_SSLv2
#     # ssl_context.options |= ssl.OP_NO_SSLv3
#     接口=小天接口()
#     # a=test.发送图片("https://cdn.xxhzm.cn/images/heisi/SL7H29dhdGoPSTEXGGI1ZxSP.jpg","filehelper",img_type="url")
#     # a=接口.发送视频(r"https://tucdn.wpon.cn/api-girl/videos/133.mp4","filehelper",'url')
    
#     await  接口.发送消息('男改:🍀测试\n女改:🌸测试\n拒撩/情侣改：💞XX','filehelper')
    
# asyncio.run(test())