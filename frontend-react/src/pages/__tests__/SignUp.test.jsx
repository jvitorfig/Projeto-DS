import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import SignUp from '../sing-up';

const mockNavigate = jest.fn();

jest.mock('react-router-dom', () => {
  const actual = jest.requireActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate
  };
});

describe('SignUp', () => {
  beforeEach(() => {
    mockNavigate.mockReset();
    global.fetch = jest.fn();
  });

  test('renderiza campos do formulário e botão', () => {
    render(
      <MemoryRouter>
        <SignUp />
      </MemoryRouter>
    );

    expect(screen.getByLabelText(/nome completo/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/e-mail/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^senha$/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/confirmar senha/i)).toBeInTheDocument();
    expect(
      screen.getByRole('button', { name: /cadastrar/i })
    ).toBeInTheDocument();
  });

  test('mostra erro quando senhas não coincidem', () => {
    render(
      <MemoryRouter>
        <SignUp />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/nome completo/i), {
      target: { value: 'Usuário Teste' }
    });
    fireEvent.change(screen.getByLabelText(/e-mail/i), {
      target: { value: 'teste@example.com' }
    });
    fireEvent.change(screen.getByLabelText(/^senha$/i), {
      target: { value: '123456' }
    });
    fireEvent.change(screen.getByLabelText(/confirmar senha/i), {
      target: { value: 'diferente' }
    });

    fireEvent.submit(
      screen.getByRole('button', { name: /cadastrar/i }).closest('form')
    );

    expect(
      screen.getByText(/as senhas não coincidem/i)
    ).toBeInTheDocument();
    expect(global.fetch).not.toHaveBeenCalled();
  });

  test('envia cadastro com sucesso e navega para login', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true })
    });

    render(
      <MemoryRouter>
        <SignUp />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/nome completo/i), {
      target: { value: 'Usuário Teste' }
    });
    fireEvent.change(screen.getByLabelText(/e-mail/i), {
      target: { value: 'teste@example.com' }
    });
    fireEvent.change(screen.getByLabelText(/^senha$/i), {
      target: { value: '123456' }
    });
    fireEvent.change(screen.getByLabelText(/confirmar senha/i), {
      target: { value: '123456' }
    });

    fireEvent.submit(
      screen.getByRole('button', { name: /cadastrar/i }).closest('form')
    );

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        'http://127.0.0.1:5000/api/register',
        expect.objectContaining({
          method: 'POST'
        })
      );
      expect(mockNavigate).toHaveBeenCalledWith('/login');
    });
  });
});
