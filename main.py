import pyttsx3
import speech_recognition as sr
from fuzzywuzzy import fuzz
from datetime import datetime
import time

# options

opts = {
    "alias": ("Алиса", "алиса", "Лиса", "лиса"),  # обращение при прослушивании
    "tbr": ('скажи', 'покажи', 'расскажи', 'произнеси', 'сколько'),
    "cmds": {
        "ctime": (
            'текущие время', 'сейчас времени', 'сейчас время', 'сколько времени', 'какой час', 'на часах',
            'который час'),  # команды
        "about_dev": ('Кто тебя создал', 'создатель'),
    }
}


# Главный [метод] который стартует по умолчанию
def main():
    while True:
        sp_recognizer()


# Перечесление [обращений]
# к голосовому помошнику

def all_name_assistent():
    for alis in opts["alias"]:
        result = alis
        sp_text(result)


# [метод] Приветствие
def hello_to_me():
    sp_text('Добро пожаловать')
    all_name_assistent()


# -------------------


# функция воспроизведения
def sp_text(what):
    print("Вы сказали " + what)
    speech = pyttsx3.init()
    speech.say(what)
    speech.runAndWait()


def recognizer_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC


def execute_cmd(cmd):
    # комманда ["Время"]
    if cmd == 'ctime':
        # текущие время
        now = datetime.now()
        # говорим текущие время
        sp_text("Текущие время: " + str(now.hour) + ":" + str(now.minute))

    # комманды [нецензурные]
    if cmd == 'about_dev':
        sp_text("SkyNet")


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU")

        print(str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":"
              + str(datetime.now().second) + " [LG] Распознал: " + voice)

        if voice.startswith(opts["alias"]):

            # Обращение по имени
            cmd = voice

            for x in opts["alias"]:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознавание комманды
            cmd = recognizer_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print(str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":"
              + str(datetime.now().second) + " [LG] Не распознал комманду")
    except sr.RequestError:
        print(str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":"
              + str(datetime.now().second) + " [LG] Не могу сделать запрос!")


# Функция прослушивания
def sp_recognizer():
    # print("Слушаю!")

    rec = sr.Recognizer()
    # индекс микрофона с которого мы слушаем
    mic = sr.Microphone(device_index = 1)

    with mic as source:
        # создает шум
        rec.adjust_for_ambient_noise(source)

    # Приветствие
    # hello_to_me()

    # слушает каждую сек
    stop_listen = rec.listen_in_background(mic, callback)
    while True: time.sleep(0.1)  # бесконечное просулшивание


# auto first start program


main()
