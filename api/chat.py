import json
import re
from http.server import BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.error import URLError

KNOWLEDGE = [
 {"topico":"variavel","titulo":"Conceito de Variável","conteudo":"Uma variável é um espaço alocado na memória RAM do computador com um nome específico (rótulo) usado para armazenar dados que podem ser lidos ou alterados durante a execução do programa. Metáfora didática: imagine uma gaveta etiquetada onde você guarda objetos temporariamente.","palavras_chave":["variavel","variável","let","const","dados","memoria"]},
 {"topico":"funcao","titulo":"Conceito de Função","conteudo":"Uma função é um bloco autônomo e reutilizável de instruções de código que recebe entradas (parâmetros), executa uma lógica específica e pode retornar um resultado. Evita repetição de código e facilita a manutenção.","palavras_chave":["funcao","função","bloco","parametro","retorno"]},
 {"topico":"api","titulo":"Conceito de API e Function Calling","conteudo":"API (Interface de Programação de Aplicações) é um conjunto de regras e protocolos que permite que sistemas diferentes se comuniquem e troquem dados de forma segura (normalmente via formato JSON). Em IA, Function Calling permite que o agente monte uma chamada estruturada para que a API execute uma ação externa no mundo real.","palavras_chave":["api","endpoint","json","integracao","integrar","requisicao"]},
 {"topico":"multiagente","titulo":"Sistemas Multiagente e Orquestração","conteudo":"Em vez de um único robô sobrecarregado (agente monolítico), sistemas multiagente dividem as responsabilidades entre especialistas coordenados por um Agente Orquestrador. A transferência formal de tarefas e contexto entre especialistas é chamada de Handoff.","palavras_chave":["multiagente","monolitico","orquestrador","handoff","agentes"]},
 {"topico":"rag","titulo":"RAG (Recuperação Aumentada por Geração)","conteudo":"RAG é a técnica em que o sistema busca trechos confiáveis em uma base de documentos oficial antes de responder. Esses trechos são injetados no prompt da IA, garantindo que ela responda com base em fatos reais e eliminando alucinações.","palavras_chave":["rag","recuperacao","documento","alucinacao","base","contexto"]},
 {"topico":"git","titulo":"Versionamento Colaborativo com Git","conteudo":"O Git gerencia o histórico de alterações do código. Branches permitem desenvolver melhorias e testar novos agentes em paralelo sem colocar em risco a versão principal (main). Commits registram o progresso e Merges integram as soluções validadas.","palavras_chave":["git","branch","commit","merge","versao"]}
]
POLOS={"01001000":{"nome":"Polo Centro - Praça da Sé","logradouro":"Praça da Sé, 100","bairro":"Centro","cidade":"São Paulo/SP"},"04101000":{"nome":"Polo Vila Mariana","logradouro":"Rua Domingos de Morais, 500","bairro":"Vila Mariana","cidade":"São Paulo/SP"},"13010000":{"nome":"Polo Interior - Campinas","logradouro":"Av. Francisco Glicério, 800","bairro":"Centro","cidade":"Campinas/SP"}}

def tutor(question):
    q=question.lower()
    best=None; score=0
    for doc in KNOWLEDGE:
        points=3 if doc["topico"] in q else 0
        points += sum(1 for word in doc["palavras_chave"] if word in q)
        if points>score: best=doc; score=points
    if not best:
        return ("📘 [Tutor TechSchool]: Puxa, dei uma olhada na nossa apostila oficial e não encontrei esse conteúdo cadastrado. Para não inventar informações, confira se sua dúvida é sobre Variáveis, Funções, APIs, Sistemas Multiagente, RAG ou Git. Quer tentar novamente com um desses temas?","AgenteTutor")
    return (f"📘 [Tutor TechSchool - {best['titulo']}]:\n{best['conteudo']}\n\n💡 Dica de amigo: Pense nesse conceito como uma peça de montar; cada parte tem seu lugar certo no código.\nFicou claro para você ou quer que eu detalhe mais alguma parte?","AgenteTutor")

def cep_lookup(message):
    digits="".join(re.findall(r"\d",message))
    if len(digits)!=8:
        return ("🌐 [Agente de Ferramentas / API]: Não identifiquei um CEP válido. Digite os 8 números, por exemplo: 01001-000.","AgenteFerramentas")
    if digits in POLOS:
        d=POLOS[digits]
        return (f"🌐 [Consulta de polo TechSchool]:\n📍 Polo: {d['nome']}\nLogradouro: {d['logradouro']}\nBairro: {d['bairro']}\nCidade/UF: {d['cidade']}\nFonte: Base Local de Polos TechSchool","AgenteFerramentas")
    try:
        req=Request(f"https://viacep.com.br/ws/{digits}/json/",headers={"User-Agent":"TechSchoolAI/1.0"})
        with urlopen(req,timeout=5) as response: data=json.loads(response.read().decode("utf-8"))
        if data.get("erro"): return ("🌐 [Agente de Ferramentas / API]: CEP não localizado na base nacional dos Correios.","AgenteFerramentas")
        return (f"🌐 [Consulta ViaCEP concluída]:\nLogradouro: {data.get('logradouro') or 'Não informado'}\nBairro: {data.get('bairro') or 'Não informado'}\nCidade/UF: {data.get('localidade','')}/{data.get('uf','')}\nFonte: API ViaCEP","AgenteFerramentas")
    except (URLError,TimeoutError,ValueError):
        return ("🌐 [Agente de Ferramentas / API]: Não foi possível consultar o ViaCEP agora. Tente novamente mais tarde.","AgenteFerramentas")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length=int(self.headers.get("Content-Length","0"))
            payload=json.loads(self.rfile.read(length) or b"{}")
            message=str(payload.get("message","")).strip()
            if not message: self.respond(400,{"error":"Digite uma pergunta."}); return
            low=message.lower()
            if any(term in low for term in ["cep","endereco","endereço","polo","localizacao","localização"]):
                reply,agent=cep_lookup(message)
            elif any(term in low for term in ["ola","olá","oi","bom dia","boa tarde","boa noite","ajuda","menu"]):
                reply=("🤖 [Orquestrador TechSchool]: Olá! Sou o Orquestrador do sistema.\nVocê pode tirar dúvidas sobre os conteúdos da apostila ou consultar endereços de polos pelo CEP.\nExemplos: 'O que é variável?' ou 'Qual o endereço do CEP 01001-000?'.","Orquestrador")
                agent="Orquestrador"
            else: reply,agent=tutor(message)
            self.respond(200,{"reply":reply,"agent":agent})
        except Exception as exc:
            self.respond(500,{"error":"Erro interno ao processar a solicitação."})
    def do_OPTIONS(self): self.respond(200,{})
    def respond(self,status,data):
        body=json.dumps(data,ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Cache-Control","no-store")
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.send_header("Access-Control-Allow-Methods","POST, OPTIONS")
        self.end_headers(); self.wfile.write(body)
