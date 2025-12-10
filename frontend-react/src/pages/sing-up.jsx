import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/login.css'; // 1. IMPORTANTE: Importa o mesmo CSS do Login
import logo from '../assets/logo.png'; 

// URL da sua API Flask
const API_URL = 'https://projeto-ds-qs25.onrender.com';

export default function SignUp() {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [confirmarSenha, setConfirmarSenha] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();
    setError('');

    if (senha !== confirmarSenha) {
      setError('As senhas não coincidem.');
      return;
    }

    fetch(`${API_URL}/api/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ nome, email, senha }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          navigate('/login'); 
        } else {
          setError(data.error || 'Ocorreu um erro ao cadastrar.');
        }
      })
      .catch((err) => {
        console.error('Erro de conexão:', err);
        setError('Não foi possível conectar ao servidor.');
      });
  };

  return (
    <div className="login-body">
      <form className="login-form" onSubmit={handleSubmit}>
        <header className="login-header">
          <img
            src={logo} 
            alt="Logo da Intellecta AI"
            width="150" height="150" 
          />

          <h1 id="titulo">Intellecta AI</h1>
          <p id="bemvindo">Crie sua conta gratuitamente.</p>
        </header>

        <div className="form-group">
          <label htmlFor="nome" className="h2">Nome Completo</label>
          <input
            type="text"
            id="nome"
            name="nome"
            className="input"
            placeholder="Digite seu nome completo"
            required
            value={nome}
            onChange={(e) => setNome(e.target.value)}
          />
        </div>

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
            placeholder="Crie uma senha"
            required
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label htmlFor="confirmar_senha" className="h2">Confirmar Senha</label>
          <input
            type="password"
            id="confirmar_senha"
            name="confirmar_senha"
            className="input"
            placeholder="Confirme sua senha"
            required
            value={confirmarSenha}
            onChange={(e) => setConfirmarSenha(e.target.value)}
          />
        </div>

        {error && <p style={{ color: 'red', fontSize: '0.9rem', marginBottom: '1rem' }}>{error}</p>}

        <button type="submit" id="botao">Cadastrar</button>

        <p id="semconta">
          Já tem uma conta?{' '}
          <a id="linkcadas" href="/login">Faça login</a>
        </p>
      </form>
    </div>
  );
}