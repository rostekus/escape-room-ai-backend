import abc
import os
import uuid
from pathlib import Path

import soundfile as sf
from google.cloud import storage


class LocalToRemoteSerializer(abc.ABC):
    def __init__(self, tmp_folder_directory: str, ext: str):
        self.tmp_folder_directory = tmp_folder_directory
        self.ext = ext.replace(".", "")
        self._tmp_file_Path = Path(
            self.tmp_folder_directory, str(uuid.uuid4())
        ).with_suffix("." + ext)
        os.makedirs(self.tmp_folder_directory, exist_ok=True)
        self._local_serializer = None

    def get_tmp_file_path(self):
        return str(self._tmp_file_Path)

    @abc.abstractmethod
    def _write_to_local(self):
        pass

    @abc.abstractmethod
    def serialize(
        self, dst_bucket_name: str, dst_file_path: str
    ) -> None:  # todo: exception handle'
        pass

    def __enter__(self):
        self._write_to_local()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # TODO: exception handling
        self._tmp_file_Path.unlink()


class AudioGoogleSerializer(LocalToRemoteSerializer):
    def __init__(self, audio_content, sampling_rate, ext: str, tmp_folder_path: str):
        super().__init__(tmp_folder_path, ext)
        self._audio_buffer = audio_content
        self._sampling_rate = sampling_rate

    def serialize(self, dst_bucket_name: str, dst_bucket_file_key: str):
        storage_client = storage.Client()
        bucket = storage_client.bucket(dst_bucket_name)
        tmp_file_key = dst_bucket_file_key
        if dst_bucket_file_key[-len(self.ext) :] != self.ext:
            tmp_file_key = dst_bucket_file_key + "." + self.ext
        blob = bucket.blob(tmp_file_key)
        blob.upload_from_filename(str(self._tmp_file_Path))

    def _write_to_local(self):
        sf.write(str(self._tmp_file_Path), self._audio_buffer, self._sampling_rate)

    def get_audio_duration(self):
        return len(self._audio_buffer) / self._sampling_rate
