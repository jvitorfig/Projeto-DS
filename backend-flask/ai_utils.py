import json
import re

def extract_json_from_response(response):
    """
    Tenta extrair um JSON válido da resposta do Gemini.
    - Se encontrar e conseguir decodificar, retorna o dict.
    - Se não conseguir, levanta ValueError com uma mensagem explicativa.
    """
    try:
        raw_text = response.text
    except Exception:
        raw_text = str(response)

    match = re.search(r"\{[\s\S]*\}", raw_text)
    if not match:
        raise ValueError(f"JSON não encontrado na resposta da IA. Trecho: {raw_text[:120]}...")

    json_str = match.group(0)

    # 3. Tenta decodificar
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Falha ao decodificar JSON da IA: {e}. Trecho: {json_str[:120]}..."
        )
