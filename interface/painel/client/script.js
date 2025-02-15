// Função para alternar entre seleção de arquivos e pastas
function toggleFileInput(inputId, isFolder) {
    let inputElement = document.getElementById(inputId);
    inputElement.setAttribute("type", "file");

    if (isFolder) {
        inputElement.setAttribute("webkitdirectory", "");
        inputElement.setAttribute("directory", "");
        inputElement.removeAttribute("multiple");
    } else {
        inputElement.removeAttribute("webkitdirectory");
        inputElement.removeAttribute("directory");
        inputElement.setAttribute("multiple", "");
    }
}

// Função para abrir o seletor de arquivos/pastas
function openFileSelector(inputId, checkboxId) {
    let checkbox = document.getElementById(checkboxId);
    toggleFileInput(inputId, checkbox.checked);
    document.getElementById(inputId).click();
}

// Função para obter arquivos selecionados
function getSelectedFiles(inputId) {
    const inputElement = document.getElementById(inputId);
    const files = Array.from(inputElement.files);
    return files.map(file => file.path || file.webkitRelativePath || file.name);
}

// Função para enviar os arquivos para a API
function importFiles() {
    const imagePaths = getSelectedFiles("imageInput");
    const musicPaths = getSelectedFiles("musicInput");

    const imageMixSize = parseInt(document.querySelector("#imageInput").closest(".file-box").querySelector(".count").textContent);
    const musicMixSize = parseInt(document.querySelector("#musicInput").closest(".file-box").querySelector(".count").textContent);

    const imageShuffle = document.getElementById("imageShuffleCheck").checked;
    const musicShuffle = document.getElementById("musicShuffleCheck").checked;

    const imageFolder = document.getElementById("imageFolderCheck").checked;
    const musicFolder = document.getElementById("musicFolderCheck").checked;

    const payload = {
        image_config: {
            path: imagePaths,
            mix_size: imageMixSize,
            shuffle: imageShuffle,
            folder: imageFolder
        },
        music_config: {
            path: musicPaths,
            mix_size: musicMixSize,
            shuffle: musicShuffle,
            folder: musicFolder
        }
    };

    fetch("http://localhost:5000/import_files", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(data => console.log("Resposta da API:", data))
        .catch(error => console.error("Erro ao importar arquivos:", error));
}

// Adiciona o evento ao botão "Adicionar na sequencia"
function addFiles() {
    fetch("http://localhost:5000/add_files", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
    })
        .then(response => response.json())
        .then(data => console.log("Resposta da API:", data))
        .catch(error => console.error("Erro ao adicionar arquivos:", error));
}

// Adiciona o evento ao botão "Limpar sequencia"
function clearFilesBtn() {
    fetch("http://localhost:5000/clear", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
    })
        .then(response => response.json())
        .then(data => console.log("Resposta da API:", data))
        .catch(error => console.error("Erro ao limpar sequencia:", error));
};

// Adiciona o evento ao botão "Importar Arquivos"
document.getElementById("importFilesBtn").addEventListener("click", importFiles);

// Adiciona o evento ao botão "Adicionar na sequencia"
document.getElementById("addFilesBtn").addEventListener("click", addFiles);

// Adiciona o evento ao botão "Limpar sequencia"
document.getElementById("clearFilesBtn").addEventListener("click", clearFilesBtn);


// Função para atualizar os contadores de mix size
document.querySelectorAll('.file-box').forEach(fileBox => {
    let countElement = fileBox.querySelector('.count');
    let count = parseInt(countElement.textContent);

    fileBox.querySelector('.plus').addEventListener('click', () => {
        count++;
        countElement.textContent = count;
    });

    fileBox.querySelector('.minus').addEventListener('click', () => {
        if (count > 1) {
            count--;
            countElement.textContent = count;
        }
    });
});
