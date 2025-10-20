import React, { useState } from 'react';
import './signup.css'; 
import LogoImagem from "./assets/logo.png";
import App from "./App.jsx";

function SignUp(){
    const [telaAtual, setTelaAtual] = useState('signup');

    const handleLogin = () => {
    setTelaAtual('login');
    };

    if (telaAtual == 'login'){
        return <App/>;
    }
    return(
    <div className="signup">
      <div><img src={LogoImagem} width="150px" height="150px" alt="Logo"/></div>
      <div id="titulo">Intellecta AI</div>
      <div id="bemvindo">Bem-vindo(a), Cadastre sua Conta!</div>

      {/*Colocar o nome completo aqui:*/}
      <div className="h2">Nome completo</div> 
      <input type="text" className="input" placeholder="Digite seu Nome" />

      {/*Colocar o username aqui*/}
      <div className="h2">Username</div>
      <input type="text" className="input" placeholder="Digite seu Nome de Usuário" />

      {/*Colocar o email aqui*/}
      <div className="h2">E-mail</div>
      <input type="text" className="input" placeholder="Digite seu E-mail" />

      {/*Colocar a senha aqui*/}
      <div className="h2">Senha</div>
      <input type="password" className="input" placeholder="Digite sua Senha" />

      <div> 
        <button id="botao" onClick={handleLogin}>Cadastrar</button>
      </div>
      <div id="comconta">Já tem uma conta? <a id="linkcadas" onClick={handleLogin}>Entrar</a></div>
    </div>
    );
}

export default SignUp;