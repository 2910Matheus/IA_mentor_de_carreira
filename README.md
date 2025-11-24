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

* **Coleta automática de dados** via GitHub REST API.
* **Cálculo de métricas técnicas** (diversidade de linguagens, consistência de commits, qualidade dos projetos).
* **Geração de relatórios estruturados** e roadmap de evolução.
* **Interface completa em Streamlit** para visualização dos resultados.
* **Arquitetura modular** com classes dedicadas para coleta, análise e geração de insights.

## Tecnologias e Ferramentas

* Python 3.10+
* Streamlit
* Requests (GitHub API)
* Pandas
* Google Generative AI (Gemini)
* python-dotenv
