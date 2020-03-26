# 酷狗
https://www.cnblogs.com/daxiangxm/p/
https://github.com/ecitlm/Kugou-apikugou_music_api.html
## 1. 获取歌曲下载地址
`https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash=825B158767D706B7C534C066420640BC`

> data.is_free_part
> 表示是否试听内容 1-是，0-否
```json
{
    "status":1,
    "err_code":0,
    "data":{
        "hash":"825B158767D706B7C534C066420640BC",
        "timelength":180950,
        "filesize":2895784,
        "audio_name":"华晨宇 - 水手 (Live)",
        "have_album":1,
        "album_name":"王牌对王牌第五季 第4期",
        "album_id":"36620615",
        "img":"http://imge.kugou.com/stdmusic/20200313/20200313150404133973.jpg",
        "have_mv":0,
        "video_id":0,
        "author_name":"华晨宇",
        "song_name":"水手 (Live)",
        "lyrics":"[id:$00000000]
[ar:华晨宇]
[ti:水手]
[by:yangbin_karakal]
[00:00.00]水手 (Live) - 华晨宇
[00:01.58]词：郑智化
[00:01.70]曲：陈志远
[00:01.85]编曲：SIMON MONGTRISON/崔迪
[00:02.04]原唱：郑智化
[00:02.19]制作人：崔迪
[00:02.36]吉他：金冬昱
[00:02.52]音乐总监：楼恩奇
[00:04.44]他说风雨中这点痛 算什么
[00:14.29]他说风雨中这点痛 算什么
[00:37.13]苦涩的沙 吹痛脸庞的感觉
[00:41.35]像父亲的责骂母亲的哭泣
[00:44.04]永远难忘记
[00:46.34]年少的我 喜欢一个人在海边
[00:51.31]卷起裤管光着脚丫踩在沙滩上
[00:56.38]总是幻想海洋的尽头有另一个世界
[01:01.15]总是以为勇敢的水手是真正的男儿
[01:06.08]总是一副弱不禁风孬种的样子
[01:10.77]在受人欺负的时候总是听见水手说
[01:18.05]他说风雨中这点痛算什么
[01:22.51]擦干泪不要怕
[01:25.13]至少我们还有梦
[01:27.36]他说风雨中这点痛算什么
[01:32.23]擦干泪不要问
[01:34.86]为什么
[01:45.41]总是拿着微不足道的成就来骗自己
[01:49.97]总是莫名其妙感到一阵的空虚
[01:55.03]总是靠一点酒精的麻醉才能够睡去
[01:59.74]在半睡半醒之间仿佛听见水手说
[02:05.62]嘿 痛算什么
[02:09.37]擦干泪不要怕
[02:11.62]至少我们还有梦
[02:13.89]他说风雨中这点痛算什么
[02:18.91]擦干泪不要问
[02:26.52]他说风雨中这点痛算什么
[02:31.06]擦干泪不要怕
[02:33.56]至少我们还有梦
[02:35.90]他说风雨中这点痛算什么
[02:40.93]擦干泪 不要问
[02:45.83]为什么
",
        "author_id":"90875",
        "privilege":8,
        "privilege2":"1000",
        "play_url":"https://webfs.yun.kugou.com/202003160125/2f2e2ffd3ec977faa6ac8eb9b30782e9/G192/M05/14/03/oJQEAF5rMfmABqLPACwvqCIOEXw604.mp3",
        "authors":[
            {
                "author_id":"90875",
                "is_publish":"1",
                "sizable_avatar":"http://singerimg.kugou.com/uploadpic/softhead/{size}/20190923/20190923173403247.jpg",
                "author_name":"华晨宇",
                "avatar":"http://singerimg.kugou.com/uploadpic/softhead/400/20190923/20190923173403247.jpg"
            }
        ],
        "is_free_part":0,
        "bitrate":128,
        "audio_id":"68837473",
        "play_backup_url":"https://webfs.cloud.kugou.com/202003160125/661c7d7083a25c6d5adee3bdd5dcb953/G192/M05/14/03/oJQEAF5rMfmABqLPACwvqCIOEXw604.mp3"
    }
}
```
## 2. 歌手信息
`http://mobilecdnbj.kugou.com/api/v3/singer/info?singerid=86747&with_res_tag=1`

```json
{
  "status": 1,
  "error": "",
  "data": {
    "identity": 11,
    "mvcount": 13,
    "has_long_intro": 1,
    "intro": "覃沐曦，艺名风小筝，10月4日出生，内地女歌手。曾获酷狗音乐年度音乐人。代表作有《梦魇》《花飞花》《西塘》《一切都会好的》《别丢下我不管》《粘心》《仙侠世界2·剑逍遥》《回忆的日记本》《神度》等。2016年2月1日，风小筝将首发其开年首支新单曲《仙侠世界2·剑逍遥》MV。2017年9月26日，首张数字专辑《学不会妥协》在百度音乐独家首发。2017年10月10日，发表个人单曲《神度》。",
    "songcount": 385,
    "imgurl": "http://singerimg.kugou.com/uploadpic/softhead/{size}/20200101/20200101111427263327.jpg",
    "profile": "覃沐曦，艺名风小筝，10月4日出生，内地女歌手。曾获酷狗音乐年度音乐人。代表作有《梦魇》《花飞花》《西塘》《一切都会好的》《别丢下我不管》《粘心》《仙侠世界2·剑逍遥》《回忆的日记本》《神度》等。2016年2月1日，风小筝将首发其开年首支新单曲《仙侠世界2·剑逍遥》MV。2017年9月26日，首张数字专辑《学不会妥协》在百度音乐独家首发。2017年10月10日，发表个人单曲《神度》。",
    "singerid": 86747,
    "singername": "风小筝",
    "albumcount": 39
  },
  "errcode": 0
}
```

## 3. 搜索
`http://msearchcdn.kugou.com/api/v3/search/song?pagesize=3&keyword=%E5%91%A8%E6%9D%B0%E4%BC%A6&page=1`
> trans_param.musicpack_advance
> 表示是否会员试听。1-会员， 0-无会员
>

```json
{
  "status": 1,
  "error": "",
  "data": {
    "aggregation": [
      {
        "key": "DJ",
        "count": 0
      },
      {
        "key": "现场",
        "count": 0
      },
      {
        "key": "广场舞",
        "count": 0
      },
      {
        "key": "伴奏",
        "count": 0
      },
      {
        "key": "铃声",
        "count": 0
      }
    ],
    "tab": "",
    "info": [
      {
        "othername_original": "",
        "pay_type_320": 3,
        "m4afilesize": 1105494,
        "price_sq": 200,
        "isoriginal": 0,
        "filesize": 4318459,
        "source": "",
        "bitrate": 128,
        "topic": "",
        "trans_param": {
          "cid": 2456863,
          "pay_block_tpl": 1,
          "musicpack_advance": 1,
          "display_rate": 0,
          "exclusive": 1,
          "display": 0,
          "hash_offset": {
            "offset_hash": "2FFFC9C39E650D74564AF316FBC03F64",
            "start_byte": 0,
            "end_ms": 60000,
            "file_type": 0,
            "start_ms": 0,
            "end_byte": 960992
          }
        },
        "price": 200,
        "Accompany": 1,
        "old_cpy": 0,
        "songname_original": "晴天",
        "singername": "周杰伦",
        "pay_type": 3,
        "sourceid": 0,
        "topic_url": "",
        "fail_process_320": 4,
        "pkg_price": 1,
        "feetype": 0,
        "filename": "周杰伦 - 晴天",
        "price_320": 200,
        "songname": "晴天",
        "group": [
          
        ],
        "hash": "3bd5c05b9f8d082ba3c9425a1a712394",
        "mvhash": "f8a3d64efc7245d464126d626ad8b0c2",
        "rp_type": "audio",
        "privilege": 10,
        "album_audio_id": 32100650,
        "rp_publish": 1,
        "album_id": "966846",
        "ownercount": 39384,
        "fold_type": 0,
        "audio_id": 20505418,
        "pkg_price_sq": 1,
        "320filesize": 10794946,
        "isnew": 0,
        "duration": 269,
        "pkg_price_320": 1,
        "srctype": 1,
        "fail_process_sq": 4,
        "sqfilesize": 34643897,
        "fail_process": 4,
        "320hash": "3392290ccc37c963711f30178b8b04b1",
        "extname": "mp3",
        "sqhash": "7a81c75f284121090e21fa8269cb424d",
        "pay_type_sq": 3,
        "320privilege": 10,
        "sqprivilege": 10,
        "album_name": "叶惠美",
        "othername": ""
      },
      {
        "othername_original": "",
        "pay_type_320": 3,
        "m4afilesize": 943525,
        "price_sq": 200,
        "isoriginal": 0,
        "filesize": 3577344,
        "source": "",
        "bitrate": 128,
        "topic": "",
        "trans_param": {
          "cid": 2556475,
          "pay_block_tpl": 1,
          "musicpack_advance": 1,
          "display_rate": 0,
          "exclusive": 1,
          "display": 0,
          "hash_offset": {
            "offset_hash": "B30DAC221051D288DA0F15F150189624",
            "start_byte": 0,
            "end_ms": 60000,
            "file_type": 0,
            "start_ms": 0,
            "end_byte": 960083
          }
        },
        "price": 200,
        "Accompany": 1,
        "old_cpy": 0,
        "songname_original": "稻香",
        "singername": "周杰伦",
        "pay_type": 3,
        "sourceid": 0,
        "topic_url": "",
        "fail_process_320": 4,
        "pkg_price": 1,
        "feetype": 0,
        "filename": "周杰伦 - 稻香",
        "price_320": 200,
        "songname": "稻香",
        "group": [
          {
            "othername_original": "",
            "pay_type_320": 3,
            "m4afilesize": 943525,
            "price_sq": 200,
            "isoriginal": 0,
            "filesize": 3577344,
            "source": "",
            "bitrate": 128,
            "topic": "",
            "trans_param": {
              "cid": 5674436,
              "pay_block_tpl": 1,
              "musicpack_advance": 1,
              "display_rate": 0,
              "exclusive": 1,
              "display": 0,
              "hash_offset": {
                "offset_hash": "B30DAC221051D288DA0F15F150189624",
                "start_byte": 0,
                "end_ms": 60000,
                "file_type": 0,
                "start_ms": 0,
                "end_byte": 960083
              }
            },
            "price": 200,
            "Accompany": 1,
            "old_cpy": 0,
            "songname_original": "稻香",
            "singername": "周杰伦",
            "pay_type": 3,
            "sourceid": 0,
            "topic_url": "",
            "fail_process_320": 4,
            "pkg_price": 1,
            "feetype": 0,
            "filename": "周杰伦 - 稻香",
            "price_320": 200,
            "songname": "稻香",
            "hash": "0a62227caab66f54d43ec084b4bdd81f",
            "mvhash": "abab6d0264026c640cf551ed482566b7",
            "rp_type": "audio",
            "privilege": 10,
            "album_audio_id": 27663257,
            "rp_publish": 1,
            "album_id": "533695",
            "ownercount": 45,
            "fold_type": 0,
            "audio_id": 332453,
            "pkg_price_sq": 1,
            "320filesize": 8942422,
            "isnew": 0,
            "duration": 223,
            "pkg_price_320": 1,
            "srctype": 1,
            "fail_process_sq": 4,
            "sqfilesize": 26093502,
            "fail_process": 4,
            "320hash": "07b52ba6125abe18dfbbd6c34bdcf993",
            "extname": "mp3",
            "sqhash": "f9c90d62803ea395d7cb9566e06fb54d",
            "pay_type_sq": 3,
            "320privilege": 10,
            "sqprivilege": 10,
            "album_name": "巨星金曲",
            "othername": ""
          }
        ],
        "hash": "0a62227caab66f54d43ec084b4bdd81f",
        "mvhash": "abab6d0264026c640cf551ed482566b7",
        "rp_type": "audio",
        "privilege": 10,
        "album_audio_id": 32042828,
        "rp_publish": 1,
        "album_id": "960399",
        "ownercount": 25792,
        "fold_type": 0,
        "audio_id": 332453,
        "pkg_price_sq": 1,
        "320filesize": 8942422,
        "isnew": 0,
        "duration": 223,
        "pkg_price_320": 1,
        "srctype": 1,
        "fail_process_sq": 4,
        "sqfilesize": 26093502,
        "fail_process": 4,
        "320hash": "07b52ba6125abe18dfbbd6c34bdcf993",
        "extname": "mp3",
        "sqhash": "f9c90d62803ea395d7cb9566e06fb54d",
        "pay_type_sq": 3,
        "320privilege": 10,
        "sqprivilege": 10,
        "album_name": "魔杰座",
        "othername": ""
      },
      {
        "othername_original": "",
        "pay_type_320": 3,
        "m4afilesize": 1115709,
        "price_sq": 200,
        "isoriginal": 0,
        "filesize": 4253775,
        "source": "",
        "bitrate": 128,
        "topic": "",
        "trans_param": {
          "cid": 2556399,
          "pay_block_tpl": 1,
          "musicpack_advance": 1,
          "display_rate": 0,
          "exclusive": 1,
          "display": 0,
          "hash_offset": {
            "offset_hash": "651B9CFE3F2A5FA20A5269745B0234DC",
            "start_byte": 0,
            "end_ms": 60000,
            "file_type": 0,
            "start_ms": 0,
            "end_byte": 964146
          }
        },
        "price": 200,
        "Accompany": 1,
        "old_cpy": 0,
        "songname_original": "听妈妈的话",
        "singername": "周杰伦",
        "pay_type": 3,
        "sourceid": 0,
        "topic_url": "",
        "fail_process_320": 4,
        "pkg_price": 1,
        "feetype": 0,
        "filename": "周杰伦 - 听妈妈的话",
        "price_320": 200,
        "songname": "听妈妈的话",
        "group": [
          {
            "othername_original": "",
            "pay_type_320": 3,
            "m4afilesize": 1115709,
            "price_sq": 200,
            "isoriginal": 0,
            "filesize": 4253775,
            "source": "",
            "bitrate": 128,
            "topic": "",
            "trans_param": {
              "cid": 7213239,
              "pay_block_tpl": 1,
              "musicpack_advance": 1,
              "display_rate": 0,
              "exclusive": 1,
              "display": 0,
              "hash_offset": {
                "offset_hash": "651B9CFE3F2A5FA20A5269745B0234DC",
                "start_byte": 0,
                "end_ms": 60000,
                "file_type": 0,
                "start_ms": 0,
                "end_byte": 964146
              }
            },
            "price": 200,
            "Accompany": 1,
            "old_cpy": 0,
            "songname_original": "听妈妈的话",
            "singername": "周杰伦",
            "pay_type": 3,
            "sourceid": 0,
            "topic_url": "",
            "fail_process_320": 4,
            "pkg_price": 1,
            "feetype": 0,
            "filename": "周杰伦 - 听妈妈的话",
            "price_320": 200,
            "songname": "听妈妈的话",
            "hash": "0fff5535ce1862ec37d590688a586b9d",
            "mvhash": "2a08a02d6d721d7e2b6b4118bd693ed0",
            "rp_type": "audio",
            "privilege": 10,
            "album_audio_id": 63788558,
            "rp_publish": 1,
            "album_id": "2547995",
            "ownercount": 35,
            "fold_type": 0,
            "audio_id": 327478,
            "pkg_price_sq": 1,
            "320filesize": 10629986,
            "isnew": 0,
            "duration": 265,
            "pkg_price_320": 1,
            "srctype": 1,
            "fail_process_sq": 4,
            "sqfilesize": 31516210,
            "fail_process": 4,
            "320hash": "faf493b15c5873eac1bdd3421eb309c9",
            "extname": "mp3",
            "sqhash": "e0c38130e16070844d80c3ffa5d26995",
            "pay_type_sq": 3,
            "320privilege": 10,
            "sqprivilege": 10,
            "album_name": "闪亮2006 Hit FM年度百首单曲票选",
            "othername": ""
          }
        ],
        "hash": "0fff5535ce1862ec37d590688a586b9d",
        "mvhash": "2a08a02d6d721d7e2b6b4118bd693ed0",
        "rp_type": "audio",
        "privilege": 10,
        "album_audio_id": 64473824,
        "rp_publish": 1,
        "album_id": "965291",
        "ownercount": 24043,
        "fold_type": 0,
        "audio_id": 327478,
        "pkg_price_sq": 1,
        "320filesize": 10629986,
        "isnew": 0,
        "duration": 265,
        "pkg_price_320": 1,
        "srctype": 1,
        "fail_process_sq": 4,
        "sqfilesize": 31516210,
        "fail_process": 4,
        "320hash": "faf493b15c5873eac1bdd3421eb309c9",
        "extname": "mp3",
        "sqhash": "e0c38130e16070844d80c3ffa5d26995",
        "pay_type_sq": 3,
        "320privilege": 10,
        "sqprivilege": 10,
        "album_name": "依然范特西",
        "othername": ""
      }
    ],
    "correctiontype": 0,
    "timestamp": 1584294372,
    "allowerr": 0,
    "total": 440,
    "istag": 0,
    "istagresult": 0,
    "forcecorrection": 0,
    "correctiontip": ""
  },
  "errcode": 0
}
```

# 4. 推荐歌手
`http://service.mobile.kugou.com/v1/singer/recommend`

```json
{
  "status": 1,
  "error": "",
  "data": {
    "timestamp": 1584294653,
    "info": [
      {
        "singerid": 3520,
        "singername": "周杰伦",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20180515/20180515002522714.jpg"
      },
      {
        "singerid": 90875,
        "singername": "华晨宇",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20190923/20190923173403247.jpg"
      },
      {
        "singerid": 4490,
        "singername": "G.E.M.邓紫棋",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20190720/20190720220214641.jpg"
      },
      {
        "singerid": 1574,
        "singername": "林俊杰",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20191017/20191017142309922.jpg"
      },
      {
        "singerid": 3060,
        "singername": "薛之谦",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20190103/20190103191232626.jpg"
      },
      {
        "singerid": 722869,
        "singername": "毛不易",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20190802/20190802101420425.jpg"
      },
      {
        "singerid": 169967,
        "singername": "周深",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20190708/20190708101121281.jpg"
      },
      {
        "singerid": 1573,
        "singername": "刘德华",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20180507/20180507120242140.jpg"
      },
      {
        "singerid": 3521,
        "singername": "张学友",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20140527/20140527095042283066.jpg"
      },
      {
        "singerid": 753317,
        "singername": "小阿枫",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20180716/20180716172540971.jpg"
      },
      {
        "singerid": 803022,
        "singername": "隔壁老樊",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20190808/20190808152656115.jpg"
      },
      {
        "singerid": 281886,
        "singername": "肖战",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20200203/20200203101223608.jpg"
      },
      {
        "singerid": 730,
        "singername": "刀郎",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20190115/20190115150401884.jpg"
      },
      {
        "singerid": 792619,
        "singername": "杨小壮",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20191226/20191226182839295.jpg"
      },
      {
        "singerid": 90912,
        "singername": "伍佰&China Blue",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20140423/20140423150047293170.jpg"
      },
      {
        "singerid": 3539,
        "singername": "张杰",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20200116/20200116112014747.jpg"
      },
      {
        "singerid": 7633,
        "singername": "凤凰传奇",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20180530/20180530091046423.jpg"
      },
      {
        "singerid": 829435,
        "singername": "半吨兄弟",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20200130/20200130153915971922.jpg"
      },
      {
        "singerid": 3047,
        "singername": "许嵩",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20180906/20180906181115284.jpg"
      },
      {
        "singerid": 420,
        "singername": "陈奕迅",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20180622/20180622193316603.jpg"
      },
      {
        "singerid": 555709,
        "singername": "BLACKPINK",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20190626/20190626102829897.jpg"
      },
      {
        "singerid": 1383,
        "singername": "黄家驹",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20140219/20140219104100727871.jpg"
      },
      {
        "singerid": 93475,
        "singername": "李荣浩",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20191209/20191209164452855.jpg"
      },
      {
        "singerid": 2725,
        "singername": "王杰",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20160910/20160910145826790.jpg"
      },
      {
        "singerid": 1485,
        "singername": "汪苏泷",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20191223/20191223091219204.jpg"
      },
      {
        "singerid": 3538,
        "singername": "郑源",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20160418/20160418100508296.jpg"
      },
      {
        "singerid": 1403,
        "singername": "何鹏",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20181108/20181108161112894.jpg"
      },
      {
        "singerid": 7249,
        "singername": "BEYOND",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20160418/20160418100531196.jpg"
      },
      {
        "singerid": 86281,
        "singername": "庄心妍",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20200210/20200210142406221.jpg"
      },
      {
        "singerid": 3525,
        "singername": "张信哲",
        "img": "http://singerimg.kugou.com/uploadpic/pass/softhead/{size}/20181109/20181109143841244.jpg"
      }
    ]
  },
  "errcode": 0
}
`