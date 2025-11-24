# Mentor IA de Carreira

> **Uma aplicação que analisa perfis do GitHub e gera recomendações personalizadas de carreira usando IA.**

Este projeto demonstra integração real com APIs, análise de dados, métricas técnicas, engenharia de prompts e construção de interface interativa com Streamlit.

## Visão Geral

O **Mentor IA de Carreira** transforma dados públicos do GitHub em insights estruturados sobre o nível técnico de um desenvolvedor. A aplicação coleta informações de repositórios, linguagem, atividade e padrões de contribuição, processa esses dados por um analisador próprio e utiliza um modelo generativo para produzir:

* Diagnóstico do nível técnico;
* Pontos fortes e lacunas;
* Sugestões práticas de melhoria;
* Roadmap personalizado (30/60/90 dias).

Este projeto foi planejado para demonstrar habilidades em **Python**, análise de dados, IA generativa e desenvolvimento de aplicações interativas.

## Principais Funcionalidades

* ** Coleta de Dados:** Extração automática de repositórios, linguagens e frequência de commits via GitHub API.
* ** Análise Técnica (Heurística):** Algoritmo próprio (`analyzer.py`) que calcula:
    * Diversidade e profundidade de linguagens.
    * Consistência de atividade (commits semanais).
    * Qualidade dos projetos (README, testes, tamanho).
* ** Inteligência Artificial:** Integração com o modelo `gemini-2.5-flash` para gerar:
    * Análise de pontos fortes e fracos.
    * Sugestões de carreira compatíveis com o perfil.
    * **Roadmap completo de 90 dias** (30/60/90) focado no objetivo do usuário.
* ** Interface Gráfica:** Dashboard interativo e moderno construído com **Streamlit**.

---

## Tecnologias e Ferramentas

* Python 3.10+
* Streamlit
* Requests (GitHub API)
* Pandas
* Google Generative AI (Gemini)
* python-dotenv
