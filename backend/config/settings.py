"""
Настройки Django для Fixam.

Всё, что зависит от окружения (секреты, адрес базы, debug), берётся из
переменных окружения через django-environ. Локально их можно положить в
файл .env в корне репозитория (см. .env.example), в Docker они приходят
из docker-compose.yml, на сервере — из окружения процесса.
"""

from pathlib import Path

import environ

# BASE_DIR = папка backend/ (там лежит manage.py).
# BASE_DIR.parent = корень репозитория (там лежит .env).
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent

env = environ.Env(
    # имя переменной = (тип, значение по умолчанию, если переменной нет)
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)

# Читаем .env, если он есть. Если файла нет (например, в Docker или на сервере,
# где всё уже в окружении) — просто ничего не делает, ошибки не будет.
environ.Env.read_env(ROOT_DIR / ".env")

# ---------------------------------------------------------------------------
# Базовое
# ---------------------------------------------------------------------------

# env("X") без default упадёт с ошибкой, если переменной нет.
# Для SECRET_KEY это правильно: лучше не запуститься, чем запуститься с пустым ключом.
SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Свои приложения будут добавляться сюда по мере появления:
    # "apps.accounts",
    # "apps.content",
    # ...
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise раздаёт статику (css/js) прямо из Django, без nginx.
    # Должен стоять сразу после SecurityMiddleware.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Общие шаблоны проекта (base.html и т.п.) — в backend/templates/.
        # Шаблоны конкретных приложений — в <app>/templates/<app>/ (APP_DIRS=True).
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ---------------------------------------------------------------------------
# База данных
# ---------------------------------------------------------------------------

# Одна переменная DATABASE_URL вместо пяти (host/port/user/pass/name).
# Формат: postgres://user:password@host:port/dbname
# env.db() сам разбирает URL и собирает словарь для Django.
# Если переменной нет — падаем на SQLite, чтобы можно было быстро что-то
# проверить без Postgres. Но реальная разработка — на Postgres, как и прод.
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
    ),
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Пароли
# ---------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# Локализация
# ---------------------------------------------------------------------------

# Русский интерфейс админки, русские сообщения об ошибках форм.
LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

# В базе всё хранится в UTC, в шаблонах показывается по TIME_ZONE.
USE_TZ = True

# ---------------------------------------------------------------------------
# Статика и медиа
# ---------------------------------------------------------------------------

STATIC_URL = "static/"
# Куда collectstatic складывает все статические файлы для раздачи.
STATIC_ROOT = BASE_DIR / "staticfiles"

# Файлы, загруженные пользователями (картинки к заданиям и т.п.).
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # WhiteNoise сжимает статику и добавляет хеш в имя файла
        # (style.css -> style.abc123.css), чтобы браузер не кэшировал старую версию.
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ---------------------------------------------------------------------------
# Почта
# ---------------------------------------------------------------------------

# Пока писем нет — выводим их в консоль. Когда появится восстановление пароля,
# заменим на настоящий SMTP через переменные окружения.
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}
