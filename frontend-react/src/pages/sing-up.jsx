import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png'; 

const API_URL = 'http://127.0.0.1:5000';

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
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      {/* 6. Liga o formulário à função handleSubmit */}
      <form
        className="login-form bg-white p-8 rounded-2xl shadow-md w-full max-w-md"
        onSubmit={handleSubmit}
      >
        <header className="login-header flex flex-col items-center mb-6">
          <img
            src={logo} 
            alt="Logo da Intellecta AI"
            width="100"
            height="100"
          />

          <h1 id="titulo" className="text-2xl font-bold mt-4">
            Intellecta AI
          </h1>

          <p id="bemvindo" className="text-gray-600 text-center mt-2">
            Bem-vindo(a)! Crie sua conta gratuitamente.
          </p>
        </header>

        {/* 7. Conecta todos os inputs aos seus respectivos estados */}
        <div className="form-group mb-4">
          <label htmlFor="nome" className="h2 block font-medium mb-1">
            Nome Completo
          </label>
          <input
            type="text"
            id="nome"
            name="nome"
            className="input w-full border rounded-lg p-2"
            placeholder="Digite seu nome completo"
            required
            value={nome}
            onChange={(e) => setNome(e.target.value)}
          />
        </div>

        <div className="form-group mb-4">
          <label htmlFor="email" className="h2 block font-medium mb-1">
            E-mail
          </label>
          <input
            type="email"
            id="email"
            name="email"
            className="input w-full border rounded-lg p-2"
            placeholder="Digite seu E-mail"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div className="form-group mb-4">
          <label htmlFor="senha" className="h2 block font-medium mb-1">
            Senha
          </label>
          <input
            type="password"
            id="senha"
            name="senha"
            className="input w-full border rounded-lg p-2"
            placeholder="Crie uma senha"
            required
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
          />
        </div>

        <div className="form-group mb-6">
          <label htmlFor="confirmar_senha" className="h2 block font-medium mb-1">
            Confirmar Senha
          </label>
          <input
            type="password"
            id="confirmar_senha"
            name="confirmar_senha"
            className="input w-full border rounded-lg p-2"
            placeholder="Confirme sua senha"
            required
            value={confirmarSenha}
            onChange={(e) => setConfirmarSenha(e.target.value)}
          />
        </div>

        {/* 8. Exibe a mensagem de erro */}
        {error && <p style={{ color: 'red', fontSize: '0.9rem', textAlign: 'center', marginBottom: '1rem' }}>{error}</p>}

        <button
          type="submit"
          id="botao"
          className="w-full bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 transition"
        >
          Cadastrar
        </button>

        <p id="semconta" className="text-center mt-4">
          Já tem uma conta?{' '}
          <a
            id="linkcadas"
            href="/login" 
            className="text-blue-600 hover:underline"
          >
            Faça login
          </a>
        </p>
      </form>
    </div>
  );
}