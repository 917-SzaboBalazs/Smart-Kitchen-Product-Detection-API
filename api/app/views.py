from django.shortcuts import render

from rest_framework.views import APIView

from rest_framework.response import Response


class TestView(APIView):

    def get(self, request, *args, **kwargs):

        hello_message_template = 'Hello, {}!'
        name = request.query_params.get('name', 'world')
        message = hello_message_template.format(name)

        return Response({'message': message})

