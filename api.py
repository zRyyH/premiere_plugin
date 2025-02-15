from premiere.premiere import Premiere
from models import MediaConfig
from fastapi import FastAPI
import uvicorn
import atexit


app = FastAPI()


premiere_driver = Premiere()
premiere_driver.connect()
atexit.register(premiere_driver.disconnect)


@app.get("/connect")
def connect():
    try:
        return {"mensagem": "Projeto Premiere Pro Conectado!"}
    except Exception as e:
        return {"mensagem": f"Erro ao conectar ao Premiere Pro!, error: {e}"}


@app.post("/import_files")
def import_files(payload: MediaConfig):
    try:
        config = payload.dict()
        print(config)

        image_config = config["image_config"]
        music_config = config["music_config"]

        premiere_driver.import_images(**image_config)
        premiere_driver.import_musics(**music_config)

        return {"mensagem": "Arquivos importados!"}
    except Exception as e:
        return {"mensagem": f"Erro ao importar arquivos!, error: {e}"}


@app.get("/add_files")
def add_files():
    try:
        premiere_driver.add_audio()
        premiere_driver.add_image()

        return {"mensagem": "Arquivos adicionados a sequencia!"}
    except Exception as e:
        return {"mensagem": f"Erro ao adicionar arquivos a sequencia!, error: {e}"}


@app.get("/clear")
def start():
    try:
        premiere_driver.limpar_sequencia()

        return {"mensagem": "Sequencia limpa!"}
    except Exception as e:
        return {"mensagem": f"Erro ao limpar sequencia!, error: {e}"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
