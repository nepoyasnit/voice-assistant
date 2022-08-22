from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .models import Dialog, Message

from .assistant import VoiceAssistant
from .forms import UserCreationForm

voice_assistant = VoiceAssistant()


class HomeView(View):
    template_name = 'chat/home.html'

    def get(self, request):  # Decide if to create dialog or upload previous messages
        if request.user.is_authenticated:
            try:
                dialog = Dialog.objects.get(user_id=request.user.id)
            except:
                Dialog.objects.create(user_id=request.user.id)
            finally:
                messages = Message.objects.filter(dialog__user_id=request.user.id).order_by('date')
            return render(request, self.template_name, {'messages': messages})
        return render(request, self.template_name)

    def post(self, request):  # should add messages to the dialog
        # the user is already authenticated
        current_dialog = Dialog.objects.get(user_id=request.user.id)
        message = request.POST['message']
        answer = voice_assistant.assistant_answer(message)
        Message.objects.create(text=message, dialog=current_dialog, is_mine=True)
        Message.objects.create(text=answer, dialog=current_dialog, is_mine=False)
        result = {
            'message': message,
            'answer': answer,
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
