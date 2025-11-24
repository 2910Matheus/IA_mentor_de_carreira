import streamlit as st # type:ignore
from github_collector import GitHubCollector
from analyzer import SkillAnalyzer
from mentor_ai import MentorAI 
import pandas as pd # type:ignore

st.set_page_config(
    page_title="Mentor IA de Carreira",
    page_icon="🤖",
    layout="wide"
)

# ============================
# ESTILO GLOBAL 
# ============================
GLOBAL_CSS = """
<style>
body {
    background-color: #f5f7fa;
    font-family: Arial, sans-serif;
}

.title {
    font-size: 36px;
    font-weight: bold;
    color: #333;
    margin-bottom: 10px;
}

.subtitle {
    font-size: 18px;
    color: #555;
}

/* NOVO: Estilo base para os containers gerados pelo Streamlit/Markdown */
.json-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #ddd;
    box-shadow: 0 1px 6px rgba(0,0,0,0.08);
    margin-top: 20px;
    margin-bottom: 20px; /* Adiciona espaço entre os cards */
}
</style>
"""

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ============================
# TÍTULO
# ============================
st.markdown("<div class='title'>🤖 Mentor IA de Carreira</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Seu orientador profissional guiado por IA, baseado nos seus dados reais do GitHub</div>", unsafe_allow_html=True)

st.write("---")

# ============================
# FORMULÁRIO DE INPUT
# ============================
with st.form("form"):
    username = st.text_input("🔎 Informe seu GitHub:", placeholder="ex: torvalds")

    objetivo = st.text_input(
        "🎯 Informe seu objetivo de carreira:",
        placeholder="ex: Backend Python, Data Science, Full Stack, DevOps..."
    )

    submitted = st.form_submit_button("Gerar Análise ➜")

# ============================
# PROCESSAMENTO E RENDERIZAÇÃO
# ============================
if submitted:

    if not username.strip():
        st.error("Por favor, insira um nome de usuário do GitHub.")
        st.stop()

    if not objetivo.strip():
        st.error("Por favor, insira um objetivo de carreira.")
        st.stop()

    try:
        # Inicialização e Coleta de Dados
        st.info("🔍 Coletando dados do GitHub...")
        collector = GitHubCollector(username)
        raw_data = collector.collect_profile_data()

        st.info("🧠 Analisando perfil técnico...")
        analyzer = SkillAnalyzer()
        analyzed = analyzer.analyze(raw_data)

        st.info("🤖 Gerando insights com IA (Gemini)...")
        ai = MentorAI()
        
        # OBTENDO DADOS JSON
        feedback_data = ai.analyze_profile(analyzed) 
        roadmap_data = ai.generate_roadmap(objetivo) 

        # ============================
        # EXIBIR RESULTADOS
        # ============================
        st.write("---")
        st.markdown("<h2>🧠 Análise do Mentor IA</h2>", unsafe_allow_html=True)
        
        # -----------------------------
        # 1. RESUMO GERAL
        # -----------------------------
        st.markdown("<div class='json-card'>", unsafe_allow_html=True)
        st.subheader("📌 Resumo Geral do Perfil")
        st.write(feedback_data.get("resumo_geral", "Resumo não encontrado."))
        st.markdown("</div>", unsafe_allow_html=True)

        # -----------------------------
        # 2. FORÇAS E PONTOS A MELHORAR
        # -----------------------------
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='json-card'>", unsafe_allow_html=True)
            st.subheader("💡 Forças Técnicas")
            for item in feedback_data.get("forcas_tecnicas", []):
                 st.success(f"✅ {item}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='json-card'>", unsafe_allow_html=True)
            st.subheader("⚠️ Pontos a Melhorar")
            for item in feedback_data.get("pontos_melhorar", []):
                st.warning(f"❗ {item}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # -----------------------------
        # 3. SUGESTÕES DE CURTO PRAZO
        # -----------------------------
        st.markdown("<div class='json-card'>", unsafe_allow_html=True)
        st.subheader("🚀 Sugestões de Curto Prazo (7-30 dias)")
        for item in feedback_data.get("sugestoes_curto_prazo", []):
            st.info(f"👉 {item}")
        st.markdown("</div>", unsafe_allow_html=True)

        # -----------------------------
        # 4. CAMINHOS DE CARREIRA
        # -----------------------------
        st.markdown("<h3>🎯 Possíveis Caminhos de Carreira</h3>", unsafe_allow_html=True)
        
        caminhos = feedback_data.get("caminhos_carreira", [])
        
        # expander para cada caminho de carreira
        for i, caminho in enumerate(caminhos):
            title = caminho.get('titulo', f'Caminho {i+1}')
            compatibilidade = caminho.get('compatibilidade', 'Nível não especificado')
            
            with st.expander(f"**{title}** - Compatibilidade: {compatibilidade}"):
                st.markdown(f"**O que precisa ser desenvolvido:** {caminho.get('desenvolvimento_necessario', 'N/A')}")
                st.markdown(f"**Oportunidades no Mercado:** {caminho.get('oportunidades', 'N/A')}")
        
        st.write("---")
        
        # ============================
        # EXIBIR ROADMAP
        # ============================
        st.markdown("<h2>🗺️ Roadmap Personalizado</h2>", unsafe_allow_html=True)

        # -----------------------------
        # 1. FUNDAMENTOS
        # -----------------------------
        with st.container():
            st.markdown("<div class='json-card' style='background-color:#e6f3ff; border-left: 5px solid #007bff;'>", unsafe_allow_html=True)
            st.subheader("✅ Fundamentos Essenciais")
            for f in roadmap_data.get('fundamentos_essenciais', []):
                st.markdown(f"• **{f}**")
            st.markdown("</div>", unsafe_allow_html=True)

        # -----------------------------
        # 2. FERRAMENTAS ESSENCIAIS
        # -----------------------------
        with st.container():
            st.markdown("<div class='json-card'>", unsafe_allow_html=True)
            st.subheader("🛠️ Ferramentas, Linguagens e Frameworks Essenciais")
            if roadmap_data.get("ferramentas_essenciais"):
                df = pd.DataFrame(roadmap_data["ferramentas_essenciais"])
                df.columns = ["Nome", "Prioridade", "Quando Aprender", "Conexão Mercado"]
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("Nenhuma ferramenta essencial especificada.")
            st.markdown("</div>", unsafe_allow_html=True)

        # -----------------------------
        # 3. PROJETOS PRÁTICOS
        # -----------------------------
        with st.container():
            st.markdown("<div class='json-card' style='background-color:#fff8e1; border-left: 5px solid #ffc107;'>", unsafe_allow_html=True)
            st.subheader("🏗️ Projetos Práticos Obrigatórios")

            projetos = roadmap_data.get("projetos_praticos", [])
            for i, projeto in enumerate(projetos):
                st.markdown(f"**{i+1}. {projeto.get('titulo', 'Projeto Sem Nome')}**")
                st.markdown(f"*Objetivo:* {projeto.get('objetivo', 'N/A')}")
                st.markdown(f"*Desenvolve Habilidades:* {projeto.get('desenvolve_habilidades', 'N/A')}")
                if i < len(projetos) - 1:
                    st.markdown("---")
            st.markdown("</div>", unsafe_allow_html=True)

        # -----------------------------
        # 4. PLANO DE EVOLUÇÃO (30/60/90 dias)
        # -----------------------------
        with st.container():
            st.markdown("<div class='json-card'>", unsafe_allow_html=True)
            st.subheader("🗓️ Plano de Evolução")

            dias_planos = [
                ("📅 30 Dias", roadmap_data.get("plano_30_dias"), "#e8f5e8", "#28a745"),
                ("📅 60 Dias", roadmap_data.get("plano_60_dias"), "#fff3cd", "#ffc107"), 
                ("📅 90 Dias", roadmap_data.get("plano_90_dias"), "#d1ecf1", "#17a2b8")
            ]

            cols = st.columns(3)

            for i, (dias, plano, cor_fundo, cor_borda) in enumerate(dias_planos):
                if plano and cols[i]:
                    with cols[i]:
                        # Card individual para cada período
                        st.markdown(f"""
                        <div style='
                            background-color: {cor_fundo}; 
                            border-left: 5px solid {cor_borda};
                            border-radius: 10px;
                            padding: 15px;
                            margin: 5px;
                            height: 100%;
                        '>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"**{dias}**")
                        
                        if plano.get('objetivos'):
                            st.markdown("**🎯 Objetivos Chave:**")
                            for o in plano.get('objetivos', []):
                                st.markdown(f"• {o}")
                        
                        if plano.get('atividades'):
                            st.markdown("**📚 Atividades:**")
                            for a in plano.get('atividades', []):
                                st.markdown(f"• {a}")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

        # -----------------------------
        # 5. RESULTADO ESPERADO
        # -----------------------------
        with st.container():
            st.markdown("<div class='json-card' style='background-color:#f8f9fa; border-left: 5px solid #6c757d;'>", unsafe_allow_html=True)
            st.subheader("🏆 Resultado Final Esperado (90 Dias)")
            resultado = roadmap_data.get('resultado_90_dias_esperado', 'Resultado final não especificado.')
            st.info(resultado)
            st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"⚠️ Erro ao processar. Verifique o nome de usuário ou a API Key: {str(e)}")