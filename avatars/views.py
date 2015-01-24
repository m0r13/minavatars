import io
import os
import time
import urllib

from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import render

from PIL import Image


def get_avatar(gen_func, cache_name, request, user, size):
    sizes = getattr(settings, "AVATARS_SIZES", None)
    if sizes is None:
        return HttpResponse("Available sizes are not set!")
    cache_root = getattr(settings, "AVATARS_CACHE_DIR", None)
    if cache_root is None:
        return HttpResponse("Cache dir is not set!")
    cache_expiry = getattr(settings, "AVATARS_CACHE_EXPIRY", None)
    if cache_expiry is None:
        return HttpResponse("Cache expiry is not set!")
    
    try:
        size = int(size)
        if not size in sizes and sizes != []:
            raise ValueError
    except ValueError:
        return HttpResponse("Invalid size '%s'!" % size)
    
    # get url of user skin and path to avatar cache file
    url = "http://skins.minecraft.net/MinecraftSkins/%s.png" % user
    cache_dir = os.path.join(cache_root, cache_name)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    cache_file = os.path.join(cache_dir, "%s_%d.png" % (user, size))
    
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
    avatar = gen_func(skin)
    avatar = avatar.resize((avatar.size[0]*size, avatar.size[1]*size))
    avatar.save(cache_file)
    
    # return generated avatar
    return HttpResponse(open(cache_file, "rb").read(), content_type="image/png")

def gen_player_head(skin):
    # head
    head = skin.crop((8, 8, 16, 16))
    # hat
    hat = skin.crop((40, 8, 40+8, 8+8))
    head.paste(hat, (0, 0), hat)
    return head

def head(request, user, size):
    return get_avatar(gen_player_head, "head", request, user, size)

def gen_player_body(skin):
    body = Image.new("RGBA", (16, 32))
    # head
    body.paste(gen_player_head(skin), (4, 0))
    # body
    body.paste(skin.crop((20, 20, 20+8, 20+12)), (4, 8))
    # left and right arm
    body.paste(skin.crop((44, 20, 44+4, 20+12)), (0, 8))
    body.paste(skin.crop((47, 20, 47+4, 20+12)), (12, 8))
    # left and right leg
    body.paste(skin.crop((4, 20, 4+4, 20+12)), (4, 20))
    body.paste(skin.crop((8, 20, 8+4, 20+12)), (8, 20))
    return body

def body(request, user, size):
    return get_avatar(gen_player_body, "body", request, user, size)
