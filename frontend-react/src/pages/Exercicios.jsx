import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import ReactMarkdown from "react-markdown";
import '../styles/exercicios.css'; 

export default function ExercicioAI() {
  const [topic, setTopic] = useState("");
  const [exercise, setExercise] = useState("");
  const [answer, setAnswer] = useState("");
  const [correction, setCorrection] = useState("");
  const [loadingExercise, setLoadingExercise] = useState(false);
  const [loadingCorrection, setLoadingCorrection] = useState(false);

  const navigate = useNavigate();

  const gerarExercicio = async () => {
    if (!topic.trim()) return;

    setLoadingExercise(true);
    setExercise("");
    setCorrection("");
    setAnswer("");

    try {
      const response = await fetch("http://127.0.0.1:5000/api/generate-exercise", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic }),
      });

      const data = await response.json();
      setExercise(data.exercise || "Erro ao gerar exercício.");
    } catch (err) {
      console.error(err);
      setExercise("Erro ao gerar exercício. Tente novamente.");
    }

    setLoadingExercise(false);
  };

  const corrigirExercicio = async () => {
    if (!answer.trim()) return;

    setLoadingCorrection(true);
    setCorrection("");

    try {
      const response = await fetch("http://127.0.0.1:5000/api/correct-exercise", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ exercise, answer }),
      });

      const data = await response.json();
      setCorrection(data.correction || "Erro ao corrigir.");
    } catch (err) {
      console.error(err);
      setCorrection("Erro ao corrigir. Tente novamente.");
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
          Criador e Corretor de Exercícios — <span>Intellecta AI</span>
        </h1>

        <p className="ex-subtitle">
          Gere exercícios personalizados com IA e envie sua resposta para correção automática.
        </p>

        <label className="ex-label">Tópico do Exercício</label>
        <input
          type="text"
          className="ex-input"
          placeholder="Ex: Derivadas, Matrizes, Probabilidade..."
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        />

        <button
          onClick={gerarExercicio}
          disabled={loadingExercise}
          className="ex-btn"
        >
          {loadingExercise ? "Gerando exercício..." : "Gerar Exercício"}
        </button>

        {exercise && (
          <div className="ex-section">
            <h3 className="ex-section-title">Exercício Gerado</h3>
            <div className="ex-box"><ReactMarkdown>{exercise}</ReactMarkdown></div>
          </div>
        )}

        {exercise && (
          <>
            <h2 className="ex-section-title">Sua Resposta</h2>

            <textarea
              className="ex-textarea"
              placeholder="Digite sua resposta aqui..."
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
            />

            <button
              onClick={corrigirExercicio}
              disabled={loadingCorrection}
              className="ex-btn purple"
            >
              {loadingCorrection ? "Corrigindo..." : "Enviar para Correção"}
            </button>
          </>
        )}

        {correction && (
          <div className="ex-section">
            <h3 className="ex-section-title">Correção</h3>
            <div className="ex-box">{correction}</div>
          </div>
        )}

      </div>
    </div>
  );
}
