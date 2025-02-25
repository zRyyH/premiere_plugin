// =============================
// VARIÁVEIS GLOBAIS
// =============================
let selectedImages = [];
let selectedMusic = [];

// Aba de imagens e botões
const imageRow = document.getElementById("imageRow");
const loadImagesBtn = document.getElementById("loadImagesBtn");
const importImagesBtn = document.getElementById("importImagesBtn");
const addImagesBtn = document.getElementById("addImagesBtn");
const clearImagesBtn = document.getElementById("clearImagesBtn");

// Indicadores de imagens (agora dentro dos botões, mas ainda referenciados aqui)
const imgBrowseIndicator = document.getElementById("imgBrowseIndicator");
const imgLoadIndicator   = document.getElementById("imgLoadIndicator");
const imgImportIndicator = document.getElementById("imgImportIndicator");
const imgAddIndicator    = document.getElementById("imgAddIndicator");
const imgClearIndicator  = document.getElementById("imgClearIndicator");

// Aba de músicas e botões
const loadMusicsBtn   = document.getElementById("loadMusicsBtn");
const importMusicsBtn = document.getElementById("importMusicsBtn");
const addMusicsBtn    = document.getElementById("addMusicsBtn");
const clearMusicsBtn  = document.getElementById("clearMusicsBtn");

// Indicadores de músicas
const mscBrowseIndicator = document.getElementById("mscBrowseIndicator");
const mscLoadIndicator   = document.getElementById("mscLoadIndicator");
const mscImportIndicator = document.getElementById("mscImportIndicator");
const mscAddIndicator    = document.getElementById("mscAddIndicator");
const mscClearIndicator  = document.getElementById("mscClearIndicator");

// =============================
// FUNÇÕES DE HABILITAR / DESABILITAR
// =============================
function disableImageRow() {
  imageRow.classList.add("disabled");
}
function enableImageRow() {
  imageRow.classList.remove("disabled");
}

// Desabilita SOMENTE Importar e Adicionar Imagens
function setImportAddImagesDisabled(disabled) {
  importImagesBtn.disabled = disabled;
  addImagesBtn.disabled = disabled;
}

// Verifica se podemos habilitar "Limpar Imagens"
function updateClearImagesAvailability() {
  // Limpar Imagens deve estar disponível se houver pelo menos 1 música.
  clearImagesBtn.disabled = (selectedMusic.length === 0);
}

// =============================
// FUNÇÕES - ÚLTIMO BOTÃO CLICADO
// =============================
function resetAllImageIndicators() {
  imgBrowseIndicator.classList.remove("active");
  imgLoadIndicator.classList.remove("active");
  imgImportIndicator.classList.remove("active");
  imgAddIndicator.classList.remove("active");
  imgClearIndicator.classList.remove("active");
}

function markLastClickedImageButton(btnId) {
  resetAllImageIndicators();
  if (btnId === "browseImagesBtn") {
    imgBrowseIndicator.classList.add("active");
  } else if (btnId === "loadImagesBtn") {
    imgLoadIndicator.classList.add("active");
  } else if (btnId === "importImagesBtn") {
    imgImportIndicator.classList.add("active");
  } else if (btnId === "addImagesBtn") {
    imgAddIndicator.classList.add("active");
  } else if (btnId === "clearImagesBtn") {
    imgClearIndicator.classList.add("active");
  }
}

function resetAllMusicIndicators() {
  mscBrowseIndicator.classList.remove("active");
  mscLoadIndicator.classList.remove("active");
  mscImportIndicator.classList.remove("active");
  mscAddIndicator.classList.remove("active");
  mscClearIndicator.classList.remove("active");
}

function markLastClickedMusicButton(btnId) {
  resetAllMusicIndicators();
  if (btnId === "browseMusicsBtn") {
    mscBrowseIndicator.classList.add("active");
  } else if (btnId === "loadMusicsBtn") {
    mscLoadIndicator.classList.add("active");
  } else if (btnId === "importMusicsBtn") {
    mscImportIndicator.classList.add("active");
  } else if (btnId === "addMusicsBtn") {
    mscAddIndicator.classList.add("active");
  } else if (btnId === "clearMusicsBtn") {
    mscClearIndicator.classList.add("active");
  }
}

// =============================
// AUXILIARES DE SELEÇÃO
// =============================
function getSelectedFolderName(inputId) {
  const inputElement = document.getElementById(inputId);
  const files = Array.from(inputElement.files);
  if (files.length > 0) {
    const path = files[0].webkitRelativePath || files[0].path || files[0].name;
    const splitted = path.split(/[/\\]/);
    return splitted[0] || "Nenhuma pasta detectada";
  }
  return "Nenhuma pasta detectada";
}

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

function openFileSelector(inputId, checkboxId) {
  let checkbox = document.getElementById(checkboxId);
  toggleFileInput(inputId, checkbox.checked);
  document.getElementById(inputId).click();
}

function getSelectedFiles(inputId) {
  const inputElement = document.getElementById(inputId);
  const files = Array.from(inputElement.files);
  return files.map(file => file.path || file.webkitRelativePath || file.name);
}

// =============================
// LISTAS NA TELA
// =============================
function renderLists() {
  const imageList = document.getElementById("imageList");
  const musicList = document.getElementById("musicList");
  imageList.innerHTML = "";
  musicList.innerHTML = "";

  // Imagens
  selectedImages.forEach((imageName) => {
    const li = document.createElement("li");
    li.textContent = imageName;
    imageList.appendChild(li);
  });

  // Músicas
  selectedMusic.forEach((musicName) => {
    const li = document.createElement("li");
    li.textContent = musicName;
    musicList.appendChild(li);
  });
}

// =============================
// IMAGENS
// =============================
function loadImages() {
  const imagePaths = getSelectedFiles("imageInput");
  const imageMixSize = parseInt(
    document
      .querySelector("#imageInput")
      .closest(".file-box")
      .querySelector(".count").textContent
  );
  const imageShuffle = document.getElementById("imageShuffleCheck").checked;
  const imageFolder = document.getElementById("imageFolderCheck").checked;

  const payload = {
    image_config: {
      path: imagePaths,
      mix_size: imageMixSize,
      shuffle: imageShuffle,
      folder: imageFolder
    }
  };

  fetch("http://localhost:5000/load_images", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(response => response.json())
    .then(data => {
      console.log("Resposta (load_images):", data);
      if (data.image_names) {
        selectedImages = data.image_names;
      }

      // Nome da pasta
      document.getElementById("imageFolderName").textContent = "";
      if (imageFolder) {
        const folderName = getSelectedFolderName("imageInput");
        document.getElementById("imageFolderName").textContent =
          "Pasta Selecionada: " + folderName;
      }
      renderLists();

      // Após carregar, habilita Importar e Adicionar
      setImportAddImagesDisabled(false);

      // E atualiza disponibilidade do "Limpar Imagens"
      updateClearImagesAvailability();
    })
    .catch(error => console.error("Erro ao carregar imagens:", error));
}

function importImages() {
  fetch("http://localhost:5000/import_images")
    .then(response => response.json())
    .then(data => {
      console.log("Resposta (import_images):", data);
    })
    .catch(error => console.error("Erro ao importar imagens:", error));
}

function addImages() {
  fetch("http://localhost:5000/add_images")
    .then(response => response.json())
    .then(data => {
      console.log("Resposta (add_images):", data);
    })
    .catch(error => console.error("Erro ao adicionar imagens:", error));
}

function clearImages() {
  fetch("http://localhost:5000/clear_images")
    .then(response => response.json())
    .then(data => {
      console.log("Resposta (clear_images):", data);
      selectedImages = [];
      renderLists();
    })
    .catch(error => console.error("Erro ao limpar imagens:", error));
}

// =============================
// MÚSICAS
// =============================
function loadMusics() {
  const musicPaths = getSelectedFiles("musicInput");
  const musicMixSize = parseInt(
    document
      .querySelector("#musicInput")
      .closest(".file-box")
      .querySelector(".count").textContent
  );
  const musicShuffle = document.getElementById("musicShuffleCheck").checked;
  const musicFolder = document.getElementById("musicFolderCheck").checked;

  const payload = {
    music_config: {
      path: musicPaths,
      mix_size: musicMixSize,
      shuffle: musicShuffle,
      folder: musicFolder
    }
  };

  fetch("http://localhost:5000/load_musics", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(response => response.json())
    .then(data => {
      console.log("Resposta (load_musics):", data);
      if (data.music_names) {
        selectedMusic = data.music_names;
      }

      // Nome da pasta
      document.getElementById("musicFolderName").textContent = "";
      if (musicFolder) {
        const folderName = getSelectedFolderName("musicInput");
        document.getElementById("musicFolderName").textContent =
          "Pasta Selecionada: " + folderName;
      }

      renderLists();

      // Se temos música, habilita a aba de imagens
      if (selectedMusic.length > 0) {
        enableImageRow();
        // "Carregar Imagens" sempre livre se tem música
        loadImagesBtn.disabled = false; 
      }
      // E atualiza se "Limpar Imagens" pode ficar habilitado
      updateClearImagesAvailability();
    })
    .catch(error => console.error("Erro ao carregar músicas:", error));
}

function importMusics() {
  fetch("http://localhost:5000/import_musics")
    .then(response => response.json())
    .then(data => {
      console.log("Resposta (import_musics):", data);
    })
    .catch(error => console.error("Erro ao importar músicas:", error));
}

function addMusics() {
  fetch("http://localhost:5000/add_musics")
    .then(response => response.json())
    .then(data => {
      console.log("Resposta (add_musics):", data);
      // Ao adicionar músicas, desabilitamos SOMENTE "Importar" e "Adicionar" Imagens
      setImportAddImagesDisabled(true);

      // "Limpar Imagens" continua disponível se já houver música
      updateClearImagesAvailability();
    })
    .catch(error => console.error("Erro ao adicionar músicas:", error));
}

function clearMusics() {
  fetch("http://localhost:5000/clear_musics")
    .then(response => response.json())
    .then(data => {
      console.log("Resposta (clear_musics):", data);
      selectedMusic = [];
      renderLists();

      // Se não há mais música, desabilita novamente a aba de imagens
      disableImageRow();
      loadImagesBtn.disabled = true;

      // Importar/Adicionar Imagens desabilitados
      setImportAddImagesDisabled(true);

      // E "Limpar Imagens" fica desabilitado
      updateClearImagesAvailability();
    })
    .catch(error => console.error("Erro ao limpar músicas:", error));
}

// =============================
// AJUSTE DE CONTADORES (+/-)
// =============================
document.querySelectorAll(".file-box").forEach(fileBox => {
  let countElement = fileBox.querySelector(".count");
  let count = parseInt(countElement.textContent);

  fileBox.querySelector(".plus").addEventListener("click", () => {
    count++;
    countElement.textContent = count;
  });

  fileBox.querySelector(".minus").addEventListener("click", () => {
    if (count > 1) {
      count--;
      countElement.textContent = count;
    }
  });
});

// Inicia desabilitada a parte de imagens
disableImageRow();
