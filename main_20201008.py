from flask import Flask, request, abort
import os
import json

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage)

app = Flask(__name__)
app.debug = False

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text

    if text == '写真下見':
        confirm_template = ConfirmTemplate(text='LINE下見ですね。こちらはすでに日通にご連絡いただいた方専用となります。　日通にご連絡いただいていますか？', 
        actions=[
            MessageAction(label='はい', text='はい'),
            MessageAction(label='いいえ', text='いいえ'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text =='はい':
            line_bot_api.reply_message(
                event.reply_token, [
                TextSendMessage(text='日通担当者とお打合せ開始済みの場合は、お客様のフルネームをご記入後、お写真をご送付ください。')
                ]
            )
    elif text == 'いいえ':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='新規のお問い合わせはこちらからご連絡ください。', title='新規お問い合わせ', actions=[
                URIAction(label='新規お問い合わせ', uri='https://www.nittsu.co.jp/form_gl/php/agree.php?ID=moving_sg'),
            ]), 
        ])
        template_message = TemplateSendMessage(
            alt_text='新規お問い合わせ', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
#    elif text == '引越準備の情報':
#        carousel_template = CarouselTemplate(columns=[
#            CarouselColumn(text='以下の選択肢より、お選びください。', title='引越準備の情報', actions=[
#                {"type":"uri", "label":"１. 日本向け　禁制品一覧", "uri":'https://www.nipponexpress.com/moving/sg/doc/flow-prohibiteditems-list.pdf'}, 
#                {"type":"uri", "label":'２. 日本向け　お荷物別注意点', "uri":'https://www.nipponexpress.com/moving/sg/doc/flow-luggage_attention.pdf'}, 
#                {"type":"message", "label":"３. 日本向け　所要日数", "text":"３.　日本向け　所要日数"}
#                {"type":"uri", "label":'４．お客様事前梱包について', "uri":'https://www.nipponexpress.com/moving/sg/doc/flow-customer-packing.pdf'}, 
#                {"type":"uri", "label":'５．仕分けの方法について', "uri":'https://www.nipponexpress.com/moving/sg/doc/flow-sorting.pdf'}, 
#                {"type":"message", "label":"６．日本人会への寄付品について", "text":"６．日本人会への寄付品について"},
#                {"type":"uri", "label":'７．別送品申告について', "uri":'https://www.nipponexpress.com/moving/sg/doc/flow-unaccompanied-baggage-personal-effects.pdf'}
#            ]), 
#        ])
#        template_message = TemplateSendMessage(
#            alt_text='Carousel alt text', template=carousel_template)
#        line_bot_api.reply_message(event.reply_token, template_message)

    elif text == '引越準備の情報':
        bubble_string = """
{
    "type": "bubble",
    "hero": {
      "type": "image",
      "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "cover",
      "action": {
        "type": "uri",
        "label": "Line",
        "uri": "https://linecorp.com/"
      }
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "お問い合わせ内容",
          "size": "xl",
          "weight": "bold"
        },
        {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "margin": "lg",
          "contents": [
            {
              "type": "box",
              "layout": "baseline",
              "spacing": "sm",
              "contents": [
                {
                  "type": "text",
                  "text": "以下の選択肢より、お選びください。",
                  "flex": 5,
                  "size": "sm",
                  "color": "#666666",
                  "wrap": true
                }
              ]
            }
          ]
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "vertical",
      "flex": 0,
      "spacing": "sm",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "【日本向け】禁制品一覧",
            "uri": "https://www.nipponexpress.com/moving/sg/doc/flow-prohibiteditems-list.pdf"
          },
          "style": "primary"
        },
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "【日本向け】お荷物別注意点",
            "uri": "https://www.nipponexpress.com/moving/sg/doc/flow-luggage_attention.pdf"
          },
          "style": "primary"
        },
        {
          "type": "button",
          "action": {
            "type": "message",
            "label": "【日本向け】所要日数",
            "text": "【日本向け】所要日数"
          },
          "style": "primary"
        },
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "お客様事前梱包について",
            "uri": "https://www.nipponexpress.com/moving/sg/doc/flow-customer-packing.pdf"
          },
          "style": "primary"
        },
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "仕分けの方法について",
            "uri": "https://www.nipponexpress.com/moving/sg/doc/flow-sorting.pdf"
          },
          "style": "primary"
        },
        {
          "type": "button",
          "action": {
            "type": "message",
            "label": "日本人会への寄付品について",
            "text": "日本人会への寄付品について"
          },
          "style": "primary"
        },
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "別送品申告について",
            "uri": "https://www.nipponexpress.com/moving/sg/doc/flow-unaccompanied-baggage-personal-effects.pdf"
          },
          "style": "primary"
        },
        {
          "type": "spacer",
          "size": "sm"
        }
      ]
    }
  }
        """
        message = FlexSendMessage(alt_text="hello", contents=json.loads(bubble_string))
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif text =='【日本向け】所要日数':
            line_bot_api.reply_message(
                event.reply_token, [
                TextSendMessage(text='シンガポールから日本の所要日数目安は下記となります。'),
                TextSendMessage(text='船便：1ヶ月～1か月半　\n航空便：2週間前後'),
                TextSendMessage(text='※北海道、沖縄、離島は上記に加え数日いただく場合がございます。　\n※船舶、航空便の遅延により、上記よりお時間を要する場合がございます。')
                ]
            )
    elif text =='日本人会への寄付品について':
            line_bot_api.reply_message(
                event.reply_token, [
                TextSendMessage(text='シンガポール日通では、日本人会への寄付品を、お引越時にお受け取りし、日本人会へお運びしております。'),
                TextSendMessage(text='・不要な本（新品、中古品）　\n・日用品（未使用のみ）　\n・お洋服（未使用のみ）'),
                TextSendMessage(text='ご自宅1か所にまとめていただき、お引越当日、寄付品がある旨、スタッフへお申しつけ下さい。')
                ]
            )

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)) 

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)