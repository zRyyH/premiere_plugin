from premiere.utils import load_files
from premiere.premiere_sequence import PremiereSequence
from premiere.premiere_project import PremiereProject
from premiere.wrappers import safe_premiere
from logger import info
import pymiere


# Classe que representa o Adobe Premiere Pro
class Premiere:
    def __init__(self):
        self.project = None
        self.sequence_project = None
        self.duration_ticks = "0"
        self.music_names = []
        self.image_names = []
        self.music_paths = []
        self.image_paths = []

    @safe_premiere
    # Conectar ao Adobe Premiere Pro
    def connect(self):
        self.project = PremiereProject(pymiere.objects.app.project)
        self.sequence_project = PremiereSequence(self.project)
        info("Projeto Premiere Pro Conectado!")
        return None

    @safe_premiere
    # Desconectar do Adobe Premiere Pro
    def disconnect(self):
        self.project = None
        self.sequence_project = None
        info("Projeto Premiere Pro Desconectado!")
        return None

    @safe_premiere
    # Carregar arquivos de música
    def load_musics(self, path, mix_size, shuffle, folder):
        self.music_paths, self.music_names = load_files(path, mix_size, shuffle, folder)
        return self.music_names

    @safe_premiere
    # Carregar arquivos de imagem
    def load_images(self, path, mix_size, shuffle, folder):
        self.image_paths, self.image_names = load_files(path, mix_size, shuffle, folder)
        return self.image_names

    @safe_premiere
    # Importar arquivos de imagem
    def import_images(self):
        project_files = self.project.get_project_files()
        info(f"Arquivos de imagem: {self.image_paths}")
        self.project.import_files(self.image_paths, project_files)
        return None

    @safe_premiere
    # Importar arquivos de música
    def import_musics(self):
        project_files = self.project.get_project_files()
        info(f"Arquivos de música: {self.music_paths}")
        self.project.import_files(self.music_paths, project_files)
        return None

    @safe_premiere
    # Adicionar arquivos de música e imagem à sequência
    def add_audio(self):
        self.sequence_project.add_audio(self.music_names)
        self.duration_ticks = self.sequence_project.get_sequence_duration()
        return None

    @safe_premiere
    # Adicionar arquivos de imagem à sequência
    def add_image(self):
        self.sequence_project.add_image(
            self.image_names,
            int(
                self.duration_ticks
                / (self.sequence_project.get_video_tracks() + len(self.image_names))
            ),
        )
        return None

    @safe_premiere
    # Limpar sequência de músicas
    def limpar_musicas(self):
        self.sequence_project.limpar_musics()
        self.duration_ticks = "0"
        self.music_names = []
        self.music_paths = []
        return None

    @safe_premiere
    # Limpar sequência de imagens
    def limpar_imagens(self):
        self.sequence_project.limpar_images()
        self.duration_ticks = "0"
        self.image_names = []
        self.image_paths = []
        return None