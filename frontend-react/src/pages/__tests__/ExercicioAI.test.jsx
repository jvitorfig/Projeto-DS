import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import ExercicioAI from '../Exercicios';

const mockNavigate = jest.fn();

jest.mock('react-router-dom', () => {
  const actual = jest.requireActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate
  };
});

jest.mock('lucide-react', () => ({
  ArrowLeft: () => <div data-testid="arrow-left-icon" />
}));

jest.mock('react-markdown', () => {
  return ({ children }) => <div>{children}</div>;
});

describe('ExercicioAI', () => {
  beforeEach(() => {
    mockNavigate.mockReset();
    global.fetch = jest.fn();
  });

  test('renderiza campos principais', () => {
    render(
      <MemoryRouter>
        <ExercicioAI />
      </MemoryRouter>
    );

    expect(
      screen.getByPlaceholderText(/ex: derivadas/i)
    ).toBeInTheDocument();

    expect(
      screen.getByRole('button', { name: /gerar exercício/i })
    ).toBeInTheDocument();

    expect(
      screen.getByRole('button', { name: /voltar ao chat/i })
    ).toBeInTheDocument();
  });

  test('não mostra seções de exercício e correção inicialmente', () => {
    render(
      <MemoryRouter>
        <ExercicioAI />
      </MemoryRouter>
    );

    expect(
      screen.queryByText(/exercício gerado/i)
    ).not.toBeInTheDocument();

    expect(
      screen.queryByRole('heading', { name: /correção/i })
    ).not.toBeInTheDocument();
  });

  test('gera exercício', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ exercise: 'Exercício de teste' })
    });

    render(
      <MemoryRouter>
        <ExercicioAI />
      </MemoryRouter>
    );

    fireEvent.change(
      screen.getByPlaceholderText(/ex: derivadas/i),
      { target: { value: 'Derivadas' } }
    );

    fireEvent.click(
      screen.getByRole('button', { name: /gerar exercício/i })
    );

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalled();
    });

    expect(
      await screen.findByText(/exercício gerado/i)
    ).toBeInTheDocument();

    expect(
      await screen.findByText(/exercício de teste/i)
    ).toBeInTheDocument();
  });

  test('envia resposta e recebe correção', async () => {
    global.fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ exercise: 'Exercício de teste' })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ correction: 'Correção da resposta' })
      });

    render(
      <MemoryRouter>
        <ExercicioAI />
      </MemoryRouter>
    );

    fireEvent.change(
      screen.getByPlaceholderText(/ex: derivadas/i),
      { target: { value: 'Derivadas' } }
    );

    fireEvent.click(
      screen.getByRole('button', { name: /gerar exercício/i })
    );

    await screen.findByText(/exercício de teste/i);

    fireEvent.change(
      screen.getByPlaceholderText(/digite sua resposta/i),
      { target: { value: 'Minha resposta' } }
    );

    fireEvent.click(
      screen.getByRole('button', { name: /enviar para correção/i })
    );

    expect(
      await screen.findByText(/correção da resposta/i)
    ).toBeInTheDocument();
  });

  test('voltar ao chat navega para /chat', () => {
    render(
      <MemoryRouter>
        <ExercicioAI />
      </MemoryRouter>
    );

    fireEvent.click(
      screen.getByRole('button', { name: /voltar ao chat/i })
    );

    expect(mockNavigate).toHaveBeenCalledWith('/chat');
  });
});
