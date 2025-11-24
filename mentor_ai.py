import google.generativeai as genai # type:ignore
import os
from dotenv import load_dotenv, find_dotenv # type:ignore
import json

# Tava com problema para localizar o .env, esses print da para tirar se quiser
env_file = find_dotenv()
if not env_file:
    print("⚠️ AVISO: Arquivo .env não encontrado!")
else:
    print(f"✅ Arquivo .env encontrado em: {env_file}")

load_dotenv(env_file)

# 2. Pega a chave e VERIFICA se ela veio
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ ERRO FATAL: A variável 'GEMINI_API_KEY' está vazia ou não existe no .env")

print("🔑 Chave carregada com sucesso. Configurando Gemini...")
genai.configure(api_key=api_key)

# =========================================================================
# CLASSE MENTORAI
# =========================================================================

class MentorAI:
    def __init__(self):
        self.generation_config_json = {
            "response_mime_type": "application/json",
        }
        # Modelo que estou usando: gemini-2.5-flash
        self.model = genai.GenerativeModel(
            "gemini-2.5-flash",
            generation_config=self.generation_config_json
        )
    def analyze_profile(self, profile_summary):
        # Estou forçando a IA a me retornar o arquivo em formato JSON para facilitar na formatação no streamlit
        json_schema_analysis = """
{
  "resumo_geral": "string - Descrição breve e objetiva do perfil analisado.",
  "forcas_tecnicas": ["string - Força 1 (Item da lista)", "string - Força 2 (Item da lista)", "..."],
  "pontos_melhorar": ["string - Ponto a melhorar 1 (Item da lista)", "string - Ponto a melhorar 2 (Item da lista)", "..."],
  "sugestoes_curto_prazo": ["string - Sugestão de 7-30 dias 1 (Item da lista)", "string - Sugestão 2 (Item da lista)", "..."],
  "caminhos_carreira": [
    {
      "titulo": "string - Ex: Backend Python",
      "compatibilidade": "string - Nível de compatibilidade (Ex: Alta, Média).",
      "desenvolvimento_necessario": "string - O que precisa ser desenvolvido para consistência profissional.",
      "oportunidades": "string - Oportunidades no mercado e tipos de empresa."
    }
    // Inclua mais dois objetos de caminho similar
  ]
}
        """

        prompt = f"""
Você é um mentor de carreira em tecnologia especializado em análise de perfil técnico e orientação profissional baseada em competências.

Regras obrigatórias de Formato:
- O resultado deve ser **SOMENTE** o objeto JSON.
- Siga rigorosamente a **ESTRUTURA JSON OBRIGATÓRIA** definida abaixo.
- Não use nenhum bloco de código Markdown (ex: ```json).
- Não escreva nenhum texto introdutório, explicativo ou conclusivo fora do JSON.
- Mantenha o tom construtivo, motivador e direto ao ponto.

ESTRUTURA JSON OBRIGATÓRIA:
{json_schema_analysis}

O conteúdo do JSON deve ser gerado seguindo os seguintes requisitos de análise:

1. **Forças técnicas identificadas** (Popule a lista 'forcas_tecnicas')
- Grau de maturidade técnica
- Clareza do foco profissional
- Estilo de aprendizado e possíveis padrões comportamentais inferidos
- Tecnologias dominadas
- Soft skills aplicáveis ao mercado
- Padrões de comportamento positivos e evidências práticas

2. **Fraquezas ou lacunas** (Popule a lista 'pontos_melhorar')
- Tecnologias mais consolidadas
- Competências transferíveis entre áreas
- Evidências de autonomia, consistência ou boas práticas
- Skills essenciais faltando para avançar
- Tecnologias que precisam ser estudadas imediatamente
- Gaps que impedem evolução para o próximo nível

3. **Três Caminhos de Carreira Possíveis** (Popule a lista 'caminhos_carreira')
Para cada caminho inclua:
- Título (ex: Backend Python, Data Science, Cloud Engineering)
- Nível de compatibilidade com o perfil
- O que precisa ser desenvolvido para atingir consistência profissional
- Oportunidades no mercado e tipos de empresa

4. **Ações Práticas de Curto Prazo (7–30 dias)** (Popule a lista 'sugestoes_curto_prazo')
- Cursos muito específicos
- Projetos pequenos e objetivos para portfólio
- Documentação ou tecnologias para estudar
- Pequenos desafios semanais de prática

Agora avalie o seguinte perfil:
Perfil:
{profile_summary}
"""
        # CHAMADA À API GEMINI:
        response = self.model.generate_content(prompt)
        return json.loads(response.text) # Retorna um dicionário Python

    def generate_roadmap(self, goal):
        
        json_schema_roadmap = """
{
  "meta_carreira": "string - O objetivo de carreira (ex: Backend Python).",
  "fundamentos_essenciais": ["string - Fundamento 1", "string - Fundamento 2", "..."],
  "projetos_praticos": [
    {
      "titulo": "string - Nome do Projeto",
      "objetivo": "string - O que será construído e por que é importante.",
      "desenvolve_habilidades": "string - Habilidades técnicas específicas que desenvolve na prática."
    }
    // Inclua de 3 a 6 objetos de projeto no total
  ],
  "ferramentas_essenciais": [
    {
      "nome": "string - Ex: Django/FastAPI",
      "prioridade": "string - Ex: Alta, Média, Baixa",
      "quando_aprender": "string - Momento no cronograma (Ex: Dia 30, Dia 60).",
      "conexao_mercado": "string - Por que é crucial no mercado de trabalho."
    }
    // Inclua outras ferramentas
  ],
  "plano_30_dias": {"objetivos": ["string - Objetivo 1", "..."], "atividades": ["string - Atividade 1", "..."]},
  "plano_60_dias": {"objetivos": ["string - Objetivo 1", "..."], "atividades": ["string - Atividade 1", "..."]},
  "plano_90_dias": {"objetivos": ["string - Objetivo 1", "..."], "atividades": ["string - Atividade 1", "..."]},
  "resultado_90_dias_esperado": "string - O que o estudante será capaz de fazer, nível de proficiência e próximos passos."
}
        """

        prompt = f"""
Gere um roadmap prático de aprendizado para o objetivo de carreira: **{goal}**.

Regras obrigatórias de Formato:
- O resultado deve ser **SOMENTE** o objeto JSON.
- Siga rigorosamente a **ESTRUTURA JSON OBRIGATÓRIA** definida abaixo.
- Não use nenhum bloco de código Markdown.
- Retorne APENAS o JSON válido.

ESTRUTURA JSON OBRIGATÓRIA:
{json_schema_roadmap}

O conteúdo do JSON deve ser gerado seguindo os seguintes requisitos:

1. **Fundamentos essenciais** (Popule 'fundamentos_essenciais')
- O que realmente precisa ser dominado
- Por que cada fundamento é importante
- Nível mínimo esperado pelo mercado

2. **Projetos práticos obrigatórios** (Popule a lista 'projetos_praticos')
- 3 a 6 projetos concretos que construam experiência real
- Explicando o que cada projeto desenvolve na prática (ex: APIs, bancos de dados, arquitetura, dados, etc.)

3. **Ferramentas, linguagens e frameworks essenciais** (Popule a lista 'ferramentas_essenciais')
- Linguagens, bibliotecas, frameworks, plataformas e ferramentas da área
- Por que cada ferramenta importa
- Quando aprender cada uma no cronograma
- Prioridade (alta, média, baixa)
- Como isso se conecta ao mercado

4. **Plano de evolução 30 / 60 / 90 dias** (Popule os objetos 'plano_30_dias', 'plano_60_dias', 'plano_90_dias')
- Objetivos claros e mensuráveis
- Atividades semanais
- Materiais recomendados (tipos, não links)
- Metas de portfólio
- Sinais de que o aluno está pronto para avançar

5. **Resultado esperado ao final dos 90 dias** (Popule 'resultado_90_dias_esperado')
- O que o estudante será capaz de fazer
- Nível de proficiência
- Possíveis próximos passos na carreira
"""
        # CHAMADA À API GEMINI:
        response = self.model.generate_content(prompt)
        return json.loads(response.text) 