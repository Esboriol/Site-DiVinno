async function fetchBotResponse(messageText) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000); // Timeout de 5 segundos

    try {
        const response = await fetch(`/search?prompt=${encodeURIComponent(messageText)}`, {
            signal: controller.signal,
        });

        const data = await response.json();
        clearTimeout(timeoutId); // Limpar o timeout se a resposta for recebida a tempo
        return data.message;
    } catch (error) {
        clearTimeout(timeoutId);
        console.error('Erro ao buscar dados:', error);
        if (error.name === 'AbortError') {
            return 'Desculpe, a resposta demorou muito. Tente novamente.';
        }
        return 'Desculpe, não consegui buscar uma resposta agora.';
    }
}

async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const chatWindow = document.getElementById('chatWindow');
    const messageText = userInput.value.trim();

    if (!messageText) {
        // Impede o envio se a mensagem estiver vazia
        const errorMessage = document.createElement('div');
        errorMessage.className = 'message bot';
        errorMessage.innerHTML = `<span>Por favor, digite algo antes de enviar.</span>`;
        chatWindow.appendChild(errorMessage);
        return;
    }

    const userMessage = document.createElement('div');
    userMessage.className = 'message user';
    userMessage.innerHTML = `<span>${messageText}</span>`;
    chatWindow.appendChild(userMessage);

    userInput.value = '';

    const loadingMessage = document.createElement('div');
    loadingMessage.className = 'message bot loading';
    loadingMessage.innerHTML = `<span>Carregando...</span>`;
    chatWindow.appendChild(loadingMessage);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    const botResponse = await fetchBotResponse(messageText);

    chatWindow.removeChild(loadingMessage);
    const botMessage = document.createElement('div');
    botMessage.className = 'message bot';
    botMessage.innerHTML = `<span>${botResponse}</span>`;
    chatWindow.appendChild(botMessage);

    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function checkEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Função para habilitar os links quando o usuário clicar em "Sim"
document.getElementById('yesBtn').addEventListener('click', () => {
    document.getElementById('cardapioLink').classList.remove('disabled-link');
    document.getElementById('contatoLink').classList.remove('disabled-link');
    document.getElementById('cardapioLink').style.pointerEvents = 'auto';
    document.getElementById('contatoLink').style.pointerEvents = 'auto';

    // Mudando a cor dos links para a cor original
    document.getElementById('cardapioLink').style.color = '#722F37';
    document.getElementById('contatoLink').style.color = '#722F37';
});