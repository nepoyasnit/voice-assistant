from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .models import Dialog, Message
from .assistant import VoiceAssistant
from .forms import UserCreationForm

voice_assistant = VoiceAssistant()  # creating an instance of class-model to predict answers in HomeView.post method


class HomeView(View):
    template_name = 'chat/home.html'

    def get(self, request):
        """
        shows messanger page if user is authenticated
        shows login page if user is anonymous
        """
        if request.user.is_authenticated:
            try:  # creates of finds dialog
                dialog = Dialog.objects.get(user_id=request.user.id)
            except:
                Dialog.objects.create(user_id=request.user.id)
            finally: # select related to this dialog messages
                messages = Message.objects.filter(dialog__user_id=request.user.id).order_by('date')

            return render(request, self.template_name, {'messages': messages})  # returning messanger page
        return render(request, self.template_name)  # returning link to login

    def post(self, request):  # adds messages to the template
        # the user is already authenticated anyway
        current_dialog = Dialog.objects.get(user_id=request.user.id)  # the dialog is guaranted created thanks to the
        # get method
        message = request.POST['message']
        answer = voice_assistant.assistant_answer(message)  # getting the answer
        Message.objects.bulk_create([Message(text=message, dialog=current_dialog, is_mine=True),Message(text=answer, dialog=current_dialog, is_mine=False)])
        # Message.objects.create(text=message, dialog=current_dialog, is_mine=True)
        # Message.objects.create(text=answer, dialog=current_dialog, is_mine=False)
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
