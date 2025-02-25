from premiere.premiere import Premiere
from models import ImageConfig, MusicConfig
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


@app.post("/load_images")
def load_images(payload: ImageConfig):
    try:
        config = payload.dict()
        print(config)

        image_config = config["image_config"]
        image_names = premiere_driver.load_images(**image_config)

        return {"image_names": image_names}
    except Exception as e:
        return {"mensagem": f"Erro ao carregar imagens!, error: {e}"}


@app.post("/load_musics")
def load_musics(payload: MusicConfig):
    try:
        config = payload.dict()
        print(config)

        music_config = config["music_config"]
        music_names = premiere_driver.load_musics(**music_config)

        return {"music_names": music_names}
    except Exception as e:
        return {"mensagem": f"Erro ao carregar musicas!, error: {e}"}


@app.get("/import_images")
def import_images():
    try:
        premiere_driver.import_images()

        return {"mensagem": "Imagens importadas!"}
    except Exception as e:
        return {"mensagem": f"Erro ao importar imagens!, error: {e}"}


@app.get("/import_musics")
def import_musics():
    try:
        premiere_driver.import_musics()

        return {"mensagem": "Musicas importadas!"}
    except Exception as e:
        return {"mensagem": f"Erro ao importar musicas!, error: {e}"}


@app.get("/add_musics")
def add_musics():
    try:
        premiere_driver.add_audio()

        return {"mensagem": "Musicas adicionadas a sequencia!"}
    except Exception as e:
        return {"mensagem": f"Erro ao adicionar arquivos a sequencia!, error: {e}"}


@app.get("/add_images")
def add_images():
    try:
        premiere_driver.add_image()

        return {"mensagem": "Imagens adicionadas a sequencia!"}
    except Exception as e:
        return {"mensagem": f"Erro ao adicionar imagens a sequencia!, error: {e}"}


@app.get("/clear_images")
def clear_images():
    try:
        premiere_driver.limpar_imagens()

        return {"mensagem": "Imagens removidas da sequencia!"}
    except Exception as e:
        return {"mensagem": f"Erro ao remover imagens da sequencia!, error: {e}"}


@app.get("/clear_musics")
def clear_musics():
    try:
        premiere_driver.limpar_musicas()

        return {"mensagem": "Musicas removidas da sequencia!"}
    except Exception as e:
        return {"mensagem": f"Erro ao remover musicas da sequencia!, error: {e}"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
