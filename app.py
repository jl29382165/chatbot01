#template msg 測試(confirm msg, button,carousel msg,imagecarousel msg)
from flask import Flask, request, abort
from linebot.v3.messaging import (
    MessagingApi, ApiClient, Configuration,
    ReplyMessageRequest, PushMessageRequest, TextMessage, TemplateMessage,
    ButtonsTemplate, PostbackAction, StickerMessage, ImageMessage,
    VideoMessage, AudioMessage, LocationMessage,
    ConfirmTemplate,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    URIAction,
    MessageAction,
    DatetimePickerAction,
    ImagemapMessage,
    ImagemapBaseSize,
    ImagemapVideo,
    ImagemapArea,
    ImagemapExternalLink,
    URIImagemapAction,
)
from linebot.v3.webhooks import MessageEvent, FollowEvent, PostbackEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhook import WebhookHandler
import logging

import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# LINE Bot 設定
configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
api_client = ApiClient(configuration)
messaging_api = MessagingApi(api_client)
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

@app.route("/callback", methods=['GET', 'POST'])
def callback():
    if request.method == 'GET':
        return 'OK', 200
    else:
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)
        try:
            line_handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)
        return 'OK', 200

@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_message = event.message.text
    app.logger.info(f"User message: {user_message}")

    if user_message == '您好':
        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text="您好")]
            )
        )

    elif user_message == 'postback':
        buttons_template = ButtonsTemplate(
            title='Postback Sample',
            text='請選擇一個動作',
            actions=[
                PostbackAction(label='Postback Action', data='postback')
            ]
        )
        template_message = TemplateMessage(
            alt_text='Postback Sample',
            template=buttons_template
        )
        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[template_message]
            )
        )

    elif user_message == '文字':
        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text="這是文字訊息")]
            )
        )

    elif user_message == '表情符號':
    # v3 版本暫時移除 Emoji 功能，或使用純文字替代
        messaging_api.reply_message_with_http_info(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=' 這是表情符號訊息 😆😊😊💯💯💯')]
        )
    )

    elif user_message == '貼圖':
        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[StickerMessage(package_id="446", sticker_id="1988")]
            )
        )

    elif user_message == '圖片':
        url = request.url_root + 'static/logo.png'
        url = url.replace("http", "https")
        app.logger.info("url=" + url)
        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[ImageMessage(original_content_url=url, preview_image_url=url)]
            )
        )

    elif user_message == '影片':
        url = request.url_root + 'static/video.mp4'
        url = url.replace("http", "https")
        preview_url = request.url_root + 'static/video_preview.jpg'  # 需要有預覽圖片
        preview_url = preview_url.replace("http", "https")
        app.logger.info("url=" + url)
        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[VideoMessage(original_content_url=url, preview_image_url=preview_url)]
            )
        )

    elif user_message == '聲音':
        url = request.url_root + 'static/audio.m4a'
        url = url.replace("http", "https")
        app.logger.info("url=" + url)
        duration = 60000  # in milliseconds
        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[AudioMessage(original_content_url=url, duration=duration)]
            )
        )

    elif user_message == '位置':
        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[LocationMessage(
                    title='我的位置',
                    address='台北市',
                    latitude=25.0339637,
                    longitude=121.564468
                )]
            )
        )

    elif user_message == "吃飯":
        confirm_template = ConfirmTemplate(
            text="今天吃飯了嗎？",
            actions=[
                MessageAction(label="是", text="吃飽太好了！"),
                MessageAction(label="否", text="去吃飯！")
            ]
        )
        template_message = TemplateMessage(
            alt_text="Confirm Template",
            template=confirm_template
        )
        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[template_message]
            )
        )

    elif user_message == "按鈕":
        buttons_template = ButtonsTemplate(
            thumbnail_image_url="https://res.cloudinary.com/df0cwejff/image/upload/v1759050641/icecream_xgvbwt.jpg",
            title="請選擇一個選項",
            text="您可點擊以下按鈕：",
            actions=[
                URIAction(label="購買連結", uri="https://br31.tw/"),
                PostbackAction(label="回傳資料", data="ice cream", display_text="傳送中..."),
                MessageAction(label="傳送訊息", text="冰淇淋"),
                DatetimePickerAction(label="選擇時間", data="選擇時間", mode="datetime")
            ]
        )
        template_message = TemplateMessage(
            alt_text="Buttons Template",
            template=buttons_template
        )
        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[template_message]
            )
        )

    elif user_message == "選項輪播":
        carousel_template = CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url="https://res.cloudinary.com/df0cwejff/image/upload/v1759050641/google_cbmtpd.jpg",
                    title="1.google",
                    text="1.google",
                    actions=[
                        URIAction(label="連結到 Google官網", uri="https://www.google.com"),
                        MessageAction(label="傳送訊息", text="1.google")
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://res.cloudinary.com/df0cwejff/image/upload/v1759050640/apple_px8pwf.jpg",
                    title="2.apple",
                    text="2.apple",
                    actions=[
                        URIAction(label="連結到 apple官網", uri="https://www.apple.com"),
                        MessageAction(label="傳送訊息", text="2.apple")
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://res.cloudinary.com/df0cwejff/image/upload/v1759050640/aws_hzinuh.jpg",
                    title="3.amazon",
                    text="3.amazon",
                    actions=[
                        URIAction(label="連結到 amazon官網", uri="https://www.amazon.com"),
                        MessageAction(label="傳送訊息", text="3.amazon官網")
                    ]
                ),
                 CarouselColumn(
                    thumbnail_image_url="https://res.cloudinary.com/df0cwejff/image/upload/v1759050641/msft_yx6i4y.jpg",
                    title="4.microsoft",
                    text="4.microsoft",
                    actions=[
                        URIAction(label="連結到 microsoft官網", uri="https://www.microsoft.com"),
                        MessageAction(label="傳送訊息", text="4.microsoft官網")
                    ]
                )
            ]
        )
        template_message = TemplateMessage(
            alt_text="Carousel Template",
            template=carousel_template
        )
        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[template_message]
            )
        )

    elif user_message == "圖片輪播":
        image_carousel_template = ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url="https://res.cloudinary.com/df0cwejff/image/upload/v1759050641/google_cbmtpd.jpg",
                    action=URIAction(label="google", uri="https://www.google.com")
                ),
                ImageCarouselColumn(
                    image_url="https://res.cloudinary.com/df0cwejff/image/upload/v1759050640/apple_px8pwf.jpg",
                    action=URIAction(label="apple", uri="https://www.apple.com")
                ),
                ImageCarouselColumn(
                    image_url="https://res.cloudinary.com/df0cwejff/image/upload/v1759050640/aws_hzinuh.jpg",
                    action=URIAction(label="amazon", uri="https://www.amazon.com")
                )
            ]
        )
        template_message = TemplateMessage(
            alt_text="Image Carousel Template",
            template=image_carousel_template
        )
        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[template_message]
            )
        )

    elif event.message.text == 'imagemap':
        imagemap_message = ImagemapMessage(
            base_url='https://raw.githubusercontent.com/jl29382165/imagemap/main', 
            alt_text='This is an imagemap',
            base_size=ImagemapBaseSize(height=1040, width=1040),
            actions=[
                URIImagemapAction(
                    link_uri='https://www.google.com/',
                    area=ImagemapArea(
                        x=4, y=2, width=504, height=510
                    )
                ),
                URIImagemapAction(
                    link_uri='https://translate.google.com.tw/?hl=zh-TW&sl=en&tl=zh-TW&op=translate',
                    area=ImagemapArea(
                        x=508, y=0, width=532, height=512
                    )
                ),
                URIImagemapAction(
                    link_uri='https://docs.google.com/spreadsheets/d/14HF5TGlxGc-Zs_hbjNC7m1KWRkg-tYmvX2AnOW_p13Q/edit?usp=drive_link',
                    area=ImagemapArea(
                        x=4, y=516, width=504, height=524
                    )
                ),
                URIImagemapAction(
                    link_uri='https://www.youtube.com/watch?v=bInfKZtQwFQ',
                    area=ImagemapArea(
                        x=514, y=518, width=524, height=522
                    )
                )
            ]
        )
        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[imagemap_message]
            )
        )


@line_handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    app.logger.info(f"User {user_id} followed the bot")
    try:
        messaging_api.push_message_with_http_info(
            PushMessageRequest(
                to=user_id,
                messages=[TextMessage(text="感謝你加入好友！輸入 'postback' 試試看按鈕功能。")]
            )
        )
    except Exception as e:
        app.logger.error(f"Failed to send follow message: {e}")

@line_handler.add(PostbackEvent)
def handle_postback(event):
    postback_data = event.postback.data
    app.logger.info(f"Postback data: {postback_data}")
    try:
        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=f"你觸發了 Postback 動作，資料：{postback_data}")]
            )
        )
    except Exception as e:
        app.logger.error(f"Failed to send postback response: {e}")

if __name__ == "__main__":
    app.run(port=5001, debug=True)
