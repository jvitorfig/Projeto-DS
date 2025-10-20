import { useState } from 'react';
import './App.css';
import Chat from "./chat.jsx";
import LogoImagem from "./assets/logo.png";
import SignUp from "./signup.jsx";

function App() {
  const [telaAtual, setTelaAtual] = useState('login');

  const handleLogin = () => {
    setTelaAtual('chat');
  };

  const handleSignUp = () => {
    setTelaAtual('signup')
  }

  if (telaAtual == 'chat') {
    return <Chat />;
  }

  if (telaAtual == 'signup') {
    return <SignUp/>;
  }
  return (
    <div className="login">
      <div><img src={LogoImagem} width="150px" height="150px" alt="Logo"/></div>
      <div id="titulo">Intellecta AI</div>
      <div id="bemvindo">Bem-vindo(a) de volta! Faça login em sua conta.</div>
      <div className="h2">E-mail</div>
      <input type="text" className="input" placeholder="Digite seu E-mail" />
      <div className="h2">Senha</div>
      <input type="password" className="input" placeholder="Digite sua Senha" />
      <div id="forgot"><a href="#" id="link_forgot">Esqueceu a senha?</a></div>
      <div> 
        <button id="botao" onClick={handleLogin}>Entrar</button>
      </div>
      <div id="semconta">Não tem uma conta? <a id="signup" onClick={handleSignUp}>Cadastre-se</a></div>
    </div>
  );
}

// Agora este arquivo só tem UMA exportação padrão. ✅
export default App;