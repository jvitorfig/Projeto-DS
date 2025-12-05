import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, CheckCircle, XCircle } from "lucide-react";
import ReactMarkdown from "react-markdown";
import '../styles/exercicios.css';

export default function ExercicioAI() {
  const [topic, setTopic] = useState("");
  const [exerciseData, setExerciseData] = useState(null); 
  
  // MUDANÇA 1: Usamos null para "nenhuma selecionada" e números (0-4) para as opções
  const [selectedAnswerIndex, setSelectedAnswerIndex] = useState(null);
  
  const [correction, setCorrection] = useState(null);
  const [loadingExercise, setLoadingExercise] = useState(false);
  const [loadingCorrection, setLoadingCorrection] = useState(false);
  const navigate = useNavigate();

  const userId = localStorage.getItem('userId');
  
  useEffect(() => {
      if (!userId) {
          navigate("/login");
      }
    }, [userId, navigate]);

  // ✅ GERAR EXERCÍCIO
  const gerarExercicio = async () => {
    if (!topic.trim()) return;

    setLoadingExercise(true);
    setExerciseData(null);
    setCorrection(null);
    setSelectedAnswerIndex(null); // Reseta a seleção

    try {
      const response = await fetch("http://127.0.0.1:5000/api/generate-exercise", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic }),
      });

      const data = await response.json();
      
      if (data.error) {
        alert("Erro na IA: " + data.error);
      } else {
        setExerciseData(data);
      }
      
    } catch (err) {
      console.error(err);
      alert("Erro ao conectar com o servidor.");
    }

    setLoadingExercise(false);
  };

  // ✅ CORRIGIR EXERCÍCIO (Lógica Nova baseada em índices)
  const corrigirExercicio = async () => {
    // Validação estrita: null significa que não escolheu. 0 é uma escolha válida (Letra A)
    if (selectedAnswerIndex === null) {
      alert("Por favor, selecione uma alternativa.");
      return;
    }

    setLoadingCorrection(true);

    try {
      // MUDANÇA 2: Enviamos o objeto exercise completo e o índice escolhido
      const payload = { 
        exercise: exerciseData,
        answer_text: exerciseData.alternativas[selectedAnswerIndex], // Texto para salvar no histórico
        answer_index: selectedAnswerIndex, // Índice para validação lógica
        user_id: userId,
        topic: topic 
      };

      const response = await fetch("http://127.0.0.1:5000/api/correct-exercise", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();
      setCorrection(data);
      
    } catch (err) {
      console.error(err);
      alert("Erro ao corrigir.");
    }

    setLoadingCorrection(false);
  };

  return (
    <div className="ex-page">
      <div className="ex-container">

        {/* Botão para ver estatísticas */}
        <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '20px'}}>
            <button className="ex-back-btn" onClick={() => navigate("/chat")}>
                <ArrowLeft size={20} /> Voltar
            </button>
            <button className="ex-back-btn" onClick={() => navigate("/estatisticas")} style={{backgroundColor: '#646cff', color: 'white', border: 'none'}}>
                Ver Minhas Estatísticas 📊
            </button>
        </div>

        <h1 className="ex-title">
          Praticar com <span>Intellecta AI</span>
        </h1>

        <div className="input-group">
            <label className="ex-label">Sobre o que você quer estudar?</label>
            <div style={{ display: 'flex', gap: '10px' }}>
                <input
                type="text"
                className="ex-input"
                placeholder="Ex: Revolução Francesa, Ponteiros em C..."
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

        {exerciseData && (
          <div className="ex-section animate-fade-in">
            <h3 className="ex-section-title">Questão:</h3>
            
            <div className="ex-box enunciado">
                <ReactMarkdown>{exerciseData.enunciado}</ReactMarkdown>
            </div>

            <div className="alternativas-container">
                {exerciseData.alternativas && exerciseData.alternativas.map((alt, index) => {
                    // Lógica para definir as cores dos botões
                    let btnClass = 'alt-btn';
                    
                    if (correction) {
                        // Se já corrigiu:
                        if (index === exerciseData.indice_correta) {
                            btnClass += ' correct-answer-highlight'; // A correta fica VERDE
                        } else if (selectedAnswerIndex === index && !correction.acertou) {
                            btnClass += ' wrong-answer-highlight'; // A errada que você clicou fica VERMELHA
                        }
                    } else {
                        // Se ainda não corrigiu, apenas marca a selecionada de azul
                        if (selectedAnswerIndex === index) btnClass += ' selected';
                    }

                    return (
                        <button 
                            key={index} 
                            className={btnClass}
                            onClick={() => !correction && setSelectedAnswerIndex(index)}
                            disabled={!!correction}
                        >
                            {alt}
                        </button>
                    );
                })}
            </div>

            {!correction && (
                <button
                onClick={corrigirExercicio}
                // MUDANÇA 3: Validação correta para não travar no índice 0
                disabled={loadingCorrection || selectedAnswerIndex === null}
                className="ex-btn purple"
                style={{ marginTop: '20px' }}
                >
                {loadingCorrection ? "Corrigindo..." : "Confirmar Resposta"}
                </button>
            )}
          </div>
        )}

        {correction && (
          <div className={`ex-section correction-box ${correction.acertou ? 'success' : 'error'}`}>
            <h3 className="ex-section-title">
                {correction.acertou ? <CheckCircle /> : <XCircle />}
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