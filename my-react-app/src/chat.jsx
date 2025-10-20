import React, { useState } from 'react';
import './App.css'; 
import './chat.css';
import LogoImagem from "./assets/logo.png";
import PerfilImagem from "./assets/perfil.png";

function Chat() {
  const [messages, setMessages] = useState([]); 
  const [currentMessage, setCurrentMessage] = useState('');

  // --- A GRANDE MUDANÇA É AQUI ---
  const handleSetMessage = async (event) => { // 1. Transforma a função em 'async'
    event.preventDefault();
    const userMessage = currentMessage.trim(); // 2. Guarda a mensagem do usuário

    if (userMessage === '') return; // Não faz nada se estiver vazio

    // 3. Adiciona a MENSAGEM DO USUÁRIO imediatamente à tela
    setMessages(prevMessages => [
      ...prevMessages, 
      { text: userMessage, sender: 'user' }
    ]);
    
    // 4. Limpa o input
    setCurrentMessage('');

    try {
      // 5. Envia a mensagem do usuário para o seu backend FastAPI
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: userMessage }), // Envia no formato { "text": "..." }
      });

      if (!response.ok) {
        throw new Error('Erro na resposta da API');
      }

      const data = await response.json(); // Pega a resposta JSON ({ "response": "..." })

      // 6. Adiciona a RESPOSTA DA IA à tela
      setMessages(prevMessages => [
        ...prevMessages,
        { text: data.response, sender: 'ai' } // 7. Usamos um sender 'ai'
      ]);

    } catch (error) {
      console.error("Erro ao conectar com o backend:", error);
      // Opcional: Adiciona uma mensagem de erro no chat
      setMessages(prevMessages => [
        ...prevMessages,
        { text: 'Não foi possível conectar ao servidor. Tente novamente.', sender: 'ai' }
      ]);
    }
  };
  return (
    <div className="chat-container">

      <div id="cabecalho">

        <div id="h1">
          <div>
            <img src={LogoImagem} width="30px" alt="Logo" />
          </div>
          
          <div id="titulo">Intellecta AI</div>
        </div>

        <div className="botoes">
          <button id="professor">Modo Professor</button>
          <button id="perfil">
            <img src={PerfilImagem} width="35px" height="35px" alt="Perfil"/>
          </button>
        </div>

      </div>
      <div className="corpo">
        <div className="messages-list">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender === 'user' ? 'user-message' : ''}`}>
              {message.text}
            </div>
          ))}
        </div>

        {/* Formulário de envio */}
        <form className="input-form" onSubmit={handleSetMessage}>
          <input 
            type="text" 
            id="chat" 
            placeholder="Digite sua mensagem aqui"
            value={currentMessage} // Conecta o valor do input ao estado
            onChange={(e) => setCurrentMessage(e.target.value)} // Atualiza o estado a cada tecla
          />
          <button type="submit">Enviar</button>
        </form>
      </div>
    </div>
  );
}

export default Chat;