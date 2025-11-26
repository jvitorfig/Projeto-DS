import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, CheckCircle, XCircle } from "lucide-react"; // Adicionei ícones opcionais
import ReactMarkdown from "react-markdown";
import '../styles/exercicios.css';

export default function ExercicioAI() {
  const [topic, setTopic] = useState("");
  
  // O exercício agora é um objeto (ou null), não uma string vazia
  const [exerciseData, setExerciseData] = useState(null); 
  
  const [selectedAnswer, setSelectedAnswer] = useState(""); // Qual botão o usuário clicou
  const [correction, setCorrection] = useState(null); // Correção agora pode ser objeto também
  
  const [loadingExercise, setLoadingExercise] = useState(false);
  const [loadingCorrection, setLoadingCorrection] = useState(false);

  // IMPORTANTE: Idealmente você pega isso do contexto de autenticação/Login
  const userId = 1; 

  const navigate = useNavigate();

  // ✅ GERAR EXERCÍCIO (MÚLTIPLA ESCOLHA)
  const gerarExercicio = async () => {
    if (!topic.trim()) return;

    setLoadingExercise(true);
    setExerciseData(null); // Reseta o exercício anterior
    setCorrection(null);   // Reseta a correção anterior
    setSelectedAnswer(""); // Reseta a seleção

    try {
      const response = await fetch("http://127.0.0.1:5000/api/generate-exercise", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic }),
      });

      const data = await response.json();
      
      // Se a API retornar erro ou não tiver as chaves certas
      if (data.error) {
        alert("Erro na IA: " + data.error);
      } else {
        // Salva o objeto completo (enunciado + alternativas)
        setExerciseData(data);
      }
      
    } catch (err) {
      console.error(err);
      alert("Erro ao conectar com o servidor.");
    }

    setLoadingExercise(false);
  };

  // ✅ CORRIGIR EXERCÍCIO
  const corrigirExercicio = async () => {
    if (!selectedAnswer) {
      alert("Por favor, selecione uma alternativa.");
      return;
    }

    setLoadingCorrection(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/correct-exercise", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          exercise: exerciseData, // Envia o objeto todo da questão
          answer: selectedAnswer, // Envia a letra/texto escolhido
          user_id: userId         // Necessário para salvar no banco
        }),
      });

      const data = await response.json();
      setCorrection(data); // Salva a resposta da correção (nota, acertou, texto)
      
    } catch (err) {
      console.error(err);
      alert("Erro ao corrigir.");
    }

    setLoadingCorrection(false);
  };

  return (
    <div className="ex-page">
      <div className="ex-container">

        <button className="ex-back-btn" onClick={() => navigate("/chat")}>
          <ArrowLeft size={20} /> Voltar ao Chat
        </button>

        <h1 className="ex-title">
          Praticar com <span>Intellecta AI</span>
        </h1>

        <p className="ex-subtitle">
          Escolha um tópico e teste seus conhecimentos com questões de múltipla escolha.
        </p>

        {/* INPUT DE TÓPICO */}
        <div className="input-group">
            <label className="ex-label">Sobre o que você quer estudar?</label>
            <div style={{ display: 'flex', gap: '10px' }}>
                <input
                type="text"
                className="ex-input"
                placeholder="Ex: Revolução Francesa, Ponteiros em C, Logaritmos..."
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                />
                <button
                onClick={gerarExercicio}
                disabled={loadingExercise}
                className="ex-btn"
                style={{ width: 'auto', whiteSpace: 'nowrap' }}
                >
                {loadingExercise ? "Gerando..." : "Gerar Questão"}
                </button>
            </div>
        </div>

        <hr className="divider" />

        {/* ÁREA DO EXERCÍCIO */}
        {exerciseData && (
          <div className="ex-section animate-fade-in">
            <h3 className="ex-section-title">Questão:</h3>
            
            {/* Enunciado */}
            <div className="ex-box enunciado">
                <ReactMarkdown>{exerciseData.enunciado}</ReactMarkdown>
            </div>

            {/* Alternativas (Botões) */}
            <div className="alternativas-container">
                {exerciseData.alternativas && exerciseData.alternativas.map((alt, index) => (
                    <button 
                        key={index} 
                        className={`alt-btn ${selectedAnswer === alt ? 'selected' : ''}`}
                        onClick={() => !correction && setSelectedAnswer(alt)} // Trava clique se já corrigiu
                        disabled={!!correction} // Desabilita botões após corrigir
                    >
                        {alt}
                    </button>
                ))}
            </div>

            {/* Botão de Enviar (Só aparece se não tiver corrigido ainda) */}
            {!correction && (
                <button
                onClick={corrigirExercicio}
                disabled={loadingCorrection || !selectedAnswer}
                className="ex-btn purple"
                style={{ marginTop: '20px' }}
                >
                {loadingCorrection ? "Corrigindo..." : "Confirmar Resposta"}
                </button>
            )}
          </div>
        )}

        {/* ÁREA DA CORREÇÃO */}
        {correction && (
          <div className={`ex-section correction-box ${correction.acertou ? 'success' : 'error'}`}>
            <h3 className="ex-section-title" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                {correction.acertou ? <CheckCircle color="green"/> : <XCircle color="red"/>}
                {correction.acertou ? "Você Acertou!" : "Não foi dessa vez..."}
            </h3>
            
            <p><strong>Nota:</strong> {correction.nota}/10</p>
            
            <div className="ex-box" style={{ background: 'transparent', border: 'none', padding: '0' }}>
                <ReactMarkdown>{correction.correction || correction.correcao_detalhada}</ReactMarkdown>
            </div>
            
            <button onClick={gerarExercicio} className="ex-btn" style={{ marginTop: '15px' }}>
                Próxima Questão
            </button>
          </div>
        )}

      </div>
    </div>
  );
}