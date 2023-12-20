from rest_framework.views import APIView
from utils import Responder
# from rest_framework.permissions import IsAuthenticated


class TestView(APIView):

    def get(self, request):
        return Responder.send(
            100,
            "working"
        )
