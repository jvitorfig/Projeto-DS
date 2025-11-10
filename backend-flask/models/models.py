from typing import Any, Optional
import datetime

from sqlalchemy import DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import BIT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Questao(Base):
    __tablename__ = 'questao'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='questao_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    texto: Mapped[str] = mapped_column(String(500), nullable=False)

    questao_x_topico: Mapped[list['QuestaoXTopico']] = relationship('QuestaoXTopico', back_populates='questao')
    questionario_x_questao: Mapped[list['QuestionarioXQuestao']] = relationship('QuestionarioXQuestao', back_populates='questao')


class QuestaoResposta(Base):
    __tablename__ = 'questao_resposta'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='questao_resposta_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_questao: Mapped[int] = mapped_column(Integer, nullable=False)
    texto: Mapped[str] = mapped_column(String(500), nullable=False)
    resposta_correta: Mapped[Optional[Any]] = mapped_column(BIT(1))


class Questionario(Base):
    __tablename__ = 'questionario'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='questionario_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(String(500))

    questionario_x_questao: Mapped[list['QuestionarioXQuestao']] = relationship('QuestionarioXQuestao', back_populates='questionario')
    questionario_x_usuario: Mapped[list['QuestionarioXUsuario']] = relationship('QuestionarioXUsuario', back_populates='questionario')


class Topico(Base):
    __tablename__ = 'topico'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='topico_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    texto: Mapped[str] = mapped_column(String(255), nullable=False)

    questao_x_topico: Mapped[list['QuestaoXTopico']] = relationship('QuestaoXTopico', back_populates='topico')


class Usuario(Base):
    __tablename__ = 'usuario'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='usuario_pkey'),
        UniqueConstraint('email', name='usuario_email_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(500), nullable=False)

    questionario_x_usuario: Mapped[list['QuestionarioXUsuario']] = relationship('QuestionarioXUsuario', back_populates='usuario')


class QuestaoXTopico(Base):
    __tablename__ = 'questao_x_topico'
    __table_args__ = (
        ForeignKeyConstraint(['id_questao'], ['questao.id'], name='fk_qxt_questao'),
        ForeignKeyConstraint(['id_topico'], ['topico.id'], name='fk_qxt_topico'),
        PrimaryKeyConstraint('id', name='questao_x_topico_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_questao: Mapped[int] = mapped_column(Integer, nullable=False)
    id_topico: Mapped[int] = mapped_column(Integer, nullable=False)

    questao: Mapped['Questao'] = relationship('Questao', back_populates='questao_x_topico')
    topico: Mapped['Topico'] = relationship('Topico', back_populates='questao_x_topico')


class QuestionarioXQuestao(Base):
    __tablename__ = 'questionario_x_questao'
    __table_args__ = (
        ForeignKeyConstraint(['id_questao'], ['questao.id'], name='fk_qxq_questao'),
        ForeignKeyConstraint(['id_questionario'], ['questionario.id'], name='fk_qxq_questionario'),
        PrimaryKeyConstraint('id', name='questionario_x_questao_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_questionario: Mapped[int] = mapped_column(Integer, nullable=False)
    id_questao: Mapped[int] = mapped_column(Integer, nullable=False)

    questao: Mapped['Questao'] = relationship('Questao', back_populates='questionario_x_questao')
    questionario: Mapped['Questionario'] = relationship('Questionario', back_populates='questionario_x_questao')


class QuestionarioXUsuario(Base):
    __tablename__ = 'questionario_x_usuario'
    __table_args__ = (
        ForeignKeyConstraint(['id_questionario'], ['questionario.id'], name='fk_qxu_questionario'),
        ForeignKeyConstraint(['id_usuario'], ['usuario.id'], name='fk_qxu_usuario'),
        PrimaryKeyConstraint('id', name='questionario_x_usuario_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(Integer, nullable=False)
    id_questionario: Mapped[int] = mapped_column(Integer, nullable=False)
    pontuacao: Mapped[Optional[int]] = mapped_column(Integer)
    data_aplicacao: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))

    questionario: Mapped['Questionario'] = relationship('Questionario', back_populates='questionario_x_usuario')
    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='questionario_x_usuario')
