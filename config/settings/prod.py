import environ

from .base import *  # base 에 있는 모든 내용을 사용한다. ALLOWED_HOSTS 만 따로 쓴다.

ALLOWED_HOSTS = ["127.0.0.1"]  # AWS 이면 고정 아이피
STATIC_ROOT = BASE_DIR / 'static'
# 이유는 STATIC_ROOT가 설정된 경우 STATICFILES_DIRS 리스트에 STATIC_ROOT와 동일한 디렉터리가 포함되어 있으면
# 서버 실행 시 다음과 같은 오류가 발생
STATICFILES_DIRS = []

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': '3306',
    }
}
