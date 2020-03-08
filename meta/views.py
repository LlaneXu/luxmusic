from core.response import Response, ResponseException
from .models import Song, Artist
from core.media import get_url_from_meta
from core.netease import get_url_by_song_id
from core.redis_queue import push_download
from django.conf import settings

# Create your views here.

class SongView(Response):
    def get(self, request, json_data, *args, **kwargs):
        """
        example:
        localhost:8000/api/meta/song/?id=1234&neteaseId=23423&artists=abc&artists=def&name=something
        :param request:
        :param json_data:
        :param args:
        :param kwargs:
        :return:
        """
        id = request.GET.get('id')
        netease_id = request.GET.get('neteaseId')
        artists = request.GET.getlist('artists')
        name = request.GET.get('name')
        album = request.GET.get('album')

        ret = {}
        # use id to query first
        try:
            if id:
                song = Song.objects.get(id=id)
            elif netease_id:
                song = Song.objects.get(netease_id=netease_id)
            elif artists and len(artists) and name:
                songs = Song.objects.all()
                for artist in artists:
                    songs = songs.filter(artists__name__exact=artist)
                if album:
                    songs = songs.filter(album__name=album)
                song = songs[0]
            else:
                raise ResponseException("not enough params")

            ret = song.to_dict()

        except Song.DoesNotExist:
            pass

        # can find the song record and downloaded, return local file
        if ret.get("downloaded"):
            ret["url"] =   get_url_from_meta(ret)
        else:
            if netease_id:
                data = {
                    "source": "netease",
                    "id": netease_id,
                }
                push_download(data)
                ret["url"] = get_url_by_song_id(netease_id)
        return ret
