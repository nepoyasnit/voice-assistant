from django.shortcuts import render
from django.http import JsonResponse
from .assistant import VoiceAssistant

voice_assistant = VoiceAssistant()


def simple_view(request):
    return render(request, 'chat/index.html')


def reload_view(request):
    if request.POST:
        message = request.POST['message']
        result = {
            'message': message,
            'answer': voice_assistant.assistant_answer(message),
        }
        return JsonResponse(result)
