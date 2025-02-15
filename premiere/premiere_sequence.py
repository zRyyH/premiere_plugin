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
    def add_audio(self, files: list[str]):
        # Obtém a primeira faixa de áudio da sequência
        audio_track = self.activeSequence.audioTracks[0]

        for midia in files:
            # Obter o primeiro item de mídia carregado
            media_item = self.project.find_media_item(midia)

            # Adiciona um clipe na faixa de áudio
            audio_track.insertClip(media_item, 0)
            info(f"Adicionando áudio {midia} na sequência")
        return None

    @safe_sequence
    def add_image(self, files: list[str], duration_ticks: int = 5):
        # Obtém a primeira faixa de vídeo da sequência
        video_track = self.activeSequence.videoTracks[0]

        for midia in files:
            # Obter o primeiro item de mídia carregado
            media_item = self.project.find_media_item(midia)

            # Converter duração em segundos para ticks
            in_point_ticks = "0"  # Início sempre em 0
            out_point_ticks = str(int(duration_ticks))  # Duração convertida para ticks

            # Definir ponto de entrada (inPoint) e saída (outPoint) antes de inserir na timeline
            media_item.setInPoint(in_point_ticks, 1)
            media_item.setOutPoint(out_point_ticks, 1)

            # Adiciona um clipe na faixa de vídeo
            video_track.insertClip(media_item, 0)
            info(f"Adicionando imagem {midia} na sequência")

        return None

    @safe_sequence
    def limpar_sequencia(self):
        # Limpar trilhas de vídeo
        for track in self.activeSequence.videoTracks:
            while track.clips.numItems > 0:
                track.clips[0].remove(False, False)
                info("Removendo clipe de vídeo")

        # Limpar trilhas de áudio
        for track in self.activeSequence.audioTracks:
            while track.clips.numItems > 0:
                track.clips[0].remove(False, False)
                info("Removendo clipe de áudio")

        info("Sequência limpa")
