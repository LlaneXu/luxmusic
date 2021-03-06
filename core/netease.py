# -*- coding: utf-8 -*-
"""
@Time    : 2020-03-06 15:16
@Author  : Lei Xu
@Email   : Llane_xu@outlook.com
@File    : netease.py

Description:

Update:

Todo:


"""
# system import

# 3rd import

# self import

# module level variables here

# Create your models here.


import os
import json
import logging
import requests
import binascii
import Crypto.Cipher.AES as AES
import Crypto.PublicKey.RSA as RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
from .response import ResponseException

# to avoid useless re-calculate
KEY = None
SEC_KEY = None

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.122 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "x-real-ip": "211.161.244.70",
    # "Cookie": "NMTID=00OmYrUWn7kjnrMiEghv8VtKW-mDz8AAAF0wg82nQ; csrftoken=MfSAeFq1h34wVW5ZZkg5O2mydtQzEPDwK5L8giRb0AxzJ1K9n6pVdfbznJIdWeJg",
    "Referer": "https://music.163.com",
}

def _create_aes_key(size):
    """
    some pares
    kdlvdwn5JIeUt4O7
    0e36b7422318fa9b02dd2313985318bc2ef3d612755f428787e6446d4c0288a235fd05a65e7ab1da63d5f1e949701e43831111cd161c77c266888a5158961adf8fd809d9e99a755f1cbc2d96053988df3bfd211bdece6ba5b6a46bacad53bf0698662b7a6b2888916d043d8e78ef5ba70b53aa82ad06c5a3a0027dc9ae083eb2

    qY9moAm5Zqm5i625
    bd2c1184e29d287d845ef015bd1e520aff3a5d87645f7b55911bb5a2c9694988b355b14ad2e7ca576c5fb618af73de2439f6291644cc7e54b18bdb810221d73a0aa34e446efb1b6307198f50602f102f0db5a94ad57afcd584315d6b1b2cc651faa70e60fd0b64580c7e4ed742e5fa74f8974da3e684eb59a143029621e665ea


    oHYdtzgEZpAn7JFZ
    params: 9aPfw9boX8hYX/Tfjx2BckXhN1tjRseukd8ON7iK3tCODKwUuCyTlUUIWHgErNWxhlDrnvamDQS4TIPS50M6n29+aoVjgmf3I3Ixf82VJKPRMymRRfBKdADF6K9eV6Y5z3xqkxF+5J1KVLvO6QC1KQ==
    0a1ef21771fe37dcf6c3e22ef8e3f844915efe1a6b0a945a73638e3e9e877f6d9f4c154059a00a3ced2f5b0fdc5c3f9b24f525f8653d7062ebd38b859ffab8add55cd19ebd93482aa15939caf5c7b2466afe1f5b020df681b71b93faadd8bab18bf8a829cffc52adb1941c366fca0a49d9b0e2a4ac3465dacab999ed0c467cb1

    :param size:
    :return:
    """
    # return 'oHYdtzgEZpAn7JFZ'
    global KEY
    if not KEY:
        KEY = (''.join([hex(b)[2:] for b in os.urandom(size)]))[0:16]
    return KEY


def _aes_encrypt(msg, key):
    # 如果不是16的倍数则进行填充
    padding = 16 - len(msg) % 16
    # 这里使用padding对应的单字符进行填充
    msg += padding * chr(padding)
    msg = msg.encode('ascii')
    # 用来加密或者解密的初始向量(必须是16位)
    iv = b'0102030405060708'
    # AES加密
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 加密后得到的是bytes类型的数据
    encrypt_bytes = cipher.encrypt(msg)
    # 使用Base64进行编码,返回byte字符串
    encode_string = base64.b64encode(encrypt_bytes)
    # 对byte字符串按utf-8进行解码
    encrypt_text = encode_string.decode('ascii')
    # 返回结果
    return encrypt_text


def _rsa_encrypt(text):
    global KEY
    global SEC_KEY
    if not KEY:
        KEY = text
    if not SEC_KEY:
        e = '010001'
        n = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615' \
            'bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf' \
            '695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46' \
            'bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b' \
            '8e289dc6935b3ece0462db0a22b8e7'

        reverse_text = text[::-1]
        reverse_byte = reverse_text.encode('ascii')
        sec_key = int(reverse_byte.hex(), 16) ** int(e, 16) % int(n, 16)
        sec_key = format(sec_key, 'x')
        logging.info("sec_key:\n%s" % sec_key.zfill(256))

        pub_key = RSA.construct((int(n, 16), int(e, 16)))
        encryptor = PKCS1_OAEP.new(pub_key)
        encrypt_text = encryptor.encrypt(binascii.hexlify(reverse_text.encode('ascii')))
        logging.info("encrypt_text:\n%s" % encrypt_text.hex())

        SEC_KEY = sec_key.zfill(256)
    return SEC_KEY


def encrypt_request(data):
    text = json.dumps(data)
    logging.info("raw:\n%s" % text)
    first_aes_key = b'0CoJUm6Qyw8W8jud'
    second_aes_key = _create_aes_key(16)
    enc_text = _aes_encrypt(
        _aes_encrypt(text, first_aes_key),
        second_aes_key.encode('ascii'))
    enc_aes_key = _rsa_encrypt(second_aes_key)
    payload = {
        'params': enc_text,
        'encSecKey': enc_aes_key,
    }
    # logging.warning(payload)
    return payload


def get_url_by_song_id(id):
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) "
    #                   "AppleWebKit/537.36 (KHTML, like Gecko) "
    #                   "Chrome/80.0.3987.122 Safari/537.36",
    #     "Content-Type": "application/x-www-form-urlencoded",
    #     "x-real-ip": "211.161.244.70",
    # }
    url = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="
    query = {
        "ids": "[%s]" % id,
        "level": "standard",
        "encodeType": "aac",
        "csrf_token": ""
    }

    response = requests.post(url, headers=HEADERS, data=encrypt_request(query))
    ret_json = response.json()
    url = ret_json["data"][0].get("url")
    return url


def request(options):
    response = _request(options)

    ret = response.json()
    if ret["code"] != 200:
        raise ResponseException(ret)
    return ret

def _request(options):
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) "
    #                   "AppleWebKit/537.36 (KHTML, like Gecko) "
    #                   "Chrome/80.0.3987.122 Safari/537.36",
    #     "Content-Type": "application/x-www-form-urlencoded",
    #     "x-real-ip": "211.161.244.70",
    #     # "Cookie": "NMTID=00OmYrUWn7kjnrMiEghv8VtKW-mDz8AAAF0wg82nQ; csrftoken=MfSAeFq1h34wVW5ZZkg5O2mydtQzEPDwK5L8giRb0AxzJ1K9n6pVdfbznJIdWeJg",
    #     "Referer": "https://music.163.com",
    # }
    method = options.get("method", "POST")
    headers = options.get("headers", HEADERS)
    url = options.get("url")
    data = options.get("data", {})
    return requests.request(method, url, headers=headers, data=encrypt_request(data))


def get_artist_info(artist_id):
    """
    https://music.163.com/weapi/v1/artist/${query.id}
    post
    encrypted request
    data:
    {
        artist: {
            id: xx,
            name: xx,
        },
        hotSongs: [{
            id: xx,
            name: xx,
            ar: [{
                id: xx,
                name: xx,
            }],
            al: {
                id: xx,
                name: xx,
                picUrl: 'https://p2.music.126.net/PcJq6i7zMcPgudejdn1yeg==/109951163256302356.jpg',
            }
        }]
    }
    :return:
    """
    options = {
        "url": "https://music.163.com/weapi/v1/artist/%s" % artist_id,
        "data": {
            # "id": artist_id,
            # "csrf_token": ""
        }
    }
    response = _request(options)
    res = response.json()
    # save cookies for cookies verify later used in other api
    # self.cookies = response.cookies
    return res.get("artist", {}), res.get("hotSongs",[])


def get_comment(song_id, page=1, cursor=-1):
    """
    http://music.163.com/api/v1/resource/comments/R_SO_4_{song_id}?limit={limit}&offset={offset}
    :return:
    {
        code: 200,
        data: {
            comments: [{
                beReplied:[{
                    user: {
                        userId: xx,
                        nickname: xx,
                    }
                    beRepliedCommentId: xx,
                    content: xx
                }],
                user: {
                    userId: xx,
                    nickname: xx,
                },
                commentId: xx,
                content: xxx,
            }],
            totalCount: xxx,
        }
    }
    """
    options = {
        "url": "https://music.163.com/weapi/comment/resource/comments/get?csrf_token=",
        "data": {
            "rid": "R_SO_4_%s" % song_id,
            "threadId": "R_SO_4_%s" % song_id,
            # "offset": (page-1)*100,
            "pageNo": page,
            "pageSize": 100,
            "orderType": 2,
            "cursor": cursor,
        }
    }
    res = request(options)
    data = res["data"]
    return data.get("comments", []), data["totalCount"], data["cursor"]


def get_user_info(user_id):
    """
    https://music.163.com/api/v1/user/detail/{user_id}
    :return:
    {
        profile: {
            userId: xx,
            nickname: xx,
            gender: 0-unknown, 1-male, 2-female,
            birthday: ms timestamp, maybe a negative number
            city: may be empty
        }
    }
    """
    url = "https://music.163.com/api/v1/user/detail/%s" % (
        user_id
    )
    res = requests.get(url, headers=HEADERS).json()
    return res.get("profile", {})
