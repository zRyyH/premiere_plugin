from pydantic import BaseModel


class ImageConfig(BaseModel):
    path: list[str]
    mix_size: int
    shuffle: bool
    folder: bool


class MusicConfig(BaseModel):
    path: list[str]
    mix_size: int
    shuffle: bool
    folder: bool


class MediaConfig(BaseModel):
    image_config: ImageConfig
    music_config: MusicConfig
