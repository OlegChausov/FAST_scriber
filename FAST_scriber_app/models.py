from datetime import timedelta, timezone
from sqlalchemy import Column, String, DateTime, Float, Boolean
import uuid
from datetime import datetime, UTC
from FAST_scriber_app.db_base import Base



class AudioFile(Base):
    __tablename__ = "audio_files"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    original_filename = Column(String, nullable=False)            # имя до загрузки
    audio_uuid_name = Column(String, nullable=False, unique=True) # имя файла после сохранения
    transcript_uuid_name = Column(String, nullable=True, unique=True)  # имя json-файла транскрипта
    format = Column(String, nullable=False)                        # mp3, wav, m4a и пр.
    duration = Column(Float, nullable=True)                        # длительность в секундах
    created_at = Column(DateTime, default=lambda: datetime.now(UTC)) #Лямбда-функция нужна, чтобы значение вычислялось при каждом создании новой записи — а не один раз при запуске приложения.
    transcribed_at = Column(DateTime, nullable=True)
    is_transcript_ready = Column(String, default=None) #"Done", "In process", "Failed", "Missing", None
    in_bin = Column(Boolean, default=False)
    time_of_throwing_to_bin = Column(DateTime, nullable=True)



    @property
    def audio_url(self):
        return f"/static/audio/{self.audio_uuid_name}"

    @property
    def final_cut_time(self):
        if self.time_of_throwing_to_bin is None:
            return None
        # Превращаем naive в aware вручную
        naive = self.time_of_throwing_to_bin  #Не содержит информации о временной зоне (tzinfo=None)
        aware = naive.replace(tzinfo=timezone.utc) #Содержит tzinfo, например timezone.utc, и знает своё смещение
        return aware + timedelta(days=30)

    @property
    def is_expired(self) -> bool:
        final = self.final_cut_time
        if final is None:
            return False
        # Сравниваем aware с aware
        return datetime.now(timezone.utc) > final









