from pydantic import BaseModel


class MediaConfig(BaseModel):
    path: list[str]
    mix_size: int
    shuffle: bool
    folder: bool


class ImageConfig(BaseModel):
    image_config: MediaConfig


class MusicConfig(BaseModel):
    music_config: MediaConfig
