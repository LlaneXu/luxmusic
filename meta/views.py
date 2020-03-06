from core.response import Response, ResponseException
from .models import Song, Artist

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
                song = songs[0]
            else:
                raise ResponseException("not enough params")
        except Song.DoesNotExist:
            pass
        return song.to_dict()
