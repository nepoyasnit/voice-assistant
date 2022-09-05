from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from .models import Dialog, Message

from .assistant import VoiceAssistant
from .forms import UserCreationForm

voice_assistant = VoiceAssistant()  # creating an instance of class-model to predict answers in HomeView.post method


def divide_string(string):
    """
    function that takes a string and divides it into substrings, smaller than 250 characters
    """
    result = []
    while len(string) > 250:
        result.append(string[:250])
        string = string[250:]
    result.append(string)
    return result


class HomeView(View):
    template_name = 'chat/home.html'

    def get(self, request):  # Decide if to create dialog or upload previous messages
        if request.user.is_authenticated:
            try:  # the aim of this statement is to create or find dialog anyway
                dialog = Dialog.objects.get(user_id=request.user.id)
            except:
                Dialog.objects.create(user_id=request.user.id)
            finally:
                messages = Message.objects.filter(dialog__user_id=request.user.id).order_by('date')  # this can return
                # an empty list
            return render(request, self.template_name, {'messages': messages})  # returning messanger page with the
            # message history for authenticated user
        return render(request, self.template_name)  # if user isn't authenticated, we return a default page with the
        # link to log in

    def post(self, request):  # adds messages to the template
        # the user is already authenticated anyway
        current_dialog = Dialog.objects.get(user_id=request.user.id)  # the dialog is guaranted created thanks to the
        # get method
        message = request.POST['message']  # here we get user's message from POST request
        answer = voice_assistant.assistant_answer(message)  # get the answer on user's message
        Message.objects.create(text=message, dialog=current_dialog, is_mine=True)
        Message.objects.create(text=answer, dialog=current_dialog, is_mine=False)
        result = {
            'message': message,
            'answer': answer,
        }
        return JsonResponse(result)  # return a response in JSON format


class Register(View):  # for user's authentication
    template_name = 'registration/register.html'

    def get(self, request):
        context = {  # send user creation form to the template
            'form': UserCreationForm,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():  # if form is valid we create an instance of user and authenticate him to our app
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # then redirect him back to the home view(with changes styles)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)  # returning form with invalid info
