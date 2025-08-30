import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import random
import base64

logo = "pages/logos/ChatGPT_Image_30_08_2025__10_44_17-removebg-preview.png"

st.set_page_config(
    page_title="Resumo Financeiro - Léo",
    page_icon="logo",  # pode ser emoji ou arquivo
    layout="wide"
)


# Função para converter imagem em base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


# Carrega logo local
logo_64 = get_base64_of_bin_file("pages/logos/ChatGPT_Image_30_08_2025__10_44_17-removebg-preview.png")




# =============================
# CONFIGURAÇÃO DE TEMA ELEGANTE
# =============================

# Paleta de cores elegante - Dourado, Azul e Roxo
COLORS = {
    'primary_gold': '#D4AF37',      # Dourado elegante
    'secondary_blue': '#1E3A8A',    # Azul royal profundo
    'accent_purple': '#7C3AED',     # Roxo vibrante
    'light_gold': '#F7E7CE',        # Dourado claro
    'dark_blue': '#0F172A',         # Azul escuro
    'soft_purple': '#A78BFA',       # Roxo suave
    'gradient_gold': '#FFD700',     # Dourado brilhante
    'navy': '#1E40AF',              # Azul marinho
    'lavender': '#8B5CF6'           # Lavanda
}

# Template customizado elegante
ELEGANT_TEMPLATE = {
    'layout': {
        #'paper_bgcolor': 'rgba(47, 53, 59, 0.95)',
        'paper_bgcolor': 'rgba(15, 23, 42, 0.95)',  # Fundo escuro elegante
        'plot_bgcolor': 'rgba(30, 58, 138, 0.1)',   # Fundo dos gráficos
        'font': {
            'family': 'Georgia, serif',
            'size': 12,
            'color': '#F8FAFC'
        },
        'title': {
            'font': {
                'family': 'Georgia, serif',
                'size': 18,
                'color': COLORS['primary_gold']
            },
            'x': 0.5,
            'xanchor': 'center'
        },
        'xaxis': {
            'gridcolor': 'rgba(212, 175, 55, 0.2)',
            'linecolor': COLORS['primary_gold'],
            'tickcolor': COLORS['light_gold'],
            'title_font_color': COLORS['light_gold']
        },
        'yaxis': {
            'gridcolor': 'rgba(212, 175, 55, 0.2)',
            'linecolor': COLORS['primary_gold'],
            'tickcolor': COLORS['light_gold'],
            'title_font_color': COLORS['light_gold']
        },
        'legend': {
            'bgcolor': 'rgba(30, 58, 138, 0.8)',
            'bordercolor': COLORS['primary_gold'],
            'borderwidth': 1,
            'font_color': COLORS['light_gold']
        }
    }
}

# CSS customizado para o Streamlit
st.markdown("""
<style>
    .main > div {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        padding: 2rem;
        border-radius: 15px;
    }
    
    .stMetric {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(212, 175, 55, 0.3);
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.2);
    }
    
    h1, h2, h3 {
        color: #D4AF37 !important;
        font-family: 'Georgia', serif !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

# Injeta no HTML/CSS
st.markdown(
    f"""
    <style>
        .logo-container {{
            position: fixed;
            top: 50px;
            right: 20px;
            z-index: 100;
        }}
        .logo-container img {{
            width: 130px;
        }}
    </style>
    <div class="logo-container">
        <img src="data:image/png;base64,{logo_64}">
    </div>
    """,
    unsafe_allow_html=True
)



# =============================
# Carregar DataFrames
# =============================

@st.cache_data
def load_data(path: str):
    try:
        data = pd.read_csv(path,index_col=0)
        return data
    except FileNotFoundError:
        st.error(f'Arquivo Não encontrado: {path}')
        return pd.DataFrame()

df_gastos_leo = load_data("pages/data/gastos_leo.csv")
df_gastos_leo = df_gastos_leo.round(2)
df_rendas_leo = load_data("pages/data/rendas_leo.csv")
df_rendas_leo = df_rendas_leo.round(2)
df_saldo_mes = load_data("pages/data/saldo_mes.csv")
df_saldo_mes = df_saldo_mes.round(2)
valor_inicial_investimentos = 2958.80 - 98.12 - 149.94
df_investimentos_leo = load_data('pages/data/investimento.csv')

# =============================
# Construindo Gráficos Elegantes
# =============================

@st.cache_data
def graf_valor_investido():
    df = df_investimentos_leo
    
    fig = go.Figure()
    
    # Linha principal com gradiente
    fig.add_trace(go.Scatter(
        x=df['mês'],
        y=df['Valor Aplicado'],
        mode='lines+markers',
        line=dict(
            color=COLORS['primary_gold'],
            width=4,
            shape='spline'
        ),
        marker=dict(
            color=COLORS['gradient_gold'],
            size=10,
            symbol='diamond',
            line=dict(color=COLORS['dark_blue'], width=2)
        ),
        name='Valor Investido',
        fill='tonexty',
        fillcolor='rgba(212, 175, 55, 0.2)'
    ))
    
    # Área de fundo gradiente
    fig.add_trace(go.Scatter(
        x=df['mês'],
        y=[0] * len(df),
        mode='lines',
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=False,
        hoverinfo='skip'
    ))

    fig.update_layout(
        paper_bgcolor='rgba(15, 23, 42, 0.95)',
        plot_bgcolor='rgba(30, 58, 138, 0.1)',
        font_family='Georgia, serif',
        font_color='#F8FAFC',
        title_font_color=COLORS['primary_gold'],
        title_x=0.5,
        title="💰 Evolução do Valor Investido",
        height=400,
        margin=dict(t=80, b=60, l=60, r=60)
    )
    layout_config = ELEGANT_TEMPLATE['layout'].copy()
    layout_config['title'] = "💰 Evolução do Valor Investido"
    st.plotly_chart(fig, use_container_width=True)

@st.cache_data
def graf_renda_bruta_disponível():
    df = df_rendas_leo
    
    fig = go.Figure()
    
    # Renda Bruta
    fig.add_trace(go.Scatter(
        x=df['mês'],
        y=df['Renda Bruta'],
        mode='lines+markers',
        line=dict(
            color=COLORS['secondary_blue'],
            width=3,
            shape='spline'
        ),
        marker=dict(
            color=COLORS['navy'],
            size=8,
            symbol='circle'
        ),
        name='Renda Bruta'
    ))
    
    # Renda Disponível
    fig.add_trace(go.Scatter(
        x=df['mês'],
        y=df['Renda disponível'],
        mode='lines+markers',
        line=dict(
            color=COLORS['accent_purple'],
            width=3,
            shape='spline'
        ),
        marker=dict(
            color=COLORS['lavender'],
            size=8,
            symbol='square'
        ),
        name='Renda Disponível'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(15, 23, 42, 0.95)',
        plot_bgcolor='rgba(30, 58, 138, 0.1)',
        font_family='Georgia, serif',
        font_color='#F8FAFC',
        title_font_color=COLORS['primary_gold'],
        title_x=0.5,
        title="📈 Renda Bruta vs Renda Disponível",
        height=400,
        margin=dict(t=80, b=60, l=60, r=60)
    )
    
    st.plotly_chart(fig, use_container_width=True)

@st.cache_data
def graf_investimentos():
    df = df_investimentos_leo
    
    # Verificar se as colunas existem
    if 'Rendimento' not in df.columns:
        st.error(f"Coluna 'Rendimento' não encontrada. Colunas disponíveis: {list(df.columns)}")
        return
    
    # Transformando em formato longo
    df_long = df.melt(
        id_vars=['mês'],
        value_vars=['Valor Aplicado', 'Rendimento'],
        var_name='Tipo',
        value_name='Valor'
    )
    
    # Gráfico de barras elegante
    fig = go.Figure()
    
    # Valor Aplicado
    valores_aplicados = df_long[df_long['Tipo'] == 'Valor Aplicado']
    fig.add_trace(go.Bar(
        x=valores_aplicados['mês'],
        y=valores_aplicados['Valor'],
        name='Valor Aplicado',
        marker=dict(
            color=COLORS['primary_gold'],
            line=dict(color=COLORS['dark_blue'], width=1.5),
            pattern_shape="/"
        ),
        opacity=0.8
    ))
    
    # Rendimento
    rendimentos = df_long[df_long['Tipo'] == 'Rendimento']
    fig.add_trace(go.Bar(
        x=rendimentos['mês'],
        y=rendimentos['Valor'],
        name='Rendimento',
        marker=dict(
            color=COLORS['accent_purple'],
            line=dict(color=COLORS['dark_blue'], width=1.5)
        ),
        opacity=0.8
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(15, 23, 42, 0.95)',
        plot_bgcolor='rgba(30, 58, 138, 0.1)',
        font_family='Georgia, serif',
        font_color='#F8FAFC',
        title_font_color=COLORS['primary_gold'],
        title_x=0.5,
        title=" Investimentos vs Rendimentos",
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1,
        height=400,
        margin=dict(t=80, b=60, l=60, r=60)
    )
    
    st.plotly_chart(fig, use_container_width=True)

@st.cache_data
def graf_comparacao_rendas():
    df = df_rendas_leo.copy()

    # Criar subplots elegantes
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        specs=[[{"type": "xy"}], [{"type": "table"}]],
        subplot_titles=("Análise Comparativa", "Dados Detalhados")
    )

    # Barras com gradiente
    colors = [COLORS['secondary_blue'], COLORS['accent_purple'], COLORS['primary_gold']]
    columns = ['Renda Bruta', 'Renda disponível', 'Lucro']
    
    for i, col in enumerate(columns):
        fig.add_trace(
            go.Bar(
                x=df['mês'], 
                y=df[col],
                name=col,
                marker=dict(
                    color=colors[i],
                    line=dict(color=COLORS['dark_blue'], width=1),
                    opacity=0.8
                ),
                text=df[col].round(2),
                textposition='auto'
            ),
            row=1, col=1
        )

    # Tabela elegante
    fig.add_trace(
        go.Table(
            header=dict(
                values=[f"<b>{col}</b>" for col in df.columns.tolist()],
                fill_color=COLORS['secondary_blue'],
                font=dict(color='white', size=12),
                align="center",
                line=dict(color='white', width=0.1),
                height=0
            ),
            cells=dict(
                values=[df[col].tolist() for col in df.columns],
                fill_color=[['rgba(212, 175, 55, 0.1)', 'rgba(124, 58, 237, 0.1)'] * len(df)],
                font=dict(color='white', size=11),
                align="center",
                line=dict(color='white', width=0.1),
                height=35
            )
        ),
        row=2, col=1
    )

    fig.update_layout(
        paper_bgcolor='rgba(15, 23, 42, 0.95)',
        plot_bgcolor='rgba(30, 58, 138, 0.1)',
        font_family='Georgia, serif',
        font_color='#F8FAFC',
        title_font_color=COLORS['primary_gold'],
        title_x=0.5,
        height=700,
        title_text="👑 Comparação Completa de Rendas",
        barmode='group',
        showlegend=True,
        margin=dict(t=100, l=50, r=50, b=50)
    )

    st.plotly_chart(fig, use_container_width=True)

@st.cache_data
def graf_gastos():
    porcentagem_ideal = {
        'Alimentação Léo %': 13.33,
        'Aplicação %': 15.00,
        'Conta fixa Léo %': 45.00,
        'Doação Léo %': 10.00,
        'Empréstimo saída Léo %': 0,
        'Extras Léo %': 5,
        'Passeios Léo %': 5,
        'Transporte Léo %': 4
    }
    
    # Criar palette de cores elegante para categorias
    category_colors = [
        COLORS['primary_gold'], COLORS['secondary_blue'], COLORS['accent_purple'],
        COLORS['soft_purple'], COLORS['gradient_gold'], COLORS['navy'],
        COLORS['lavender'], '#B45309'  # Bronze para completar
    ]
    
    df_ideal = pd.DataFrame([porcentagem_ideal])
    df_ideal['mês'] = 'Ideal'
    
    df_porcentagem_long = df_gastos_leo.melt(
        id_vars=['mês'],
        value_vars=list(porcentagem_ideal.keys()),
        var_name='Tipo',
        value_name='Valor'
    )
        
    df_ideal_long = df_ideal.melt(
        id_vars=['mês'],
        value_vars=list(porcentagem_ideal.keys()),
        var_name='Tipo',
        value_name='Valor'
    )
    
    df_final = pd.concat([df_ideal_long, df_porcentagem_long], ignore_index=True)

    fig = go.Figure()
    
    # Criar barras empilhadas com cores elegantes
    tipos_unicos = df_final['Tipo'].unique()
    
    for i, tipo in enumerate(tipos_unicos):
        dados_tipo = df_final[df_final['Tipo'] == tipo]
        
        fig.add_trace(go.Bar(
            x=dados_tipo['mês'],
            y=dados_tipo['Valor'],
            #title="🏆 Análise Elegante de Gastos vs Ideal",
            name=tipo.replace(' %', ''),
            marker=dict(
                color=category_colors[i % len(category_colors)],
                line=dict(color=COLORS['dark_blue'], width=0.5),
                opacity=0.85
            ),
            text=dados_tipo['Valor'].round(1),
            textposition='inside',
            textfont=dict(color='white', size=10)
        ))

    fig.update_layout(
        paper_bgcolor='rgba(15, 23, 42, 0.95)',
        plot_bgcolor='rgba(30, 58, 138, 0.1)',
        font_family='Georgia, serif',
        font_color='#F8FAFC',
        title_font_color=COLORS['primary_gold'],
        title_x=0.5,
        title="🏆 Análise Elegante de Gastos vs Ideal",
        barmode='stack',
        bargap=0.4,
        height=500,
        margin=dict(t=80, b=60, l=60, r=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("📊 Visualizar Dados Detalhados"):
        st.dataframe(df_gastos_leo, use_container_width=True)

def create_elegant_metric(value, title, prefix="EUR ", icon="💰"):
    """Cria uma métrica elegante com design sofisticado"""
    
    fig = go.Figure()
    
    # Indicador principal
    fig.add_trace(
        go.Indicator(
            value=value,
            mode="number",
            number={
                'prefix': prefix,
                'suffix': '',
                'font': {
                    'size': 28,
                    'color': COLORS['primary_gold'],
                    'family': 'Georgia, serif'
                },
            },
            title={
                'text': f"{icon} {title}",
                'font': {
                    'size': 16,
                    'color': COLORS['light_gold'],
                    'family': 'Georgia, serif'
                },
            },
            domain={'x': [0, 1], 'y': [0.3, 1]}
        ),
        
    )
    
    # Efeito de fundo elegante
    fig.add_trace(
        go.Scatter(
            x=list(range(50)),
            y=[abs(x * 0.5 * random.random()) for x in range(50)],
            mode='lines',
            fill='tonexty',
            fillcolor=f'rgba({int(COLORS["primary_gold"][1:3], 16)}, {int(COLORS["primary_gold"][3:5], 16)}, {int(COLORS["primary_gold"][5:7], 16)}, 0.1)',
            line=dict(color=COLORS['primary_gold'], width=1, shape='spline'),
            hoverinfo="skip",
            showlegend=False
        )
    )

    fig.update_layout(
        
        paper_bgcolor='rgba(15, 23, 42, 0.9)',
        plot_bgcolor='rgba(30, 58, 138, 0.1)',
        margin=dict(t=20, b=0, l=10, r=10),
        height=120,
        showlegend=False,
        xaxis=dict(visible=False, fixedrange=True),
        yaxis=dict(visible=False, fixedrange=True)
    )

    return fig

# Métricas elegantes
@st.cache_data
def metrixs_valor_em_conta():
    fig = create_elegant_metric(
        df_saldo_mes['Saldo Inicial'].iloc[-1], 
        "Valor em Conta", 
        icon="🏦"
    )
    st.plotly_chart(fig, use_container_width=True)

@st.cache_data
def metrixs_renda_bruta_media():
    fig = create_elegant_metric(
        df_rendas_leo['Renda Bruta'].mean(), 
        "Renda Bruta Média", 
        icon="📊"
    )
    st.plotly_chart(fig, use_container_width=True)

@st.cache_data
def metrixs_gastos_medio():
    df = df_gastos_leo.copy()
    colunas = df.columns.drop('mês').tolist()
    df['Total'] = df[colunas].sum(axis=1)
    
    fig = create_elegant_metric(
        df['Total'].mean(), 
        "Gastos Médios", 
        icon="💳"
    )
    st.plotly_chart(fig, use_container_width=True)
    
@st.cache_data
def metrixs_valor_investido():
    df = df_investimentos_leo.copy()
    colunas = df.columns.drop('mês').tolist()
    df['Total'] = df[colunas].sum(axis=1)
    
    fig = create_elegant_metric(
        df['Total'].sum() + valor_inicial_investimentos, 
        "Total Investido", 
        icon="💎"
        
    )
    st.plotly_chart(fig, use_container_width=True)

# =============================
# LAYOUT PRINCIPAL ELEGANTE
# =============================

st.markdown("# Resumo Financeiro - Léo")
st.markdown("---")

st.sidebar.image(logo,use_container_width=True)

# PRIMEIRA LINHA - 4 colunas (Métricas)
st.markdown("### 📊 Indicadores Principais")
col1, col2, col3, col4 = st.columns(4)

with col1:
    metrixs_valor_em_conta()

with col2:
    metrixs_valor_investido()

with col3:
    metrixs_renda_bruta_media()

with col4:
    metrixs_gastos_medio()

st.markdown("---")

# SEGUNDA LINHA - 2 colunas (Gráficos de linha)
st.markdown("### 📈 Análise Temporal")
col5, col6 = st.columns(2)

with col5:
    graf_valor_investido()

with col6:
    graf_renda_bruta_disponível()

st.markdown("---")

# TERCEIRA LINHA - 2 colunas (Gráficos comparativos)
st.markdown("### 🔍 Análise Comparativa")
col7, col8 = st.columns(2)

with col7:
    graf_investimentos()

with col8:
    graf_comparacao_rendas()

st.markdown("---")

# QUARTA LINHA - 1 coluna (Gráfico completo)
st.markdown("### 🏆 Visão Completa dos Gastos")
graf_gastos()

st.markdown("---")
st.markdown("##### ✨ Dashboard criado com elegância e sofisticação por função finanças")
