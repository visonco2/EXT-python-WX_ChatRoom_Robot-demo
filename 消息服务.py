from typing import Dict
import json
from fastapi import FastAPI, BackgroundTasks
import asyncio
from fastapi.responses import Response
import uvicorn
import aiohttp
import aiofiles
import random
import re
import uuid
from EXT框架接口 import 小天接口
import tempfile
import os
import traceback
app = FastAPI()


接口=小天接口()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(接口.连接())
@app.post("/message")
async def 微信推送(message:Dict):
    # a = json.loads(message)
    
    print("消息内容",message)
    if message['method']=='newmsg' and message['type']==1:

        WXID=message['data']['memid']
        from_wxid=message['data']['fromid']
        content=message['data']['msg']
        print(WXID)
        print(from_wxid)
    elif message['type']==702:
        text=f"欢迎新叼毛加入一起摆烂\n微信名：{message['data']['member'][0]['nickName']}\n群聊名称：{message['data']['member'][0]['nickName2']}"
        await 接口.发送消息(text,message['data']['wxid'])
        if message['data']['member'][0]['nickName2']=='':
            nick_name="xxxxx"
        else:
            nick_name=message['data']['member'][0]['nickName2']
        await  接口.发送消息(f"新人改一下昵称\n男改:🍀{nick_name}\n女改:🌸{nick_name}\n拒撩/有情侣改：💞{nick_name}\n方便分公母，搞暧昧",message['data']['wxid'])
    elif message['type']==703:
        text=f"有个叼毛没人跟他搞暧昧跑了\n微信名：{message['data']['member'][0]['nickName']}\n群聊名称：{message['data']['member'][0]['nickName2']}\n微信ID：{message['data']['member'][0]['wxid']}\n微信号：{message['data']['member'][0]['alias']}"
        await 接口.发送消息(text,message['data']['wxid'])

       
    else:
        return

    
    try:
        if  content=="测试":
            print("测试事件")
            await 接口.发送消息('实验测试',from_wxid)
        
        elif content=="菜单":

            print("菜单事件")
            await 接口.发送消息('======功能菜单======\n--下列功能直接关键字触发--\n[庆祝]舔狗日记[庆祝]美腿盲盒[庆祝]\n[庆祝]战力查询[庆祝]腹肌盲盒[庆祝]\n[庆祝]美女盲盒[庆祝]帅哥盲盒[庆祝]\n[庆祝]人工智障[庆祝]天气查询[庆祝]\n毒鸡汤[庆祝]KFC[庆祝]黄大仙'
                    ,from_wxid)

        elif content=="KFC":
        
            print("KFC事件")
            url="http://api.v1.jixs.cc/api/wenan-fkxqs/index.php?type=json"
            async with aiohttp.ClientSession() as session:

                            async with session.get(url=url, timeout=aiohttp.ClientTimeout(total=3),ssl=False) as response:
                                data = await response.json()
                                await 接口.发送消息(data[0]['kfc'],from_wxid)
        elif content=="舔狗日记":
            
            print("舔狗日记事件")
            url="http://api.52vmy.cn/api/wl/yan/tiangou"
            async with aiohttp.ClientSession() as session:

                            async with session.get(url=url, timeout=aiohttp.ClientTimeout(total=3),ssl=False) as response:
                                data = await response.json()
                                await 接口.发送消息(data['content'],from_wxid)
        elif content=="毒鸡汤":
            
            print("毒鸡汤事件")
            url="http://api.52vmy.cn/api/wl/yan/du?type=json"
            async with aiohttp.ClientSession() as session:

                async with session.get(url=url, timeout=aiohttp.ClientTimeout(total=3),ssl=False) as response:
                    data = await response.text()
                    data = json.loads(data)
                    await 接口.发送消息(data["content"],from_wxid)
        
        
        # 黑丝
        elif content == "美腿盲盒":
            print("看腿事件")
            
            async with aiohttp.ClientSession() as session:
                url = ["http://v2.api-m.com/api/heisi",
                    "http://v2.api-m.com/api/baisi"]
                async with session.get(url=random.choice(url), timeout=aiohttp.ClientTimeout(total=10),ssl=False) as response:
                    data = await response.text()
                    print(data)
                    data = json.loads(data)
                    
                    async with session.get(data["data"]) as response:

                        print(response.content)
                        tmp= tempfile.NamedTemporaryFile(suffix='.jpg',delete=False) 
                        try:
                            tmp.write(await response.read())
                            tmp.flush()
                            print(tmp.name)                                                                                                                                                                     
                            await 接口.发送图片(tmp.name,from_wxid)
                        finally:
                            tmp.close()
        elif content == "腹肌盲盒":
            print("腹肌盲盒")
            
            async with aiohttp.ClientSession() as session:
                url = "http://papi.oxoll.cn/API/ranpic/fj.php"
                async with session.get(url=url, timeout=aiohttp.ClientTimeout(total=10),ssl=False) as response:
                    data = await response.text()
                    print(data)
                    data = json.loads(data)
                    
                    async with session.get(data["image"]) as response:

                        print(response.content)
                        tmp= tempfile.NamedTemporaryFile(suffix='.jpg',delete=False) 
                        try:
                            tmp.write(await response.read())
                            tmp.flush()
                            print(tmp.name)                                                                                                                                                                     
                            await 接口.发送图片(tmp.name,from_wxid)
                        finally:
                            tmp.close()             
        # 黑丝
        elif content == "黄大仙":
            print("黄大仙事件")
            
            图片路径=f"C:\\Users\\NAS\\Desktop\\机器人服务\\抽签\\{random.randint(1, 100)}.png"
                    
            await 接口.发送图片(图片路径,from_wxid)
        elif content == "美女盲盒":
            print("美女盲盒事件")                                                                                               
            video_url="http://tucdn.wpon.cn/api-girl/index.php?wpon=json"
            async with aiohttp.ClientSession() as session:
                async with session.get(video_url,ssl=False) as response:
                    data = await response.text()
                    print(data)
                    data = json.loads(data)                                          
                    data['mp4'] ="http:" +data['mp4']
                    async with session.get(data["mp4"],ssl=False) as response:
                        print(response)
                        tmp= tempfile.NamedTemporaryFile(suffix='.mp4',delete=False) 
                        try:
                            tmp.write(await response.read())
                            tmp.flush()
                            print(tmp.name)                                                                                                                                                                     
                            await 接口.发送文件(tmp.name,from_wxid)
                        finally:
                            tmp.close()
        elif content == "帅哥盲盒":
            print("帅哥盲盒事件")                                                                                               
            video_url="http://papi.oxoll.cn/API/sgsp/"
            async with aiohttp.ClientSession() as session:
                async with session.get(video_url) as response:
                    data = await response.text()
                    print(data)
                    data = json.loads(data)                                          
                    
                    async with session.get(data["video_link"]) as response:
                        print(response)
                        tmp= tempfile.NamedTemporaryFile(suffix='.mp4',delete=False) 
                        try:
                            tmp.write(await response.read())
                            tmp.flush()
                            print(tmp.name)                                                                                                                                                                     
                            await 接口.发送文件(tmp.name,from_wxid)
                        finally:
                            tmp.close()
                            
        elif  content.startswith("人工智障"):
            print("人工智障事件")
            问题=content.replace(' ', '')
            问题=问题.replace('人工智障', '')
            url="http://ai.cloudroo.top/text/gemini/?q="+问题
            async with aiohttp.ClientSession() as session:
                    
                    async with session.get(url=url, timeout=aiohttp.ClientTimeout(total=30),ssl=False) as response:
                        data = await response.text()
                        print(data)
                        
                        await 接口.发送艾特消息("\n"+data,from_wxid, message['data']['final_from_wxid'])
        elif  content.startswith("天气查询"):
            print("天气查询事件")
            城市=content.replace(' ', '')
            城市=城市.replace('天气查询', '')
            url="http://api.lolimi.cn/API/tqtq/api.php?b=1&msg="+城市
            async with aiohttp.ClientSession() as session:
                    
                    async with session.get(url=url, timeout=aiohttp.ClientTimeout(total=3),ssl=False) as response:
                        data = await response.text()
                        data = json.loads(data)
                        print(data)
                        if data["code"]==1:
                            信息 =f"地区：{data['data']['city']}\n昨天：{data['data']['data'][0]['Time']}\n温度：{data['data']['data'][0]['temperature']}\n风力：{data['data']['data'][0]['bearing']}\n天气情况：{data['data']['data'][0]['weather']}\n今天:{data['data']['data'][1]['Time']}\n温度：{data['data']['data'][1]['temperature']}\n风力：{data['data']['data'][1]['bearing']}\n天气情况：{data['data']['data'][1]['weather']}\n明天：{data['data']['data'][2]['Time']}\n温度：{data['data']['data'][2]['temperature']}\n风力：{data['data']['data'][2]['bearing']}\n天气情况：{data['data']['data'][2]['weather']}"
                            
                        else:
                            信息 ="指令错误或者没有该城市。\n正确指令为：天气查询+地区名"
                        await 接口.发送消息(信息,from_wxid)
        # 战力查询
        elif  content.startswith("战力查询"):
            print("战力查询事件")
            英雄=content.replace(' ', '')
            英雄=英雄.replace('战力查询', '')
            url="http://api.yaohud.cn/api/v6/wzzl?key="替换自己的KEY"&lei=wx&name="+英雄
            async with aiohttp.ClientSession() as session:
                    
                    async with session.get(url=url, timeout=aiohttp.ClientTimeout(total=3),ssl=False) as response:
                        data = await response.text()
                        data = json.loads(data)
                        print(data)
                        if data["code"]==200:
                            信息 =f"英雄名称：{英雄}\n县标最低战力：{data['data']['lowest']}\n县镇名：{data['data']['lowestname']}\n市标最低战力：{data['data']['medium']}\n城市名：{data['data']['mediumname']}\n省标最低战力：{data['data']['highest']}\n省份名：{data['data']['highestname']}\n国服最低战力：{data['data']['guobiao']}\n更新时间：{data['data']['time']}\n服务器：安卓微信"
                            
                        else:
                            信息 ="指令错误或者没有该英雄。\n正确指令为：战力查询+英雄名称"
                        await 接口.发送消息(信息,from_wxid)
      

        #  随机万能回复
        elif "智障唧唧人菲菲" in content:

            print("对话事件")
            url="http://api.qingyunke.com/api.php?key=free&appid=0&msg="
        #   清除文字
            msg = re.sub(r'[^\w\s]', '', content)  # 清除非单词字符和非空格字符
            msg = re.sub(r'\u2000-\u200f', '', msg)  # 清除 Unicode 空格字符
            msg=msg.replace('智障唧唧人菲菲', '')
            msg=msg.strip()

            url=url+msg
            async with aiohttp.ClientSession() as session:
                
                async with session.get(url=url, timeout=aiohttp.ClientTimeout(total=5),ssl=False) as response:
                    data = await response.text()
                    data=json.loads(data)
                    if message['data']['nickName2']!="":
                        msg=message['data']['nickName2']
                    else:
                        msg=message['data']['memname']
                    msg="@"+msg+"  "+data['content']
                    await 接口.发送消息(msg,from_wxid,[message['data']['memid']])

        else :
             if random.randint(0, 10) == 1:
                    print("随机聊天事件")
                    url_list=[
                         "https://api.lolimi.cn/API/kout/k.php",
                         "https://api.lolimi.cn/API/qing/api.php",
                         'https://api.lolimi.cn/API/yiyan/api.php',
                         "https://jkapi.com/api/saohua?type=text"
                    ]
                    随机网址 = random.choice(url_list)
                    async with aiohttp.ClientSession() as session:

                        async with session.get(url=随机网址, timeout=aiohttp.ClientTimeout(total=3),ssl=False) as response:
                            # if 随机网址==url_list[1]:
                            #     data = await response.text()
                            #     data = data.replace("━━━━━━━━━","")
                            #     data = data.replace("复苏API污句子","")
                            #     data = data.replace("Tips:复苏API技术支持","")
                                
                            # else:
                            data = await response.text()

                            # data = data.strip()
                            await 接口.发送消息(data,from_wxid)
    except Exception as e:
        print(traceback.format_exc())

        await 接口.发送消息("故障中无法处理",from_wxid)
        return

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000,  log_level="debug")
