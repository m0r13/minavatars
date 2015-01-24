import io
import os
import urllib
import time

from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import render

from PIL import Image


def gen_player_head(skin):
    return skin.crop((8, 8, 16, 16))

def head(request, size, user):
    cache_root = getattr(settings, "AVATARS_CACHE_DIR", None)
    if cache_root is None:
        return HttpResponse("Cache dir is not set!")
    cache_expiry = getattr(settings, "AVATARS_CACHE_EXPIRY", None)
    if cache_expiry is None:
        return HttpResponse("Cache expiry is not set!")
    
    try:
        size = int(size)
    except ValueError:
        return HttpResponse("Invalid size '%s'!" % size)
    
    # get url of user skin and path to avatar cache file
    url = "http://skins.minecraft.net/MinecraftSkins/%s.png" % user
    cache_dir = os.path.join(cache_root, "head")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    cache_file = os.path.join(cache_dir, "%s.png" % user)
    
    # check if avatar is already generated in cache
    if os.path.exists(cache_file):
        # return if it's not expired yet
        if os.stat(cache_file).st_mtime > time.time() - cache_expiry:
            return HttpResponse(open(cache_file, "rb").read(), content_type="image/png")
    
    # otherwise try to generate the avatar
    # first of all get the skin
    skin = None
    try:
        f = urllib.request.urlopen(url)
        buf = io.BytesIO(f.read())
        skin = Image.open(buf)
    except urllib.request.HTTPError as e:
        # if there is no skin, just use default steve skin for now
        skin = Image.open(os.path.join(os.path.dirname(__file__), "steve.png"))
    
    # now generate avatar and save it
    avatar = gen_player_head(skin)
    avatar.save(cache_file)
    
    # return generated avatar
    return HttpResponse(open(cache_file, "rb").read(), content_type="image/png")
