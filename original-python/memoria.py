"""
Módulo de Gestão de Memória da Conversa (Curto Prazo)
Grava e recupera as mensagens da sessão em memória.json.
"""
import json
import os
from datetime import datetime

ARQUIVO_MEMORIA = os.path.join(os.path.dirname(__file__), "memoria.json")

def inicializar_memoria():
    """Garante que o arquivo de memória exista com uma lista vazia."""
    if not os.path.exists(ARQUIVO_MEMORIA):
        salvar_historico([])

def ler_historico():
    """Lê todas as interações da sessão atual."""
    inicializar_memoria()
    try:
        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def salvar_historico(historico):
    """Salva a lista completa no arquivo JSON."""
    with open(ARQUIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)

def registrar_interacao(remetente, texto, agente_ativo="Orquestrador"):
    """
    Adiciona um novo registro ao histórico de curto prazo com timestamp.
    """
    historico = ler_historico()
    novo_registro = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "remetente": remetente,
        "agente": agente_ativo,
        "texto": texto
    }
    historico.append(novo_registro)
    salvar_historico(historico)

def limpar_memoria():
    """Reinicia o histórico da sessão."""
    salvar_historico([])
