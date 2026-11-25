# 🏫 TechSchool AI Assistant
**Projeto Prático Integrador — Inteligência Artificial (4º Bimestre)**  
*Educação Profissional Paulista — Ensino Técnico em Desenvolvimento de Sistemas*

---

## 🎯 Sobre o Projeto
O **TechSchool AI** é um sistema demonstrativo completo que implementa os conceitos trabalhados nas Semanas 21 a 26:
* **Arquitetura Multiagente:** Separação entre o Agente Orquestrador (maestro/triagem) e Agentes Especialistas (Tutor e Ferramentas).
* **Protocolo de Handoff:** Passagem formal de bastão entre agentes com registro de logs.
* **RAG (Recuperação Aumentada por Geração):** Base de conhecimento oficial em `apostila.json` para eliminar alucinações.
* **Memória de Curto Prazo:** Persistência em tempo de execução via `memoria.json`.
* **Integração com Ferramentas/APIs:** Consulta de endereços e polos com fallback offline inteligente.

---

## 📂 Estrutura de Arquivos

```text
techschool-ai/
│
├── main.py              # Ponto de entrada do sistema (terminal interativo com menu)
├── agentes.py           # Classes do Orquestrador, AgenteTutor e AgenteFerramentas
├── rag.py               # Mecanismo de busca e injeção de contexto documental
├── memoria.py           # Gerenciador de leitura e escrita do histórico recente
├── ferramentas.py       # Integração com APIs externas (ViaCEP e polos)
├── apostila.json        # Base documental oficial de tópicos do 4º bimestre
├── memoria.json         # Arquivo gerado automaticamente com os logs da conversa
├── requirements.txt     # Dependências (apenas Python padrão é obrigatório!)
└── README.md            # Este manual de instruções
```

---

## 🚀 Como Executar o Projeto Passo a Passo

### Pré-requisitos
* Python 3.8 ou superior instalado no computador.
* Terminal de comando (Prompt de Comando, PowerShell, Terminal do Linux ou VS Code).

### Passo 1: Descompactar e Acessar a Pasta
Extraia o arquivo `techschool-ai-projeto.zip` e abra o terminal dentro da pasta:
```bash
cd techschool-ai
```

### Passo 2: (Opcional) Criar um Ambiente Virtual
Para manter seu ambiente isolado, como ensinado na Semana 23:
```bash
# No Windows:
python -m venv venv
venv\Scripts\activate

# No Linux/Mac:
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Executar a Aplicação
Execute o arquivo principal:
```bash
python main.py
```
*(No Linux ou Mac, use `python3 main.py`)*

---

## 🧪 Roteiro de Testes em Sala de Aula

1. **Testando o RAG (Agente Tutor):**
   * Digite a opção `1` para entrar no chat.
   * Envie: `O que é uma variável?` ou `Como funciona o RAG?`
   * *O que observar:* O Orquestrador faz o handoff para o AgenteTutor, que busca o conteúdo em `apostila.json` e responde com um tom didático para jovens de 15 anos.
2. **Testando a Mitigação de Alucinação:**
   * Envie: `Como instalar o Photoshop no roteador?`
   * *O que observar:* O agente avisa honestamente que o conteúdo não consta na apostila oficial e não tenta inventar fatos.
3. **Testando Ferramentas e APIs:**
   * Envie: `Qual o endereço do polo do CEP 01001-000?`
   * *O que observar:* O Orquestrador identifica a intenção de localização e aciona o AgenteFerramentas.
4. **Inspecionando a Memória:**
   * Digite `voltar` no chat e escolha a opção `3` no menu.
   * *O que observar:* Veja o histórico completo gravado em `memoria.json` com timestamps e os agentes responsáveis por cada turno.
