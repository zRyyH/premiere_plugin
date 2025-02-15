from premiere.utils import load_files
from premiere.premiere_sequence import PremiereSequence
from premiere.premiere_project import PremiereProject
from premiere.wrappers import safe_premiere
from logger import info
import pymiere


class Premiere:
    def __init__(self):
        self.project = None
        self.sequence_project = None
        self.duration_ticks = "0"
        self.music_names = []
        self.image_names = []

    @safe_premiere
    def connect(self):
        self.project = PremiereProject(pymiere.objects.app.project)
        self.sequence_project = PremiereSequence(self.project)
        info("Projeto Premiere Pro Conectado!")

    @safe_premiere
    def disconnect(self):
        self.project = None
        self.sequence_project = None
        info("Projeto Premiere Pro Desconectado!")

    @safe_premiere
    def import_musics(self, path, mix_size, shuffle, folder):
        music_paths, self.music_names = load_files(path, mix_size, shuffle, folder)
        project_files = self.project.get_project_files()

        self.project.import_files(music_paths, project_files)

    @safe_premiere
    def import_images(self, path, mix_size, shuffle, folder):
        image_paths, self.image_names = load_files(path, mix_size, shuffle, folder)
        project_files = self.project.get_project_files()

        self.project.import_files(image_paths, project_files)

    @safe_premiere
    def add_audio(self):
        self.sequence_project.add_audio(self.music_names)
        self.duration_ticks = self.sequence_project.get_sequence_duration()

    @safe_premiere
    def add_image(self):
        self.sequence_project.add_image(
            self.image_names, int(self.duration_ticks / len(self.image_names))
        )

    @safe_premiere
    def limpar_sequencia(self):
        self.sequence_project.limpar_sequencia()
