from django.shortcuts import render

# Create your views here.

# 這邊就是撰寫LINE Bot接收訊息後，所要執行的運算邏輯，
# 這邊先以使用者發送什麼訊息，就回覆什麼訊息為例，來測試Django應用程式(APP)能夠成功的和LINE頻道(Channel)進行連結

# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
 
from .scraper import IFoodie

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
 
# @csrf_exempt
# def callback(request):
 
#     if request.method == 'POST':
#         signature = request.META['HTTP_X_LINE_SIGNATURE']
#         body = request.body.decode('utf-8')
 
#         try:
#             events = parser.parse(body, signature)  # 傳入的事件
#             print(events)
#         except InvalidSignatureError:
#             return HttpResponseForbidden()
#         except LineBotApiError:
#             return HttpResponseBadRequest()
 
#         for event in events:
#             if isinstance(event, MessageEvent):  # 如果有訊息事件
                
#                 # line_bot_api.reply_message(  # 回復傳入的訊息文字
#                 #     event.reply_token,
#                 #     TextSendMessage(text=event.message.text)
#                 # )

#                 food = IFoodie(event.message.text) # 使用者傳入的文字

#                 line_bot_api.reply_message( # 回應前五間最高人氣且營業中的餐廳訊息文字
#                     event.reply_token,
#                     TextSendMessage(text=food.scrape())
#                 )

#         return HttpResponse()
#     else:
#         return HttpResponseBadRequest()

@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
            # print(events)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
 
            if isinstance(event, MessageEvent):  # 如果有訊息事件
 
                food = IFoodie(event.message.text)  #使用者傳入的訊息文字
                # print('傳入地區訊息', food)
 
                line_bot_api.reply_message(  # 回應前五間最高人氣且營業中的餐廳訊息文字
                    event.reply_token,
                    TextSendMessage(text=food.scrape())
                    #  TextSendMessage(text=event.message.text)
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()