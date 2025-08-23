from imageio_ffmpeg import get_ffmpeg_exe
import subprocess

def get_ffmpeg_path() -> str:
    """Возвращает путь к встроенному бинарнику FFmpeg."""
    return get_ffmpeg_exe()

def convert_to_wav_16k_mono(input_path: str, output_path: str) -> None:
    """Конвертирует аудио в WAV 16kHz Mono."""
    ffmpeg = get_ffmpeg_path()
    command = [
        ffmpeg,
        "-y",  # overwrite
        "-i", input_path,
        "-ac", "1",         # mono
        "-ar", "16000",     # 16kHz
        output_path
    ]
    subprocess.run(command, check=True)
