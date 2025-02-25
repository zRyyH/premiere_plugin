from concurrent.futures import ThreadPoolExecutor
from premiere.wrappers import safe_sequence
from logger import info


# Classe que representa uma sequência no Adobe Premiere
class PremiereSequence:
    def __init__(self, project):
        self.project = project
        self.activeSequence = project.project.activeSequence

    @safe_sequence
    def get_sequence_duration(self):
        # Obter o tempo total da sequência em ticks
        ticks = self.activeSequence.end
        info(f"Obtendo duração da sequência: {ticks} ticks")
        return ticks

    @safe_sequence
    def get_video_tracks(self):
        # Obter o número de trilhas de vídeo na sequência
        tracks = self.activeSequence.videoTracks[0].clips.numItems
        info(f"Obtendo número de trilhas de vídeo: {tracks}")
        return tracks

    def get_audio_tracks(self):
        # Obter o número de trilhas de áudio na sequência
        tracks = self.activeSequence.audioTracks[0].clips.numItems
        info(f"Obtendo número de trilhas de áudio: {tracks}")
        return tracks

    @safe_sequence
    def add_audio(self, files: list[str]):
        audio_track = self.activeSequence.audioTracks[0]
        media_items = self.project.find_media_items(files)

        # Insere cada clipe na sequência (de forma rápida, sem sobreposição)
        for i, media_item in enumerate(media_items):
            info(f"Adicionando áudio {files[i]} na sequência")
            # Define pontos de entrada/saída e insere na sequência
            audio_track.insertClip(media_item, i)
        return None

    @safe_sequence
    def add_image(self, files: list[str], duration_ticks: int = 5):
        video_track = self.activeSequence.videoTracks[0]

        # Obter itens de mídia do projeto
        media_items = self.project.find_media_items(files)

        # Define pontos de entrada/saída e insere na sequência
        for i, media_item in enumerate(media_items):
            media_item.setInPoint("0", 1)
            media_item.setOutPoint(str(int(duration_ticks)), 1)
            video_track.insertClip(
                media_item, i * int(duration_ticks)
            )  # Espaçamento automático

            info(f"Adicionando imagem {files[i]} na sequência")

        return None

    @safe_sequence
    def limpar_musics(self):
        # Limpar trilhas de áudio
        for track in self.activeSequence.audioTracks:
            while track.clips.numItems > 0:
                track.clips[0].remove(False, False)
                info("Removendo clipe de áudio: {track.clips[0].name}")

        info("Áudios removidos da sequência")
        return None

    @safe_sequence
    def limpar_images(self):
        # Limpar trilhas de vídeo
        for track in self.activeSequence.videoTracks:
            while track.clips.numItems > 0:
                track.clips[0].remove(False, False)
                info("Removendo clipe de vídeo: {track.clips[0].name}")

        info("Imagens removidas da sequência")
        return None
