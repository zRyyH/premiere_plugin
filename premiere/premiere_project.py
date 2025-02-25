from premiere.wrappers import safe_project
import time

class PremiereProject:
    def __init__(self, project=None):
        self.project = project

    @safe_project
    def get_project_files(self):
        # Listar arquivos do projeto
        return list(map(lambda x: x.name, self.project.rootItem.children))

    @safe_project
    def find_media_items(self, file_names: list[str]):
        print("Iniciando busca otimizada de mídia...")
        
        t0 = time.time()

        # Armazena os itens do projeto em um dicionário para busca O(1)
        project_itens = list(self.project.rootItem.children)  # Avalia tudo antes
        project_dict = {item.name: item for item in project_itens}  # Indexa para busca rápida

        # Busca os arquivos de forma extremamente eficiente
        media_items = [project_dict[file] for file in file_names if file in project_dict]

        # Tempo de execução
        t1 = time.time()
        print(f"Busca concluída em {t1 - t0:.4f} segundos")

        return media_items

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
