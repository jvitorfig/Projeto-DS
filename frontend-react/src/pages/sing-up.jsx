import React from "react";

export default function SignUp() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <form
        className="login-form bg-white p-8 rounded-2xl shadow-md w-full max-w-md"
        action="/cadastro"
        method="post"
      >
        <header className="login-header flex flex-col items-center mb-6">
          <img
            src="src/assets/logo.png"
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
          />
        </div>

        <button
          type="submit"
          id="botao"
          className="w-full bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 transition"
        >
          Cadastrar
        </button>

        <p id="semconta" className="text-center mt-4">
          Já tem uma conta?{" "}
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
