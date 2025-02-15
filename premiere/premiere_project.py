from premiere.wrappers import safe_project


class PremiereProject:
    def __init__(self, project=None):
        self.project = project

    @safe_project
    def get_project_files(self):
        # Listar arquivos do projeto
        return list(map(lambda x: x.name, self.project.rootItem.children))

    @safe_project
    def find_media_item(self, file_name: str):
        # Buscar item de mídia no projeto
        for item in self.project.rootItem.children:
            if file_name.lower() in item.name.lower():
                return item

        raise FileNotFoundError(f"Arquivo {file_name} não encontrado no projeto!")

    @safe_project
    def import_files(self, file_paths: list[str], project_files: list[str]):
        # Filtrar arquivos já importados
        file_paths = list(
            filter(lambda x: x.split("\\")[-1] not in project_files, file_paths)
        )

        # Importar arquivos para o projeto
        self.project.importFiles(
            file_paths,
            suppressUI=True,
            targetBin=self.project.rootItem,
            importAsNumberedStills=False,
        )
        return None

    @safe_project
    def stop(self):
        # Encerrar instância do Adobe Premiere
        self.project = None
        return None
