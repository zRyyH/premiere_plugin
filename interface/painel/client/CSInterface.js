/*************************************************************************
 * CSInterface.js - Interface de comunicação com Adobe CEP
 * Este script conecta o painel HTML ao Adobe Premiere (ou outros produtos Adobe)
 *************************************************************************/

/**
 * Classe CSInterface.
 * Oferece funções para comunicação entre o HTML e o Adobe ExtendScript (JSX).
 */
function CSInterface() {
    this.hostEnvironment = this.getHostEnvironment();
}

/**
 * Retorna informações sobre o ambiente do host (por exemplo, versão do aplicativo Adobe).
 */
CSInterface.prototype.getHostEnvironment = function () {
    return JSON.parse(window.__adobe_cep__.getHostEnvironment());
};

/**
 * Executa um script JSX no Adobe Premiere e retorna o resultado.
 * @param {string} script - Script JSX a ser executado.
 * @param {function} callback - Função de callback com o resultado.
 */
CSInterface.prototype.evalScript = function (script, callback) {
    if (!callback) {
        callback = function () {};
    }
    window.__adobe_cep__.evalScript(script, callback);
};

/**
 * Define um evento customizado para escutar mensagens do Adobe CEP.
 * @param {string} eventType - Tipo de evento a ser escutado.
 * @param {function} callback - Função de callback quando o evento for disparado.
 */
CSInterface.prototype.addEventListener = function (eventType, callback) {
    window.__adobe_cep__.addEventListener(eventType, callback);
};

/**
 * Remove um evento customizado previamente adicionado.
 * @param {string} eventType - Tipo de evento a ser removido.
 * @param {function} callback - Função de callback associada ao evento.
 */
CSInterface.prototype.removeEventListener = function (eventType, callback) {
    window.__adobe_cep__.removeEventListener(eventType, callback);
};

/**
 * Envia um evento customizado para o Adobe CEP.
 * @param {string} eventType - Tipo de evento.
 * @param {string} data - Dados a serem enviados no evento.
 */
CSInterface.prototype.dispatchEvent = function (eventType, data) {
    var event = new CSEvent(eventType, 'APPLICATION');
    event.data = data;
    window.__adobe_cep__.dispatchEvent(event);
};
