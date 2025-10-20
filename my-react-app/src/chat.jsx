import React, { useState } from 'react';
import './App.css'; 
import './chat.css';
import LogoImagem from "./assets/logo.png";
import PerfilImagem from "./assets/perfil.png";

function Chat() {

  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState("");

  const handleSetMessage = (event) => {
    event.preventDefault();

  if (currentMessage.trim() !== "") {
    setMessages([...messages, {text: currentMessage, sender: "user"}]);

    setCurrentMessage("")
  }
  }
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