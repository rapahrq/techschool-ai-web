# TechSchool AI Web

Versão web do projeto TechSchool AI Assistant, preparada para publicação na Vercel.

## O que foi mantido
- Orquestrador com roteamento por intenção.
- Agente Tutor com busca simples na base documental (RAG simulado).
- Agente Ferramentas para consulta de CEP via ViaCEP.
- Polos locais cadastrados no projeto.
- Visualização dos seis tópicos da apostila.

## Estrutura
- `index.html`, `style.css`, `app.js`: interface web.
- `api/chat.py`: endpoint Python chamado pelo front-end.
- `vercel.json`: configuração de publicação.
- `requirements.txt`: dependências Python (nenhuma externa).

## Publicação na Vercel

1. Descompacte o projeto.
2. Crie uma conta em https://github.com, se ainda não tiver.
3. No GitHub, crie um repositório chamado `techschool-ai-web`.
4. Envie todos os arquivos e pastas deste projeto para a raiz do repositório. A pasta `api` precisa ficar na raiz.
5. Acesse https://vercel.com e entre com sua conta GitHub.
6. Clique em **Add New → Project**.
7. Escolha o repositório `techschool-ai-web` e clique em **Import**.
8. Em **Framework Preset**, selecione **Other**. Não informe diretório raiz diferente de `./`.
9. Não é necessário configurar Build Command nem Output Directory para esta estrutura estática.
10. Clique em **Deploy**.
11. Ao terminar, abra o domínio `.vercel.app` gerado e teste o chat.

## Testes depois da publicação
- `O que é uma variável?` deve retornar o conteúdo do tópico Variável.
- `Como funciona o RAG?` deve retornar o tópico RAG.
- `Qual o endereço do CEP 01001-000?` deve consultar o polo cadastrado.
- `Qual o endereço do CEP 01001-001?` deve tentar consultar o ViaCEP.

## Sobre a memória
Nesta primeira versão web, o histórico fica no `localStorage` do navegador, por dispositivo e navegador. Ele não é compartilhado entre alunos e não é um banco de dados central. Para histórico multiusuário persistente, conecte um banco de dados gerenciado, como Neon Postgres, e implemente autenticação e isolamento por usuário.

## Observação técnica
O projeto original é uma simulação didática de agentes e RAG com busca por palavras-chave. A versão web preserva essa lógica; ela não chama um modelo de linguagem generativo. A publicação na Vercel hospeda o front-end e a função Python, mas não transforma a simulação em uma IA generativa.
