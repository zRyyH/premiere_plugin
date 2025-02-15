def normalize_mix(mix_size: int, files: list) -> int:
    return files[: max(1, min(mix_size, len(files)))]