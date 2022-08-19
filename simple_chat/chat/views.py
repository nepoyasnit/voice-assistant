from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from .assistant import VoiceAssistant
from .forms import UserCreationForm

voice_assistant = VoiceAssistant()


class HomeView(View):
    template_name = 'chat/home.html'

    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        message = request.POST['message']
        result = {
            'message': message,
            'answer': voice_assistant.assistant_answer(message),
        }
        return JsonResponse(result)


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm,

        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

# def home_view(request):
#     return render(request, 'chat/home.html')
#
#
# def reload_view(request):
#     if request.POST:
#         message = request.POST['message']
#         result = {
#             'message': message,
#             'answer': voice_assistant.assistant_answer(message),
#         }
#         return JsonResponse(result)
