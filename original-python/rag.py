"""
Módulo de Recuperação de Documentos (RAG Simulado)
Carrega a base de conhecimento oficial (apostila.json) e realiza busca contextual.
"""
import json
import os

ARQUIVO_BASE = os.path.join(os.path.dirname(__file__), "apostila.json")

def carregar_base():
    """Carrega os documentos da apostila em formato JSON."""
    if not os.path.exists(ARQUIVO_BASE):
        return []
    with open(ARQUIVO_BASE, "r", encoding="utf-8") as f:
        return json.load(f)

def recuperar_contexto(pergunta):
    """
    Simula o mecanismo de busca do RAG:
    Varre a base documental comparando termos e palavras-chave da dúvida do aluno.
    Retorna o trecho mais relevante ou None se não houver correspondência.
    """
    documentos = carregar_base()
    pergunta_min = pergunta.lower()
    
    melhor_doc = None
    maior_pontuacao = 0
    
    for doc in documentos:
        pontuacao = 0
        # Verifica se o tópico principal aparece na pergunta
        if doc.get("topico", "").lower() in pergunta_min:
            pontuacao += 3
            
        # Verifica palavras-chave associadas
        for palavra in doc.get("palavras_chave", []):
            if palavra.lower() in pergunta_min:
                pontuacao += 1
                
        if pontuacao > maior_pontuacao:
            maior_pontuacao = pontuacao
            melhor_doc = doc
            
    if melhor_doc and maior_pontuacao > 0:
        return {
            "titulo": melhor_doc["titulo"],
            "conteudo": melhor_doc["conteudo"],
            "pontuacao": maior_pontuacao
        }
    return None
