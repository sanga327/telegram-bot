from flask import Flask, render_template, request
from decouple import config
import requests, pprint, random, html
 
app = Flask(__name__)

# 텔레그램 API
url = 'https://api.telegram.org'
token = config('TELEGRAM_BOT_TOKEN') 
chat_id = config('CHAT_ID')

# 구글 API
google_url = 'https://translation.googleapis.com/language/translate/v2'
google_key = config('GOOGLE_TOKEN')





@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route(f'/{token}',methods=['POST'])
def telegram():
    # 텔레그램이 보내주는 데이터 구조 확인
    pprint.pprint(request.get_json())
    # 사용자 아이디, 메시지 추출
    chat_id = request.get_json().get('message').get('from').get('id')
    message = request.get_json().get('message').get('text')

    # 사용자가 로또라고 입력하면 로또 번호 6개 돌려주기
    if message =='로또':
        result = random.sample(range(1,46), 6)

    # 사용자가 /번역 이라고 말하면 한 - 영 번역 제공
    elif message[:4] == '/번역 ':
        data = {
            'q':message[4:],
            'source':'ko',
            'target':'en'
        }
        # 1. 구글 api 번역 요청
        response = requests.post(f'{google_url}?key={google_key}',data).json()
        # 2. 번역 결과 추출 -> 답장 변수에 저장
        result = html.unescape(response['data']['translations'][0]['translatedText'])

    # 그 외의 경우엔 메아리
    else: 
        result = message
    
    # 텔레그램 API에 답장 전송 요청
    requests.get(f'{url}/bot{token}/sendMessage?chat_id={chat_id}&text={result}')

    return '',200

# https://api.telegram.org/bot825429122:AAHwXef2Irm_Y_S2ePqoJZocJ7loKtaxTJQ/setWebhook?url=https://f93190e6.ngrok.io/825429122:AAHwXef2Irm_Y_S2ePqoJZocJ7loKtaxTJQ




@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/send')
def send():
    # 1. 사용자가 입력한 데이터 받아오기 (플라스크 기능)
    text = request.args.get('message')

    # 2. 텔레그램 API 메시지 전송 요청 보내기 (파이썬 모듈)
    requests.get(f'{url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
    
    return '메시지 전송 완료! :)'

# 반드시 파일 최하단에 위치시킬 것! 
if __name__ == '__main__':
 	app.run(debug=True)
    