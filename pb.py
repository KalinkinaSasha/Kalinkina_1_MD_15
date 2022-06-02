import os
import telebot
import requests
import speech_recognition as sr
import subprocess
import datetime
token ='5323876750:AAGZhQtnZkO4ezFrC2WdmgUw9BxswQGEOgs'

logfile = str(datetime.date.today()) + 'log'

#Преобразователь
def audio_to_text(dest_name: str):
    r = sr.Recognizer()
    message = sr.AudioFile(dest_name)
    with message as source:
        audio = r.record(source)
    result = r.recognize_google(audio, language="ru_RU")
    return result

#Принять голосовое от пользователя
@bot.message_handler(content_types=['voice'])
def get_audio_messages(message):
    try:
        print(("Started recognition..."))
        file_info = bot.get_file(message.voice.file_id)
        path = file_info.file_path #Полный путь до файла
        fname = os.path.basename(path) #Путь в имя файла
        doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
        with open(fname+'.oga','wb') as f:
            f.write(doc.content) #Хранение
        process = subprocess.run(['ffmpeg', '-i', fname+'.oga', fname+'.wav'])
        result = audio_to_text(fname+'wav') #Вызов функции
        bot.send_message(message.from_user.id, format(result)) #Отправляем текст
    except sr.UnknownValueError as e:
        bot.send_message(message.from_user.id, "Не удалось разобрать")
        with open(logfile,'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id)) + ':' +str(message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' + str(message.from_user.username) + ':' + str(message.from_user.language_code) + ':Message is empty.\n')
    except Exception as e:
        bot.send_message(message.from_user.id, "Что-то пошло не так")
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id)) + ':' +str(message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' + str(message.from_user.username) + ':' + str(message.from_user.language_code) + ':' + str(e) + '\n')
    finally:
        os.remove(fname+'.wav')
        os.remove(fname+'.oga')

bot.polling(none_stop=True, interval=0) #Проверяем наличие соо