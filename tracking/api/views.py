from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .. import models, utils


class PageViewsAPIView(APIView):
    def post(self, request):
        utils.chunk_pageviews()
        return Response("success!!", status=status.HTTP_200_OK)
