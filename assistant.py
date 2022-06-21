import os
import string
import traceback
import webbrowser

import joblib
import pyttsx3
import speech_recognition
import wikipedia


def cleaner(x):
    """
    cleaning function required for neural model
    """
    return [a for a in (''.join([a for a in x if a not in string.punctuation])).lower().split()]

class VoiceAssistant:
    """
    Settings of our voice assistant
    """
    name = ""
    sex = ""
    speech_lang = ""
    recognition_lang = ""
    # initializing speech recognition and input tools
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    # initialization of the speech synthesis tool
    ttsEngine = pyttsx3.init()

    def assistant_answer(self, voice):
        """
        a function that loads user input into the neural model and predicts the response
        """
        answer = self.talk_model.predict([voice])[0]
        return answer





    # loading a neural model from disk
    talk_model = joblib.load('D:\Models\model.pkl')


    def setup_assistant_voice(self):
        """
        Setting the default voice
        """
        voices = self.ttsEngine.getProperty("voices")

        if self.speech_lang == "en":
            self.ttsEngine.recognition_lang = "en-US"
            if self.sex == "male":
                # Microsoft David Desktop - Eng(USA)
                self.ttsEngine.setProperty("voice", voices[2].id)
            else:
                # Microsoft Kira Desktop - Eng(USA)
                self.ttsEngine.setProperty("voice", voices[2].id)
        else:
            self.ttsEngine.assistant.recognition_lang = "ru-RU"
            # Microsoft Irina Desktop - Russia
            self.ttsEngine.setProperty("voice", voices[0].id)


    def search_on_wikipedia(self, *args: tuple):
        """
        Search in Wikipedia, followed by voicing the results and opening links
        :param args: search term
        """
        if not args[0]:
            return

        search_term = ''.join(args[0])

        wiki_page = wikipedia.page(search_term)

        try:
            if wiki_page.url != "":
                self.play_voice_assistant_speech("Here is what I found for " + search_term + " on Wikipedia")
                webbrowser.get().open(wiki_page.url)

                # чтение ассистентом первых двух предложений summary со страницы Wikipedia
                # (могут быть проблемы с мультиязычностью)
                self.play_voice_assistant_speech(wiki_page.summary.split(".")[:2])
            else:
                # открытие ссылки на поисковик в браузере в случае, если на Wikipedia не удалось найти ничего по запросу
                self.play_voice_assistant_speech("Can't find " + search_term + "on Wikipedia. /"
                                                                          "But here is what I found on google")
                url = "https://google.com/search?q=" + search_term
                webbrowser.get().open(url)
        except():
            self.play_voice_assistant_speech("Seems like we have a trouble. See logs for more information")
            traceback.print_exc()
            return


    def play_voice_assistant_speech(self, text):
        # voice assistant response speech playback
        self.ttsEngine.say(str(text))
        self.ttsEngine.runAndWait()


    def record_and_recognize_audio(self):
        """
        speech recording and recognition function
        """
        with self.microphone:
            recognized_data = ""

            # we adjust the ambient noise level
            self.recognizer.adjust_for_ambient_noise(self.microphone, 2)

            try:
                print("Listening...")
                audio = self.recognizer.listen(self.microphone, 5, 5)
                with open("microphone-results.wav", "wb") as file:
                    file.write(audio.get_wav_data())

            except speech_recognition.WaitTimeoutError:
                print("Can you check if your microphone is on, please?")
                return

            # we use online recognition via Google
            try:
                print("Started recognition...")
                recognized_data = self.recognizer.recognize_google(audio, language="eng").lower()

            except speech_recognition.UnknownValueError:
                pass

            # if there are problems with the Internet

            except speech_recognition.RequestError:
                print("Check your internet connection, pls")

            return recognized_data


    def video_search(self, *args: tuple):
        """
        search for a query on YouTube and open a link with answers to the query
        :param args: search term
        """
        if not args[0]:
            return
        search_term = ''.join(args[0])
        url = "https://www.youtube.com/results?search_query=" + search_term
        webbrowser.get().open(url)
        self.play_voice_assistant_speech("Here is what I found for " + search_term + "on youtube")


    def check_commands(self, voice_input, is_work, just_talk, is_talk):
        """
        a function that checks speech for commands (disabled in the "just chatting" mode)
        :param voice_input: user input
        :param is_work: a boolean variable that checks whether the assistant's work needs to be completed at the user's request
        :param just_talk: boolean variable that checks whether the user has requested to enable the "let's chat" mode
        :param is_talk: a boolean variable that checks whether the prediction of the answer is necessary or only requires the execution of a command
        """
        if voice_input == "goodbye" or voice_input == "bye":
            is_work = False
        elif voice_input == "let's talk":
            just_talk = True
            self.play_voice_assistant_speech("I love to chat! If you get tired, say stop talking")
            is_talk = False
        elif voice_input.find("find in wikipedia") != -1:
            self.search_on_wikipedia(voice_input[18:])
            is_talk = False
        elif voice_input.find("search on youtube") != -1:
            self.video_search(voice_input[18:])
            is_talk = False
        return is_work, just_talk, is_talk


    def talk(self):
        """
         the function responsible for the dialog itself calls the functions of recording and speech recognition,
         checking for commands and voicing the assistant's response.
        """
        just_talk = False
        is_work = True
        while is_work:
            is_talk = True
            voice_input = ""
            voice_input = self.record_and_recognize_audio()
            print(voice_input)
            os.remove("microphone-results.wav")
            if not just_talk:
                is_work, just_talk, is_talk = self.check_commands(voice_input, is_work, just_talk, is_talk)
            if voice_input == "stop talking":
                just_talk = False
            if is_talk:
                assistant_answer = self.assistant_answer(voice_input)
                self.play_voice_assistant_speech(assistant_answer)
                print(assistant_answer)


if __name__ == "__main__":

    vAssistant = VoiceAssistant()

    # configuring voice assistant data
    vAssistant.name = "Blonde"
    vAssistant.sex = "female"
    vAssistant.speech_lang = "en"

    # setting the default voice
    vAssistant.setup_assistant_voice()

    vAssistant.talk()
