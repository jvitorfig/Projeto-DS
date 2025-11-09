import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import ChatPage from './pages/ChatPage';
import SingPage from './pages/sing-up';

// (Opcional) Simula se o usuário está logado.
// Em um app real, isso viria de um estado, cookie ou localStorage.
const estaLogado = () => {
  // Por enquanto, vamos fingir que não está logado
  // Depois do login, você mudaria isso (ex: com localStorage)
  // Para testar o chat direto, mude para 'true'
  return localStorage.getItem('isLoggedIn') === 'true';
};

// Componente de Rota Privada
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
        <Route 
          path="/chat" 
          element={
            <PrivateRoute>
              <ChatPage />
            </PrivateRoute>
          } 
        />
        {/* Adicione outras rotas aqui */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
