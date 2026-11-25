"""
Módulo de Agentes Especialistas e Agente Orquestrador
Implementa a arquitetura multiagente com protocolo de handoff e isolamento de escopo.
"""
from rag import recuperar_contexto
from ferramentas import consultar_cep
from memoria import registrar_interacao, ler_historico

class AgenteTutor:
    """
    Agente Especialista de Conteúdo.
    Responsável por sanar dúvidas teóricas e conceituais de programação
    baseando-se estritamente na base documental oficial (RAG).
    """
    def responder(self, pergunta):
        resultado_rag = recuperar_contexto(pergunta)
        
        if not resultado_rag:
            return (
                "📘 [Tutor TechSchool]: Puxa, dei uma olhada na nossa apostila oficial e "
                "não encontrei esse conteúdo cadastrado. Para não alucinar e te passar algo errado, "
                "prefiro te pedir para conferir se a dúvida é sobre Variáveis, Funções, APIs, "
                "Sistemas Multiagente, RAG ou Git! Quer tentar de novo com um desses temas?"
            )
            
        titulo = resultado_rag["titulo"]
        conteudo = resultado_rag["conteudo"]
        
        # Simula a resposta refinada (parâmetros Temperatura 0.2 / Top-P 0.2)
        resposta_formatada = (
            f"📘 [Tutor TechSchool - {titulo}]:\n"
            f"{conteudo}\n\n"
            f"💡 Dica de amigo: Pense nesse conceito como uma peça de montar; cada parte tem seu lugar certo no código.\n"
            f"Ficou claro para você ou quer que eu detalhe mais alguma parte?"
        )
        return resposta_formatada


class AgenteFerramentas:
    """
    Agente Especialista em Ferramentas e Integração Externa (APIs).
    Executa ações concretas no mundo real através de Function Calling.
    """
    def processar(self, mensagem):
        import re
        numeros = re.findall(r"\d+", mensagem)
        if not numeros:
            return (
                "🌐 [Agente de Ferramentas / API]: Você pediu uma consulta de localização, "
                "mas não identifiquei o número do CEP na sua mensagem. Por favor, digite no formato: "
                "'consultar cep 01001-000' ou apenas os 8 números."
            )
            
        cep_candidato = "".join(numeros)
        resultado = consultar_cep(cep_candidato)
        
        if not resultado["sucesso"]:
            return f"🌐 [Agente de Ferramentas / API]: ⚠️ {resultado['erro']}"
            
        return (
            f"🌐 [Agente de Ferramentas / API - Consulta Concluída]:\n"
            f"📍 Logradouro: {resultado['logradouro']}\n"
            f"🏙️ Bairro: {resultado['bairro']}\n"
            f"🗺️ Cidade/UF: {resultado['cidade']}\n"
            f"ℹ️ Fonte de Dados: {resultado['fonte']}"
        )


class AgenteOrquestrador:
    """
    Agente Central (Maestro).
    Faz a triagem da mensagem do usuário, gerencia o fluxo de memória da sessão,
    decide a intenção e executa o HANDOFF para o especialista correto.
    """
    def __init__(self):
        self.tutor = AgenteTutor()
        self.ferramentas = AgenteFerramentas()

    def processar_solicitacao(self, mensagem_usuario):
        msg_limpa = mensagem_usuario.strip()
        if not msg_limpa:
            return "🤖 [Orquestrador]: Oi! Não entendi sua mensagem. Como posso te ajudar hoje?"

        # 1. Registra a mensagem do aluno na memória de curto prazo
        registrar_interacao(remetente="Aluno", texto=msg_limpa, agente_ativo="Interface")

        msg_lower = msg_limpa.lower()

        # 2. Análise Semântica de Intenção e Roteamento (Handoff)
        if any(termo in msg_lower for termo in ["cep", "endereco", "endereço", "polo", "localizacao", "localização"]):
            # Handoff para o Agente de Ferramentas
            print("\n  🔀 [Orquestrador]: Intenção identificada -> 'Consulta Externa/API'")
            print("  🔀 [Orquestrador]: Executando HANDOFF formal para AgenteFerramentas...")
            resposta_final = self.ferramentas.processar(msg_limpa)
            agente_responsavel = "AgenteFerramentas"

        elif any(termo in msg_lower for termo in ["ola", "olá", "oi", "bom dia", "boa tarde", "boa noite", "ajuda", "menu"]):
            resposta_final = (
                "🤖 [Orquestrador TechSchool]: Olá! Eu sou o Orquestrador do sistema.\n"
                "Aqui você pode:\n"
                "1. Tirar dúvidas de aulas (Ex: 'O que é variável?', 'Como funciona o RAG?', 'Para que serve Git?')\n"
                "2. Consultar endereços dos polos por CEP (Ex: 'Qual o endereço do CEP 01001-000?')\n"
                "3. Inspecionar o histórico da memória da nossa sessão.\n"
                "Sobre o que você gostaria de conversar agora?"
            )
            agente_responsavel = "Orquestrador"

        else:
            # Handoff para o Agente Tutor de Conteúdo (RAG)
            print("\n  🔀 [Orquestrador]: Intenção identificada -> 'Dúvida Acadêmica/Conteúdo'")
            print("  🔀 [Orquestrador]: Executando HANDOFF formal para AgenteTutor (RAG)...")
            resposta_final = self.tutor.responder(msg_limpa)
            agente_responsavel = "AgenteTutor"

        # 3. Registra a resposta final consolidada na memória
        registrar_interacao(remetente="Assistente", texto=resposta_final, agente_ativo=agente_responsavel)

        return resposta_final
