from core.response import Response, ResponseException

# Create your views here.

class SongView(Response):
    def get(self, request, json_data, *args, **kwargs):
        pass