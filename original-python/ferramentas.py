"""
Módulo de Ferramentas Externas (Function Calling & APIs)
Simula a integração com APIs externas (como ViaCEP) e serviços da TechSchool.
"""
import re
import urllib.request
import json

# Polos cadastrados da TechSchool para busca rápida
POLOS_TECHSCHOOL = {
    "01001000": {"nome": "Polo Centro - Praça da Sé", "cidade": "São Paulo/SP", "logradouro": "Praça da Sé, 100"},
    "04101000": {"nome": "Polo Vila Mariana", "cidade": "São Paulo/SP", "logradouro": "Rua Domingos de Morais, 500"},
    "13010000": {"nome": "Polo Interior - Campinas", "cidade": "Campinas/SP", "logradouro": "Av. Francisco Glicério, 800"}
}

def consultar_cep(cep_bruto):
    """
    Limpa o CEP e consulta a API pública do ViaCEP.
    Possui fallback offline caso a máquina esteja sem conexão externa.
    """
    cep_limpo = re.sub(r"\D", "", str(cep_bruto))
    
    if len(cep_limpo) != 8:
        return {
            "sucesso": False,
            "erro": "CEP inválido. Um CEP brasileiro deve conter exatamente 8 dígitos numéricos."
        }
        
    # Verifica primeiro se é um polo cadastrado internamente
    if cep_limpo in POLOS_TECHSCHOOL:
        polo = POLOS_TECHSCHOOL[cep_limpo]
        return {
            "sucesso": True,
            "fonte": "Base Local de Polos TechSchool",
            "logradouro": polo["logradouro"],
            "bairro": "Centro",
            "cidade": polo["cidade"],
            "polo_parceiro": polo["nome"]
        }
        
    # Tenta consultar o ViaCEP online
    try:
        url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
        req = urllib.request.Request(url, headers={'User-Agent': 'TechSchoolBot/1.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                dados = json.loads(response.read().decode('utf-8'))
                if "erro" in dados:
                    return {"sucesso": False, "erro": "CEP não localizado na base nacional dos Correios."}
                return {
                    "sucesso": True,
                    "fonte": "API ViaCEP (Online)",
                    "logradouro": dados.get("logradouro", "Não informado"),
                    "bairro": dados.get("bairro", "Não informado"),
                    "cidade": f"{dados.get('localidade', '')}/{dados.get('uf', '')}"
                }
    except Exception:
        # Fallback offline para demonstração didática em aula
        return {
            "sucesso": True,
            "fonte": "Simulação Didática (Modo Offline)",
            "logradouro": "Avenida Paulista, 1500",
            "bairro": "Bela Vista",
            "cidade": "São Paulo/SP",
            "aviso": "Resposta gerada em modo offline didático."
        }
