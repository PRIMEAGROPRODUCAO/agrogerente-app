import streamlit as st
import pandas as pd
import datetime
import os

# Configuração de Layout e Identidade Visual Orgânica
st.set_page_config(page_title="AgroGerente PRO", page_icon="🍄", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f7f9f5; }
    h1, h2, h3 { color: #1e3512; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #3b5928; color: white; border-radius: 6px; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #263a1a; color: white; }
    div[data-testid="stMetricValue"] { color: #2a4d14; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Mecanismo de persistência simples em arquivos locais do servidor (Para não perder dados)
def carregar_dados(nome_arquivo, colunas):
    if os.path.exists(nome_arquivo):
        return pd.read_csv(nome_arquivo)
    return pd.DataFrame(columns=colunas)

def salvar_dados(df, nome_arquivo):
    df.to_csv(nome_arquivo, index=False)

# Inicialização dos arquivos de dados permanentes
ARQUIVO_LOTES = "banco_lotes.csv"
ARQUIVO_FINANCAS = "banco_financas.csv"
ARQUIVO_CONTATOS = "banco_contatos.csv"

if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

# TELA DE LOGIN SEGURA
if not st.session_state['autenticado']:
    st.title("🍄 AgroGerente: Gestão Autossuficiente")
    st.subheader("Acesso Restrito ao Administrador")
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        usuario = st.text_input("Usuário do Campo")
        senha = st.text_input("Senha de Acesso", type="password")
        if st.button("Autenticar Sistema"):
            if usuario == "admin" and senha == "123456":
                st.session_state['autenticado'] = True
                st.rerun()
            else:
                st.error("Credenciais inválidas. Verifique os dados.")
    st.stop()

# Navegação do App Profissional
opcao = st.sidebar.radio("Módulos do Sistema", [
    "📊 Painel Financeiro & ROI", 
    "🌱 Controle Rigoroso de Lotes", 
    "💸 Custos, Compras & WhatsApp", 
    "🤝 Carteira de Clientes/Fornecedores",
    "⚙️ Configurações & Logo"
])

# Carregamento de dados persistentes
df_lotes = carregar_dados(ARQUIVO_LOTES, ["Código Lote", "Cultura", "Variedade/Espécie", "Data Inicial", "Quantidade", "Fase Atual", "Perdas (%)"])
df_financas = carregar_dados(ARQUIVO_FINANCAS, ["Data", "Tipo", "Item", "Categoria", "Valor (R$)", "Origem"])
df_contatos = carregar_dados(ARQUIVO_CONTATOS, ["Tipo", "Nome", "Contato", "Documento/CPF/CNPJ"])

# CARGA INICIAL DE CUSTOS (SE O BANCO ESTIVER VAZIO)
if df_financas.empty:
    custos_iniciais = [
        {"Data": "2026-10-26", "Tipo": "Despesa Fixa", "Item": "Madeira para Barracão", "Categoria": "Estruturação", "Valor (R$)": 1200.0, "Origem": "Manual"},
        {"Data": "2026-10-26", "Tipo": "Despesa Fixa", "Item": "Telhas, Pregos e Parafusos", "Categoria": "Estruturação", "Valor (R$)": 850.0, "Origem": "Manual"},
        {"Data": "2026-10-26", "Tipo": "Despesa Fixa", "Item": "Sombrite e Lonas Plásticas", "Categoria": "Estruturação", "Valor (R$)": 450.0, "Origem": "Manual"},
        {"Data": "2026-10-26", "Tipo": "Despesa Variável", "Item": "Micélio de Cogumelo Shimeji", "Categoria": "Produção", "Valor (R$)": 320.0, "Origem": "Manual"}
    ]
    df_financas = pd.DataFrame(custos_iniciais)
    salvar_dados(df_financas, ARQUIVO_FINANCAS)

# 1. TELA: PAINEL FINANCEIRO & ROI
if opcao == "📊 Painel Financeiro & ROI":
    st.title("📊 Painel de Controle de Lucros e Custos")
    
    # Cálculos
    total_despesas = df_financas[df_financas["Tipo"].str.contains("Despesa")]["Valor (R$)"].sum()
    total_receitas = df_financas[df_financas["Tipo"] == "Receita"]["Valor (R$)"].sum()
    lucro_liquido = total_receitas - total_despesas
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Investimento Total", f"R$ {total_despesas:,.2f}")
    col2.metric("Faturamento Total", f"R$ {total_receitas:,.2f}")
    col3.metric("Lucro Líquido Real", f"R$ {lucro_liquido:,.2f}")
    
    # Alerta de perdas médias baseados nos lotes
    if not df_lotes.empty:
        perda_media = pd.to_numeric(df_lotes["Perdas (%)"]).mean()
        cor_perda = "🔴" if perda_media > 5 else "🟢"
        col4.metric("Taxa Média de Perda", f"{perda_media:.1f}% {cor_perda}")
    else:
        col4.metric("Taxa Média de Perda", "0.0% 🟢")

    st.subheader("📈 Histórico Completo de Entradas e Saídas (Fluxo de Caixa)")
    st.dataframe(df_financas, use_container_width=True)

# 2. TELA: CONTROLE RIGOROSO DE LOTES
elif opcao == "🌱 Controle Rigoroso de Lotes":
    st.title("🌱 Controle e Manejo Rigoroso de Cultivos")
    
    with st.expander("➕ Introduzir Novo Lote Automaticamente", expanded=True):
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            cultura = st.selectbox("Cultura", ["Cogumelo", "Tomate Cereja", "Microverdes"])
        with col_b:
            if cultura == "Cogumelo":
                especie = st.selectbox("Espécie/Variedade", ["Shimeji Preto", "Shimeji Branco", "Shitake", "Paris", "Portobello"])
            elif cultura == "Tomate Cereja":
                especie = st.selectbox("Espécie/Variedade", ["Tomate Cereja Doce", "Tomate Grape"])
            else:
                especie = st.selectbox("Espécie/Variedade", ["Rúcula", "Mostarda", "Couve", "Rabanete"])
        with col_c:
            quantidade = st.number_input("Quantidade (Blocos/Bandejas/Sacos)", min_value=1, value=10)
            
        data_plantio = st.date_input("Data Inicial / Inoculação", datetime.date.today())
        
        if st.button("Gerar Lote Rastreável"):
            prefixo = cultura[:3].upper()
            cod_gerado = f"LOT-{prefixo}-{data_plantio.strftime('%Y%m%d')}-{len(df_lotes)+1}"
            
            novo_lote = pd.DataFrame([{
                "Código Lote": cod_gerado, "Cultura": cultura, "Variedade/Espécie": especie,
                "Data Inicial": data_plantio.strftime("%Y-%m-%d"), "Quantidade": quantidade,
                "Fase Atual": "Inoculação/Plantio", "Perdas (%)": 0.0
            }])
            df_lotes = pd.concat([df_lotes, novo_lote], ignore_index=True)
            salvar_dados(df_lotes, ARQUIVO_LOTES)
            st.success(f"Lote criado e registrado: {cod_gerado}")

    st.subheader("📋 Atualização Diária de Manejo e Colheita")
    if not df_lotes.empty:
        lote_selecionado = st.selectbox("Selecione um Lote Ativo para Atualizar Manejo:", df_lotes["Código Lote"].unique())
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            nova_fase = st.selectbox("Nova Fase de Desenvolvimento:", ["Inoculação/Plantio", "Incubação", "Frutificação", "Colheita", "Finalizado"])
        with col_m2:
            nova_perda = st.slider("Ajustar Porcentagem de Perda Ocorrida (%):", 0.0, 100.0, 0.0, step=0.5)
        with col_m3:
            st.write("Confirmar Atualizações Diárias")
            if st.button("Salvar Evolução Diária"):
                df_lotes.loc[df_lotes["Código Lote"] == lote_selecionado, "Fase Atual"] = nova_fase
                df_lotes.loc[df_lotes["Código Lote"] == lote_selecionado, "Perdas (%)"] = nova_perda
                salvar_dados(df_lotes, ARQUIVO_LOTES)
                st.success("Manejo atualizado com sucesso no banco de dados!")
                st.rerun()

        st.dataframe(df_lotes, use_container_width=True)
    else:
        st.info("Nenhum lote em andamento. Introduza um lote acima.")

# 3. TELA: CUSTOS, COMPRAS & WHATSAPP
elif opcao == "💸 Custos, Compras & WhatsApp":
    st.title("💸 Lançamento de Gastos & Integração WhatsApp")
    
    st.subheader("📱 Simulador de Automação de Notas Fiscais (WhatsApp)")
    st.write("Cole o texto da mensagem ou cupom lido que você enviou no WhatsApp para simular a inserção automática na planilha:")
    
    texto_whatsapp = st.text_area("Exemplo: 'Gastei 150 reais em Embalagens para Cogumelos no fornecedor PlastSul hoje'", 
                                  placeholder="Digite ou simule um envio de mensagem aqui...")
    
    if st.button("Simular Processamento de IA do WhatsApp"):
        if texto_whatsapp:
            # Mecanismo Inteligente de Identificação de texto (IA baseada em regras)
            valor_identificado = 50.0 # valor padrão fallback
            for palavra in texto_whatsapp.split():
                if palavra.isdigit():
                    valor_identificado = float(palavra)
            
            categoria_identificada = "Produção"
            if "embalagem" in texto_whatsapp.lower():
                categoria_identificada = "Embalagem"
            elif "madeira" in texto_whatsapp.lower() or "telha" in texto_whatsapp.lower():
                categoria_identificada = "Estruturação"
            
            novo_gasto_zap = pd.DataFrame([{
                "Data": datetime.date.today().strftime("%Y-%m-%d"),
                "Tipo": "Despesa Variável",
                "Item": "Lançamento Automático WhatsApp",
                "Categoria": categoria_identificada,
                "Valor (R$)": valor_identificado,
                "Origem": "WhatsApp (OCR/Texto)"
            }])
            df_financas = pd.concat([df_financas, novo_gasto_zap], ignore_index=True)
            salvar_dados(df_financas, ARQUIVO_FINANCAS)
            st.success(f"🤖 IA identificou despesa de R$ {valor_identificado:.2f} na categoria '{categoria_identificada}' e jogou na planilha!")
        else:
            st.warning("Insira algum texto para rodar a simulação.")

    st.subheader("➕ Entrada Financeira Manual (Receitas / Despesas)")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        tipo_mov = st.selectbox("Tipo de Movimentação", ["Despesa Variável", "Despesa Fixa", "Receita"])
        item_nome = st.text_input("Descrição do Item (ex: Sacos plásticos, Venda de Tomate)")
    with col_f2:
