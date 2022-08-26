import sys
from PyQt5 import QtWidgets
import AssistantApp
import pyaudio
import NeighborSampler_


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = AssistantApp.AssistantApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print(i, p.get_device_info_by_index(i)['name'])
    app.exec_()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
