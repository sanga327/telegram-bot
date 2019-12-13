import requests
from decouple import config

url = 'https://translation.googleapis.com/language/translate/v2'
key = config('GOOGLE_TOKEN')

data = {
    'q':'엄마 판다는 새끼가 있네',
    'source':'ko',  # 한국어에서
    'target':'en'   # 바꿀 언어: 영어
}

result = requests.post(f'{url}?key={key}',data).json()

print(result)
