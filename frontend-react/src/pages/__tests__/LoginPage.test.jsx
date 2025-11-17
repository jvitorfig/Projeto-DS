import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import LoginPage from '../LoginPage';

const mockNavigate = jest.fn();

jest.mock('react-router-dom', () => {
  const actual = jest.requireActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate
  };
});

describe('LoginPage', () => {
  beforeEach(() => {
    mockNavigate.mockReset();
    global.fetch = jest.fn();
    localStorage.clear();
  });

  test('renderiza campos de email, senha e botão', () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );
    expect(screen.getByLabelText(/e-mail/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/senha/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /entrar/i })).toBeInTheDocument();
  });

  test('faz login com sucesso e navega para /chat', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true })
    });

    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/e-mail/i), {
      target: { value: 'teste@example.com' }
    });
    fireEvent.change(screen.getByLabelText(/senha/i), {
      target: { value: '123456' }
    });

    fireEvent.submit(
      screen.getByRole('button', { name: /entrar/i }).closest('form')
    );

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        'http://127.0.0.1:5000/api/login',
        expect.objectContaining({
          method: 'POST'
        })
      );
      expect(localStorage.getItem('isLoggedIn')).toBe('true');
      expect(mockNavigate).toHaveBeenCalledWith('/chat');
    });
  });

  test('mostra mensagem de erro quando login falha', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: false, error: 'Credenciais inválidas' })
    });

    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/e-mail/i), {
      target: { value: 'teste@example.com' }
    });
    fireEvent.change(screen.getByLabelText(/senha/i), {
      target: { value: '123456' }
    });

    fireEvent.submit(
      screen.getByRole('button', { name: /entrar/i }).closest('form')
    );

    expect(
      await screen.findByText(/credenciais inválidas/i)
    ).toBeInTheDocument();
  });
});
