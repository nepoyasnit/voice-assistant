import mainwindow
from PyQt5 import QtWidgets
import assistant


class AssistantApp(QtWidgets.QMainWindow, mainwindow.Ui_Assistant):

    def __init__(self):
        self.assist = assistant.Assistant()
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.sendBtn.clicked.connect(self.sendBtn_clicked)
        self.voiceMessageBtn.clicked.connect(self.recordBtn_clicked)

    def sendBtn_clicked(self):
        if self.messageLine.text() != "":
            text = self.messageLine.text()
            self.messageEdit.setPlainText(self.messageEdit.toPlainText() + "You: " + text + '\n')
            answer = self.assist.answer(text)
            self.messageEdit.setPlainText(self.messageEdit.toPlainText() + "Assistex: " + answer + '\n')
            self.messageLine.setText("")
            self.assist.play_voice_assistant_speech(answer)

    def recordBtn_clicked(self):
        self.voiceMessageBtn.setDisabled(True)
        text = assistant.record_and_recognize_audio()
        self.messageEdit.setPlainText(self.messageEdit.toPlainText() + "You: " + text + '\n')
        answer = self.assist.answer(text)
        self.messageEdit.setPlainText(self.messageEdit.toPlainText() + "Assistex: " + answer + '\n')
        self.messageLine.setText("")
        self.assist.play_voice_assistant_speech(answer)
        self.voiceMessageBtn.setDisabled(False)