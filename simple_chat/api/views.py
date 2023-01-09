from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
# Create your views here.

from chat.assistant import VoiceAssistant

voice_assistant = VoiceAssistant()


class MessageAPI(APIView):

    def post(self, request):
        question = request.data['question']
        result = voice_assistant.assistant_answer(question)
        return Response({"answer": result})
