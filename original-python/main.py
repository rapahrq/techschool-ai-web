#!/usr/bin/env python3
"""
====================================================================
PROJETO INTEGRADOR: TechSchool AI Assistant
Unidade Curricular: Inteligência Artificial (4º Bimestre)
Educação Profissional Paulista - Técnico em Desenvolvimento de Sistemas
====================================================================
"""
import sys
import os

from agentes import AgenteOrquestrador
from memoria import ler_historico, limpar_memoria
from rag import carregar_base

def cabecalho():
    print("=" * 65)
    print("       🏫 TECHSCHOOL AI - ASSISTENTE MULTIAGENTE       ")
    print("   Orquestração • RAG • Memória JSON • Ferramentas & APIs   ")
    print("=" * 65)

def exibir_menu_principal():
    print("\n[MODO DE OPERAÇÃO]")
    print("1. Iniciar Chat Interativo com o Orquestrador")
    print("2. Visualizar Documentos da Base de RAG (apostila.json)")
    print("3. Inspecionar Memória de Sessão Recente (memoria.json)")
    print("4. Limpar Memória da Sessão Atual")
    print("5. Sair do Sistema")
    print("-" * 65)

def chat_interativo(orquestrador):
    print("\n" + "=" * 65)
    print("💬 CHAT ATIVO: Digite sua pergunta ou comando.")
    print("Dicas de teste:")
    print("  - 'O que é uma variável?' (Testa o Agente Tutor + RAG)")
    print("  - 'Qual o endereço do CEP 01001-000?' (Testa Agente Ferramentas + API)")
    print("  - Digite 'voltar' para retornar ao menu principal.")
    print("=" * 65)

    while True:
        try:
            entrada = input("\n👤 Aluno: ").strip()
            if not entrada:
                continue
            if entrada.lower() in ["voltar", "sair", "exit"]:
                print("\nEncerrando sessão de chat e voltando ao menu...\n")
                break
                
            resposta = orquestrador.processar_solicitacao(entrada)
            print("\n" + resposta)
            print("-" * 65)
        except (KeyboardInterrupt, EOFError):
            print("\nRetornando ao menu...")
            break

def exibir_base_rag():
    docs = carregar_base()
    print("\n" + "=" * 65)
    print(f"📚 BASE DE CONHECIMENTO OFICIAL (RAG) - {len(docs)} Tópicos Cadastrados")
    print("=" * 65)
    for i, doc in enumerate(docs, 1):
        print(f"\n[{i}] {doc['titulo']} (Tópico: '{doc['topico']}')")
        print(f"    Palavras-chave: {', '.join(doc['palavras_chave'])}")
        print(f"    Conteúdo: {doc['conteudo']}")
    print("=" * 65)

def exibir_memoria_sessao():
    historico = ler_historico()
    print("\n" + "=" * 65)
    print(f"💾 MEMÓRIA DE CURTO PRAZO (Sessão Atual) - {len(historico)} Interações")
    print("=" * 65)
    if not historico:
        print("Nenhuma interação gravada nesta sessão ainda.")
    else:
        for idx, item in enumerate(historico, 1):
            print(f"\n#{idx} [{item['timestamp']}] | Agente: {item['agente']} | Remetente: {item['remetente']}")
            # Exibe os primeiros 100 caracteres se for muito longo
            texto_curto = item['texto'].replace('\n', ' ')
            if len(texto_curto) > 120:
                texto_curto = texto_curto[:117] + "..."
            print(f"   Mensagem: {texto_curto}")
    print("=" * 65)

def main():
    cabecalho()
    orquestrador = AgenteOrquestrador()

    while True:
        exibir_menu_principal()
        try:
            opcao = input("Escolha uma opção (1-5): ").strip()
            if opcao == "1":
                chat_interativo(orquestrador)
            elif opcao == "2":
                exibir_base_rag()
            elif opcao == "3":
                exibir_memoria_sessao()
            elif opcao == "4":
                limpar_memoria()
                print("\n✅ Memória de sessão limpa com sucesso!")
            elif opcao == "5":
                print("\n🤖 [TechSchool AI]: Até logo! Bons estudos em Desenvolvimento de Sistemas!")
                break
            else:
                print("\n⚠️ Opção inválida. Por favor, digite um número entre 1 e 5.")
        except (KeyboardInterrupt, EOFError):
            print("\nSaindo do sistema...")
            break

if __name__ == "__main__":
    main()
