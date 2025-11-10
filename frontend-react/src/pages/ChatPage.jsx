import React, { useState, useEffect, useRef } from 'react';
import '../styles/chat.css'; // Importa o CSS de chat
import logo from '../assets/logo.png'; // Importa o logo
import perfil from '../assets/perfil.png'; // Importa o perfil

// URL da sua API Flask
const API_URL = 'http://127.0.0.1:5000';

function ChatPage() {
  const [messages, setMessages] = useState([]); // Guarda o histórico de msgs
  const [input, setInput] = useState(''); // Controla o input
  const chatContainerRef = useRef(null); // Para rolar o chat para baixo

  // 1. Busca a primeira mensagem do bot quando a página carrega
  useEffect(() => {
    fetch(`${API_URL}/api/initial-message`)
      .then(response => response.json())
      .then(data => {
        setMessages([{ sender: 'bot', text: data.message }]);
      })
      .catch(err => {
        console.error('Erro ao buscar msg inicial:', err);
        setMessages([{ sender: 'bot', text: 'Erro ao conectar. Tente recarregar.' }]);
      });
  }, []); // O [] vazio faz isso rodar só uma vez

  // 2. Efeito para rolar o chat para baixo sempre que 'messages' mudar
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  // 3. Função chamada ao enviar o formulário
  const handleSubmit = (event) => {
    event.preventDefault();
    const userMessage = input.trim();

    if (userMessage) {
      // 3.1. Adiciona a mensagem do usuário ao estado
      const newUserMessage = { sender: 'user', text: userMessage };
      setMessages(prevMessages => [...prevMessages, newUserMessage]);
      setInput(''); // Limpa o input

      // 3.2. Envia a mensagem para a API Flask
      fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage })
      })
      .then(response => response.json())
      .then(data => {
        // 3.3. Recebe a resposta do bot e adiciona ao estado
        let botMessageText = '';
        if (data.response) {
          botMessageText = data.response;
        } else if (data.error) {
          botMessageText = 'Desculpe, ocorreu um erro: ' + data.error;
        }
        const newBotMessage = { sender: 'bot', text: botMessageText };
        setMessages(prevMessages => [...prevMessages, newBotMessage]);
      })
      .catch(error => {
        console.error('Erro no fetch:', error);
        const errorBotMessage = { sender: 'bot', text: 'Desculpe, não consegui me conectar.' };
        setMessages(prevMessages => [...prevMessages, errorBotMessage]);
      });
    }
  };

  return (
    <>
      <header id="cabecalho">
        <a href="#" className="brand-link" id="h1">
          <img src={logo} alt="Logo da Intellecta AI" width="30" height="30" />
          <span id="titulo">Intellecta AI</span>
        </a>
        <nav className="botoes">
          <a href="/exercicios" id="professor" className="nav-button">Questões</a>
          <a href="#" id="perfil" className="nav-profile" title="Ver perfil">
            <img src={perfil} alt="Ver perfil" width="35" height="35" />
          </a>
        </nav>
      </header>

      <main className="corpo">
        <div id="chat-container" ref={chatContainerRef}>
          {/* 4. Renderiza a lista de mensagens */}
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}-message`}>
              <p>{msg.text}</p>
            </div>
          ))}
        </div>

        <form className="chat-form" onSubmit={handleSubmit}>
          <label htmlFor="chat-input" className="visually-hidden">Digite sua mensagem:</label>
          <input
            type="text"
            id="chat-input"
            name="message"
            placeholder="Digite sua mensagem aqui"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button type="submit" id="send-button" aria-label="Enviar mensagem">
            &rarr;
          </button>
        </form>
      </main>
    </>
  );
}

export default ChatPage;
