# encoding:utf-8
from flask import Flask, request, Response, make_response,render_template
import hashlib
from xml.etree import ElementTree
import time, datetime
from utils.util import xml_rep
import sys
reload(sys)
sys.setdefaultencoding("utf8")
app = Flask(__name__)
EncodingAESKey = "test"
token = 'chc900516'
appid = 'test'
appsecret = 'test'

@app.route('/wechat', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        request_data = request.args
        signature = request_data.get("signature")
        timestamp = request_data.get("timestamp")
        nonce = request_data.get("nonce")
        echostr = request_data.get("echostr")
        auth_data = ''.join(sorted([token, timestamp, nonce]))
        print auth_data, echostr
        encrapy_str = hashlib.sha1(auth_data.encode('utf-8')).hexdigest()
        if encrapy_str == signature:
            print 'Accept'
            return make_response(echostr)
        else:
            print 'Wrong'
    elif request.method == "POST":
        messages = request.stream.read()
        message_parser = ElementTree.fromstring(messages)
        print messages
        msgType = message_parser.find("MsgType").text
        fromUser = message_parser.find("FromUserName").text
        toUser = message_parser.find("ToUserName").text
        #关注后发信息的回复
        if msgType == "text":
            content = message_parser.find("Content").text
            replayText = u'''欢迎关注本微信'''
            response = make_response(xml_rep % (fromUser, toUser, str(int(time.time())), replayText))
            response.content_type = 'application/xml'
            return response
        #关注后的欢迎信息
        elif msgType == "event":
            event = message_parser.find("Event").text
            if event == "subscribe":
                replayText = u'''欢迎关注本微信，这个微信是本人业余爱好所建立，也是想一边学习Python一边玩的东西,现在还没有什么功能，只是弄了个翻译与豆瓣图书查询的小工具，你们有什么好的文章也欢迎反馈给我,我会不定期的分享给大家，输入help查看操作指令'''
                response = make_response(xml_rep % (fromUser, toUser, str(int(time.time())), replayText))
                response.content_type = 'application/xml'
                return response
            if event == "unsubscribe":
                replayText = u'我现在功能还很简单，知道满足不了您的需求，但是我会慢慢改进，欢迎您以后再来'
                response = make_response(xml_rep % (fromUser, toUser, str(int(time.time())), "welcome"))
                response.content_type = 'application/xml'
                return response


@app.route("/",methods=['GET','POST'])
def boot():
    return render_template('boot.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
