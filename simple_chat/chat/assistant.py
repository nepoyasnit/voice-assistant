import joblib


class VoiceAssistant:
    """
    Settings of our voice assistant
    """
    # loading a neural model from disk
    talk_model = joblib.load(r'chat/mmm_just_Alice .pkl')

    def assistant_answer(self, voice):
        """
        a function that loads user input into the neural model and predicts the response
        """
        answer = self.talk_model.predict([voice])[0]
        return answer

