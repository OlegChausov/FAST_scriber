#сейчас этот файл просто прокладка между ffmpeg.py и utils.py.
#возможно будем еще здесь нормализовывать громкость, убирать шумы итд
from .ffmpeg import convert_to_wav_16k_mono


# Пример вызова
#convert_to_wav_16k_mono("input.mp3", "output.wav")
