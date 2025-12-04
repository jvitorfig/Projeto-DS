import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, Trophy, Target, PieChart } from "lucide-react";
import '../styles/exercicios.css';

export default function Estatisticas() {
  const [stats, setStats] = useState([]);
  const [globalData, setGlobalData] = useState({ average: 0, total: 0 });
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  
  const userId = localStorage.getItem('userId'); 

  useEffect(() => {
    if (!userId) {
        alert("Você precisa fazer login para ver suas estatísticas.");
        navigate("/login");
        return;
    }
    fetchStats();
  }, [userId]); // Adicione userId na dependência
  // ----------------------

  const fetchStats = async () => {
    try {
      // O userId já está sendo usado corretamente na URL aqui:
      const response = await fetch(`http://127.0.0.1:5000/api/user-stats/${userId}`);
      // ... resto da função igual ...
      const data = await response.json();
      
      if (data.stats) {
        setStats(data.stats);
        setGlobalData({ 
            average: data.global_average, 
            total: data.total_questions 
        });
      }
    } catch (error) {
      console.error("Erro ao buscar estatísticas:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ex-page">
      <div className="ex-container">
        <button className="ex-back-btn" onClick={() => navigate("/exercicios")}>
          <ArrowLeft size={20} /> Voltar aos Exercícios
        </button>

        <h1 className="ex-title">Seu Desempenho</h1>
        <p className="ex-subtitle">Acompanhe sua evolução em cada matéria.</p>

        {/* Resumo Global */}
        <div className="stats-grid">
            <div className="stat-card">
                <Trophy size={32} color="#f59e0b" />
                <div>
                    <h3>Média Geral</h3>
                    <p className="stat-value">{globalData.average}%</p>
                </div>
            </div>
            <div className="stat-card">
                <Target size={32} color="#646cff" />
                <div>
                    <h3>Questões Totais</h3>
                    <p className="stat-value">{globalData.total}</p>
                </div>
            </div>
        </div>

        <h2 className="ex-section-title" style={{ marginTop: '30px' }}>Por Tópico</h2>

        {loading ? (
            <p>Carregando dados...</p>
        ) : stats.length === 0 ? (
            <div className="ex-box" style={{textAlign: 'center', padding: '40px'}}>
                <PieChart size={48} color="#ccc" style={{marginBottom: '10px'}}/>
                <p>Você ainda não realizou exercícios suficientes.</p>
                <button className="ex-btn" onClick={() => navigate("/exercicios")} style={{marginTop: '10px'}}>
                    Começar a Praticar
                </button>
            </div>
        ) : (
            <div className="topic-list">
                {stats.map((item, index) => (
                    <div key={index} className="topic-item">
                        <div className="topic-header">
                            <span className="topic-name">{item.topic}</span>
                            <span className="topic-percent" style={{
                                color: item.percent >= 70 ? '#059669' : item.percent >= 40 ? '#d97706' : '#dc2626'
                            }}>
                                {item.percent}%
                            </span>
                        </div>
                        
                        <div className="progress-bar-bg">
                            <div 
                                className="progress-bar-fill" 
                                style={{ 
                                    width: `${item.percent}%`,
                                    backgroundColor: item.percent >= 70 ? '#34d399' : item.percent >= 40 ? '#facc15' : '#f87171'
                                }}
                            ></div>
                        </div>
                        <div className="topic-details">
                            {item.acertos} acertos de {item.total} questões
                        </div>
                    </div>
                ))}
            </div>
        )}
      </div>
    </div>
  );
}