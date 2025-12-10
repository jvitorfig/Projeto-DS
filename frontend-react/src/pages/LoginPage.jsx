import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/login.css'; // Importa o CSS
import logo from '../assets/logo.png'; // Importa a imagem

// URL da sua API Flask
const API_URL = 'https://projeto-ds-qs25.onrender.com';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    // 1. Previne o recarregamento da página
    event.preventDefault(); 
    setError(''); // Limpa erros antigos

    // 2. Envia os dados para a API Flask
    fetch(`${API_URL}/api/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, senha }),
    })
    .then(response => response.json())
    .then(data => {
      // 3. Processa a resposta
      if (data.success) {
        localStorage.setItem('isLoggedIn', 'true');
        localStorage.setItem('userId', data.user.id);   // Salva o ID
        localStorage.setItem('userName', data.user.nome); // Salva o Nome 
        
        console.log("Login salvo para ID:", data.user.id); // Debug
        navigate('/chat'); 
      } else {
        setError(data.error || 'Ocorreu um erro.');
      }
    })
    .catch(err => {
      console.error('Erro de conexão:', err);
      setError('Não foi possível conectar ao servidor.');
    });
  };

  return (
    <div className="login-body">
    <form className="login-form" onSubmit={handleSubmit}>
      <header className="login-header">
        <img src={logo} alt="Logo da Intellecta AI" width="150" height="150" />
        <h1 id="titulo">Intellecta AI</h1>
        <p id="bemvindo">Bem-vindo(a) de volta! Faça login em sua conta.</p>
      </header>

      <div className="form-group">
        <label htmlFor="email" className="h2">E-mail</label>
        <input
          type="email"
          id="email"
          name="email"
          className="input"
          placeholder="Digite seu E-mail"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>

      <div className="form-group">
        <label htmlFor="senha" className="h2">Senha</label>
        <input
          type="password"
          id="senha"
          name="senha"
          className="input"
          placeholder="Digite sua Senha"
          required
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
        />
      </div>

      <p id="forgot">
        <a href="#" id="link_forgot">Esqueceu a senha?</a>
      </p>

      {error && <p style={{color: 'red', fontSize: '0.9rem'}}>{error}</p>}

      <button type="submit" id="botao">Entrar</button>

      <p id="semconta">
        Não tem uma conta? <a id="linkcadas" href="/sing-up">Cadastre-se</a>
      </p>
    </form>
    </div>
  );
}

export default LoginPage;
