import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ChatPage from '../ChatPage';

describe('ChatPage', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  test('carrega mensagem inicial do bot', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ message: 'Olá, sou o bot.' })
    });

    render(<ChatPage />);

    expect(
      await screen.findByText(/olá, sou o bot\./i)
    ).toBeInTheDocument();
  });

  test('envia mensagem do usuário e mostra resposta do bot', async () => {
    global.fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Mensagem inicial' })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: 'Resposta do bot' })
      });

    render(<ChatPage />);

    await screen.findByText(/mensagem inicial/i);

    fireEvent.change(
      screen.getByPlaceholderText(/digite sua mensagem aqui/i),
      {
        target: { value: 'Oi' }
      }
    );

    fireEvent.click(
      screen.getByRole('button', { name: /enviar mensagem/i })
    );

    expect(await screen.findByText('Oi')).toBeInTheDocument();
    expect(
      await screen.findByText(/resposta do bot/i)
    ).toBeInTheDocument();
  });
});
