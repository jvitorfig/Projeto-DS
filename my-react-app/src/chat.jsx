import React from 'react';
import './App.css'; // Ou um CSS específico para o chat
import './chat.css';
import LogoImagem from "./assets/logo.png";
import PerfilImagem from "./assets/perfil.png";

function Chat() {
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
        <input type="text" id="chat" placeholder="Digite sua mensagem aqui" />
      </div>
    </div>
  );
}

// Este arquivo agora só exporta o Chat
export default Chat;