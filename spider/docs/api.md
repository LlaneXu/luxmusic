#1. 基本信息
##1.1. 接口规则
`POST` 传递

`body` 为： `params={params}&encSecKey={encSecKey}`

`params`: 2重AES密文

`encSecKey`: AES秘钥的RSA加密

典型样例：
> 秘钥1(固定): `0CoJUm6Qyw8W8jud`
>
> 秘钥2: `kdlvdwn5JIeUt4O7` 
>
> params: `+BI8PkqY5weQYllAgB9dF7xMaS6BAo/1TJbncxfusuTDOQEmE3fD2jLAdtEWCCjyUtwiXkACu/zFynIR9DZMWcEc6zQZyxIAQuB0wKJ55jFfRiLFxPLWE52mKMnDAfvDqpl95I2FiYG7d6dzUTrAmQ==`
>
>encSecKey: `0e36b7422318fa9b02dd2313985318bc2ef3d612755f428787e6446d4c0288a235fd05a65e7ab1da63d5f1e949701e43831111cd161c77c266888a5158961adf8fd809d9e99a755f1cbc2d96053988df3bfd211bdece6ba5b6a46bacad53bf0698662b7a6b2888916d043d8e78ef5ba70b53aa82ad06c5a3a0027dc9ae083eb2`

 
##1.2. 加密规则
###1.2.1 aes 加密
加密规则：CBC

向量： `0102030405060708`

秘钥： 固定秘钥 `0CoJUm6Qyw8W8jud`

###1.2.2. param加密流程
1. param -> text
2. text + 固定秘钥  AES加密
3. 再与 16位随机秘钥 AES加密

### 1.2.3. RSA加密

#2. 接口
##2.1. 获取歌手
### api
```json
https://music.163.com/weapi/artist/identity?csrf_token=
```
##2.2. 获取歌曲信息
### api
```angular2
https://music.163.com/weapi/v3/song/detail?csrf_token=
```
### params

```json
{
 "c":"[{"id":"547606280"}]",
 "csrf_token":"",
}
```

```json
{
  "songs": [
    {
      "name": "如果你也听说 (Live)",
      "id": 29005677,
      "pst": 0,
      "t": 0,
      "ar": [
        {
          "id": 10559,
          "name": "张惠妹",
          "tns": [],
          "alias": []
        }
      ],
      "alia": [],
      "pop": 95.0,
      "st": 0,
      "rt": null,
      "fee": 8,
      "v": 27,
      "crbt": null,
      "cf": "",
      "al": {
        "id": 2975319,
        "name": "STAR LIVE庆功演唱会",
        "picUrl": "https://p1.music.126.net/1Fg4WKSjj0dTSElhi_KFhg==/109951163244872785.jpg",
        "tns": [],
        "pic_str": "109951163244872785",
        "pic": 109951163244872785
      },
      "dt": 321549,
      "h": {
        "br": 320000,
        "fid": 0,
        "size": 12866886,
        "vd": -1.48
      },
      "m": {
        "br": 160000,
        "fid": 0,
        "size": 6433973,
        "vd": -1.04
      },
      "l": {
        "br": 96000,
        "fid": 0,
        "size": 3860807,
        "vd": -1.08
      },
      "a": null,
      "cd": "1",
      "no": 10,
      "rtUrl": null,
      "ftype": 0,
      "rtUrls": [],
      "djId": 0,
      "copyright": 2,
      "s_id": 0,
      "mark": 0,
      "originCoverType": 0,
      "rurl": null,
      "mst": 9,
      "cp": 13009,
      "mv": 5570742,
      "rtype": 0,
      "publishTime": 1190217600007
    }
  ],
  "privileges": [
    {
      "id": 29005677,
      "fee": 8,
      "payed": 0,
      "st": 0,
      "pl": 128000,
      "dl": 0,
      "sp": 7,
      "cp": 1,
      "subp": 1,
      "cs": false,
      "maxbr": 999000,
      "fl": 128000,
      "toast": false,
      "flag": 0,
      "preSell": false,
      "playMaxbr": 999000,
      "downloadMaxbr": 999000
    }
  ],
  "code": 200
}
```