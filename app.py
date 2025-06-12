# FORMULARIO PARA COLETA DE DADOS DA PESQUISA DO SENTIMENTO DO USUÁRIO
import streamlit as st
import sys
import os

# Adiciona o diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa as funções do banco de dados
from db.db_resp_usuario import salvar_resposta

st.title("Formulário de Pesquisa de Satisfação - Serviço de Limpeza")

# Inicializa o estado da sessão
if 'show_success' not in st.session_state:
    st.session_state.show_success = False
if 'last_submission' not in st.session_state:
    st.session_state.last_submission = None

# Inicializa os valores dos campos do formulário
if 'setor_value' not in st.session_state:
    st.session_state.setor_value = None
if 'material_limpeza_value' not in st.session_state:
    st.session_state.material_limpeza_value = None
if 'material_value' not in st.session_state:
    st.session_state.material_value = None
if 'qualidade_value' not in st.session_state:
    st.session_state.qualidade_value = None
if 'mensagem_value' not in st.session_state:
    st.session_state.mensagem_value = ""

# Mostra mensagem de sucesso apenas uma vez após o envio
if st.session_state.show_success and st.session_state.last_submission:
    st.success(f"✅ Pesquisa enviada com sucesso! Obrigado pela sua participação.")
    st.info(f"📊 Dados registrados: {st.session_state.last_submission}")
    # Limpa a flag para não mostrar novamente na próxima interação
    st.session_state.show_success = False

with st.form(key="sentiment_form"):
    setor = st.selectbox(
        "Setor", 
        index=None if st.session_state.setor_value is None else ["Contratos", "Contabilidade", "TI"].index(st.session_state.setor_value),
        options=["Contratos", "Contabilidade", "TI"],
        key="setor_select"
    )
    
    material_de_limpeza = st.radio(
        "Esta faltando algum material de limpeza?", 
        index=None if st.session_state.material_limpeza_value is None else ["Sim", "Não"].index(st.session_state.material_limpeza_value),
        options=["Sim", "Não"],
        key="material_limpeza_radio"
    )
    
    material = st.radio(
        "Qual material está faltando?", 
        options=["Sabonete", "Papel higiênico", "Papel toalha"],
        index=None if st.session_state.material_value is None else ["Sabonete", "Papel higiênico", "Papel toalha"].index(st.session_state.material_value),
        key="material_radio"
    )
    
    qualidade_do_servico = st.radio(
        "Qual a qualidade do serviço de limpeza?", 
        index=None if st.session_state.qualidade_value is None else ["Muito Bom", "Bom", "Regular", "Ruim"].index(st.session_state.qualidade_value),
        options=["Muito Bom", "Bom", "Regular", "Ruim"],
        key="qualidade_radio"
    )
    
    mensagem = st.text_area(
        "Deixe sua opinião",
        value=st.session_state.mensagem_value,
        key="mensagem_textarea"
    )
    
    enviar = st.form_submit_button("Enviar")
    
    # Processamento do formulário
    if enviar:
        # Validação dos campos obrigatórios
        if not setor:
            st.error("❌ Por favor, selecione um setor.")
        elif not material_de_limpeza:
            st.error("❌ Por favor, responda se está faltando material de limpeza.")
        elif not qualidade_do_servico:
            st.error("❌ Por favor, avalie a qualidade do serviço.")
        else:
            try:
                # Salva a resposta no banco de dados
                sucesso = salvar_resposta(
                    setor=setor,
                    material_faltando=material_de_limpeza,
                    qual_material=material if material_de_limpeza == "Sim" else None,
                    qualidade_servico=qualidade_do_servico,
                    mensagem=mensagem if mensagem else None
                )
                
                if sucesso:
                    # Atualiza o estado da sessão
                    st.session_state.show_success = True
                    st.session_state.last_submission = f"{setor} - {qualidade_do_servico}"
                    
                    # LIMPA OS CAMPOS DO FORMULÁRIO
                    st.session_state.setor_value = None
                    st.session_state.material_limpeza_value = None
                    st.session_state.material_value = None
                    st.session_state.qualidade_value = None
                    st.session_state.mensagem_value = ""
                    
                    # Recarrega a página para mostrar a mensagem de sucesso e campos limpos
                    st.rerun()
                else:
                    st.error("❌ Erro ao enviar a pesquisa. Tente novamente.")
                    
            except Exception as e:
                st.error(f"❌ Erro ao conectar com o banco de dados: {str(e)}")
                st.error("🔧 Verifique se o banco PostgreSQL está rodando e acessível.")







