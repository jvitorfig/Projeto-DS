import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import LoginPage from './pages/LoginPage';
import ChatPage from './pages/ChatPage';
import SingPage from './pages/sing-up';
import Exercicio from './pages/Exercicios';
import Estatisticas from './pages/Estatisticas';

// Verificação de Login
const estaLogado = () => {
  return localStorage.getItem('isLoggedIn') === 'true';
};

function PrivateRoute({ children }) {
  return estaLogado() ? children : <Navigate to="/" />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />}/>
        <Route path="/sing-up" element={<SingPage/>} />
        <Route path="/login" element={<LoginPage/>} />
        
        {/* Rota de Exercícios */}
        <Route path="/exercicios" element={<Exercicio/>} />

        {/* Rota de Estatísticas (NOVA) */}
        <Route path="/estatisticas" element={<Estatisticas/>} />

        {/* Rota do Chat (Privada) */}
        <Route 
          path="/chat" 
          element={
            <PrivateRoute>
              <ChatPage />
            </PrivateRoute>
          } 
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;