from premiere.helpers import normalize_mix
from pathlib import Path
import random
from logger import info


extensoes = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".gif",
    ".tiff",
    ".mp3",
    ".wav",
    ".flac",
    ".aac",
    ".ogg",
    ".wma",
    ".m4a",
}


def load_files(paths: list[str], mix_size: int, shuffle: bool, folder: bool):
    files = [Path(p) for p in paths]
    info(f"Modo de embaralhamento: {shuffle}, Modo de pasta: {folder}")

    if folder:
        if shuffle:
            random.shuffle(files)
        files = normalize_mix(mix_size, files)
        files = [f for f in files if f.suffix.lower() in extensoes]

    for f in files:
        info(f"Arquivo carregado: {f.name} - {f}")
    files = [[str(f) for f in files], [f.name for f in files]]

    return files
