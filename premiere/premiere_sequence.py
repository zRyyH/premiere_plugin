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
        """
        Adiciona múltiplos arquivos de áudio à sequência no Adobe Premiere,
        utilizando a busca otimizada `find_media_items(files)`, garantindo que
        múltiplos clipes sejam inseridos corretamente.

        :param files: Lista de nomes dos arquivos de áudio no projeto do Premiere.
        """
        audio_track = self.activeSequence.audioTracks[0]  # Obtém a trilha de áudio

        # Obter todos os itens de mídia de uma vez
        media_items = self.project.find_media_items(files)

        # Se `find_media_items()` retorna um único item ao invés de uma lista, convertemos para lista
        if not media_items:
            info("❌ Nenhum arquivo de áudio encontrado. Cancelando operação.")
            return None
        if not isinstance(media_items, list):  # Se não for lista, transforma em lista
            media_items = [media_items]

        # Insere os clipes na sequência corretamente
        position = 0  # Posição inicial (em ticks)
        for media_item in media_items:
            try:
                # Inserir o áudio na trilha
                audio_track.insertClip(media_item, position)
                info(
                    f"✅ Adicionando áudio {media_item.name} na sequência em {position} ticks"
                )

            except Exception as e:
                info(f"❌ Erro ao adicionar áudio {media_item.name}: {str(e)}")

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
        for track in [self.activeSequence.audioTracks[0]]:
            while track.clips.numItems > 0:
                track.clips[0].remove(False, False)
                info("Removendo clipe de áudio: {track.clips[0].name}")

        info("Áudios removidos da sequência")
        return None

    @safe_sequence
    def limpar_images(self):
        # Limpar trilhas de vídeo
        for track in [self.activeSequence.videoTracks[0]]:
            while track.clips.numItems > 0:
                track.clips[0].remove(False, False)
                info("Removendo clipe de vídeo: {track.clips[0].name}")

        info("Imagens removidas da sequência")
        return None