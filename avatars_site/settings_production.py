from settings import *

# overriden later por supuesto
SECRET_KEY = "ls$m0yt4pb79lh_pmq$ys*^32qp9on2rcqt2izp%q8=)d-4gut"

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# if AVATAR_SIZES is an empty array, all sizes are allowed
AVATARS_SIZES = [1, 2, 4, 8]
AVATARS_CACHE_DIR = os.path.join(BASE_DIR, "cache")
AVATARS_CACHE_EXPIRY = 24*60*60 # 24h
