import streamlit as st
import pandas as pd
import numpy as np
import time
import altair as alt
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ExploraAI | SYSTEM ONLINE",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://unpkg.com/augmented-ui@2/augmented-ui.min.css">
        <style>
            :root {
                --bg-primary: #05050A;
                --bg-panel: #0d0d1a;
                --border-dim: #1E1E2F;
                --volt: #ADFF2F;
                --volt-dim: rgba(173, 255, 47, 0.1);
                --purple: #9D4EDD;
                --purple-dim: rgba(157, 78, 221, 0.1);
                --magenta: #FF007A;
                --magenta-dim: rgba(255, 0, 122, 0.1);
                --text-primary: #e8e8f0;
                --text-muted: #6b6b8a;
            }

            .stApp {
                background-color: var(--bg-primary);
                background-image: 
                    linear-gradient(rgba(173,255,47,0.03) 1px, transparent 1px), 
                    linear-gradient(90deg, rgba(173,255,47,0.03) 1px, transparent 1px);
                background-size: 40px 40px;
                color: var(--text-primary);
                font-family: 'Rajdhani', sans-serif;
            }

            h1, h2, h3, h4, h5, h6 {
                font-family: 'Orbitron', sans-serif;
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            [data-testid="collapsedControl"], [data-testid="stSidebar"] { display: none; }

            .stTabs [data-baseweb="tab-list"] {
                gap: 10px;
                background-color: transparent;
                border-bottom: 1px solid var(--border-dim);
            }
            .stTabs [data-baseweb="tab"] {
                font-family: 'Share Tech Mono', monospace;
                color: var(--text-muted);
                height: 50px;
                border-radius: 0;
                border: none;
                transition: all 0.3s;
                text-transform: uppercase;
            }
            .stTabs [data-baseweb="tab"]:hover {
                color: var(--volt);
                text-shadow: 0 0 8px var(--volt);
            }
            .stTabs [aria-selected="true"] {
                color: var(--volt) !important;
                border-bottom: 2px solid var(--volt) !important;
                background-color: var(--volt-dim) !important;
                text-shadow: 0 0 10px rgba(173, 255, 47, 0.5);
            }
            .stTabs [data-baseweb="tab-panel"] {
                padding-top: 2rem;
            }

            div[data-baseweb="select"] > div, input[type="text"], input[type="number"] {
                background-color: #0a0a14 !important;
                border: 1px solid var(--border-dim) !important;
                border-radius: 0 !important;
                color: var(--volt) !important;
                font-family: 'Share Tech Mono', monospace !important;
                clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px);
            }

            .stSlider [data-baseweb="slider"] {
                background: transparent !important;
            }
            .stSlider [data-baseweb="slider"] div[role="slider"] {
                background-color: var(--volt) !important;
                border-radius: 0;
                clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
                box-shadow: 0 0 10px var(--volt);
            }
            .stSlider [data-baseweb="slider"] > div:first-child > div:first-child { height: 3px; background-color: var(--border-dim); }
            .stSlider [data-baseweb="slider"] > div:first-child > div:nth-child(2) { height: 3px; background-color: var(--volt); }

            .stCheckbox label div[data-baseweb="checkbox"] > div {
                border-radius: 0;
                background-color: #0a0a14;
                border-color: var(--border-dim);
                clip-path: polygon(4px 0, 100% 0, 100% calc(100% - 4px), calc(100% - 4px) 100%, 0 100%, 0 4px);
            }

            [data-testid="stDataFrame"] {
                font-family: 'Share Tech Mono', monospace;
                border: 1px solid var(--border-dim);
            }
            .stDataFrame th {
                color: var(--volt) !important;
                background-color: var(--bg-panel) !important;
                border-bottom: 1px solid var(--volt) !important;
            }
            .stDataFrame td {
                border-bottom: 1px solid var(--border-dim) !important;
                color: var(--text-primary) !important;
                background-color: var(--bg-primary) !important;
            }
            .stDataFrame tr:hover td { background-color: rgba(173,255,47,0.03) !important; }

            [data-testid="stExpander"] {
                background-color: var(--bg-panel);
                border: 1px solid var(--border-dim);
                border-radius: 0;
            }
            [data-testid="stExpander"] summary {
                color: var(--volt) !important;
                font-family: 'Share Tech Mono', monospace;
                font-weight: bold;
                background-color: rgba(173,255,47,0.05);
            }
            [data-testid="stExpander"] summary:hover {
                color: var(--magenta) !important;
                background-color: rgba(255,0,122,0.05);
            }
            [data-testid="stExpander"] svg {
                fill: var(--text-primary) !important;
            }

            .status-header {
                display: flex; justify-content: space-between; align-items: center;
                border-bottom: 1px solid var(--border-dim); padding-bottom: 1rem; margin-bottom: 2rem;
            }
            .blinking-dot {
                width: 10px; height: 10px; background-color: var(--volt); border-radius: 50%;
                animation: blink 1s infinite; box-shadow: 0 0 10px var(--volt);
            }
            @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }

            [data-testid="stMetricValue"] {
                font-family: 'Share Tech Mono', monospace;
                color: var(--volt);
                font-size: 2rem;
            }
            [data-testid="stMetricLabel"] {
                font-family: 'Orbitron', sans-serif;
                color: var(--text-muted);
            }

            .stTabs [data-baseweb="tab-panel"] {
                padding: 0 !important;
                margin: 0 !important;
                border: none !important;
                background: transparent !important;
            }

            .block-container {
                padding-top: 1rem !important;
            }
        </style>
    """, unsafe_allow_html=True)

def inject_js():
    components.html("""
        <script>
            const targetNode = window.parent.document.body;
            const config = { childList: true, subtree: true };
            const callback = function(mutationsList, observer) {
                const buttons = window.parent.document.querySelectorAll('.stButton button, .stDownloadButton button, .stFormSubmitButton button');
                buttons.forEach(btn => {
                    if (!btn.hasAttribute('data-augmented-ui')) {
                        btn.setAttribute('data-augmented-ui', 'tl-clip br-clip both');
                        btn.style.setProperty('--aug-tl', '8px');
                        btn.style.setProperty('--aug-br', '8px');
                        btn.style.setProperty('--aug-border-all', '1px');
                        btn.style.fontFamily = "'Share Tech Mono', monospace";
                        btn.style.textTransform = "uppercase";
                        btn.style.fontWeight = "bold";
                        btn.style.transition = "all 0.3s";
                        
                        const text = btn.innerText.toUpperCase();
                        if (text.includes('RUN SIMULATION') || text.includes('NEXT') || text.includes('PREVIOUS') || text.includes('RETAKE') || text.includes('SUBMIT')) {
                            btn.style.setProperty('--aug-border-bg', '#ADFF2F');
                            btn.style.backgroundColor = '#ADFF2F';
                            btn.style.color = '#05050A';
                            btn.onmouseover = () => { btn.style.boxShadow = '0 0 20px rgba(173,255,47,0.6)'; };
                            btn.onmouseout = () => { btn.style.boxShadow = 'none'; };
                        } else {
                            btn.style.setProperty('--aug-border-bg', '#1E1E2F');
                            btn.style.backgroundColor = 'transparent';
                            btn.style.color = '#e8e8f0';
                            btn.onmouseover = () => { 
                                btn.style.setProperty('--aug-border-bg', '#ADFF2F');
                                btn.style.boxShadow = '0 0 15px rgba(173,255,47,0.3)';
                            };
                            btn.onmouseout = () => { 
                                btn.style.setProperty('--aug-border-bg', '#1E1E2F');
                                btn.style.boxShadow = 'none';
                            };
                        }
                    }
                });
            };
            const observer = new MutationObserver(callback);
            observer.observe(targetNode, config);
        </script>
    """, height=0)

def cyber_card(content, accent="volt", title=None):
    colors = {
        "volt": "#ADFF2F",
        "purple": "#9D4EDD",
        "magenta": "#FF007A"
    }
    color = colors.get(accent, "#1E1E2F")
    title_html = f'<h3 style="color: {color}; margin-bottom: 10px; font-family: \'Orbitron\', sans-serif;">{title}</h3>' if title else ''
    html = f"""
    <div data-augmented-ui="tl-clip br-clip both" style="
        --aug-tl: 12px; --aug-br: 12px; --aug-border-all: 1px; --aug-border-bg: {color};
        background-color: #0d0d1a; padding: 1.5rem; margin-bottom: 1.5rem; color: #e8e8f0;
    ">
        {title_html}
        {content}
    </div>
    """
    return html

@st.cache_data
def get_sample_data():
    np.random.seed(42)
    data = {
        'Age': np.random.normal(30, 10, 100),
        'Income': np.random.normal(50000, 15000, 100),
        'Engagement_Score': np.random.uniform(0, 100, 100),
        'Region': np.random.choice(['North America', 'Europe', 'Asia', 'South America'], 100)
    }
    df = pd.DataFrame(data)
    df.loc[5:15, 'Age'] = np.nan
    df.loc[25:35, 'Income'] = np.nan
    df.loc[45:50, 'Region'] = np.nan
    df = pd.concat([df, df.iloc[0:5]], ignore_index=True)
    df.loc[0, 'Income'] = 250000
    df.loc[1, 'Income'] = -50000
    return df

# ── SHARED ALTAIR CONFIG HELPER ──────────────────────────────────────────────
# Call this on the FINAL chart (after any + or & combining), never on sub-charts
def apply_chart_config(chart):
    return (
        chart
        .configure(background='transparent')
        .configure_axis(
            gridColor='#1E1E2F',
            domainColor='#1E1E2F',
            labelColor='#e8e8f0',
            titleColor='#e8e8f0',
            labelFont='Share Tech Mono',
            titleFont='Orbitron'
        )
        .configure_legend(
            labelColor='#e8e8f0',
            titleColor='#e8e8f0',
            labelFont='Share Tech Mono',
            titleFont='Orbitron'
        )
        .configure_view(strokeWidth=0)
    )

def render_data_playground():
    st.markdown(cyber_card(
        '<p style="color: #6b6b8a; font-family: \'Share Tech Mono\', monospace;">Upload, explore, and manipulate your datasets in real-time.</p>',
        title="Data Playground"
    ), unsafe_allow_html=True)

    with st.expander("⚡ SYSTEM BRIEFING: WHAT IS THIS SIMULATION?"):
        st.markdown("""<div style="font-family: 'Rajdhani', sans-serif; color: #e8e8f0; line-height: 1.6; padding: 10px;">
<h4 style="color: #ADFF2F; font-family: 'Orbitron', sans-serif; letter-spacing: 1px; font-size: 1.1rem; margin-top: 0;">🎯 1. Simulation Objective</h4>
<p style="margin-bottom: 20px;">This simulation demonstrates how Exploratory Data Analysis works on messy datasets.</p>

<h4 style="color: #9D4EDD; font-family: 'Orbitron', sans-serif; letter-spacing: 1px; font-size: 1.1rem;">⚙️ 2. What Happens Here?</h4>
<ul style="padding-left: 20px; font-family: 'Share Tech Mono', monospace; color: #6b6b8a; margin-bottom: 20px;">
    <li><span style="color: #e8e8f0;">Missing values handling</span> (Mean/Median/Drop)</li>
    <li><span style="color: #e8e8f0;">Duplicate removal</span></li>
    <li><span style="color: #e8e8f0;">Outlier adjustment</span> via Z-score clipping</li>
    <li><span style="color: #e8e8f0;">Visualization updates</span> in real-time</li>
</ul>

<h4 style="color: #FF007A; font-family: 'Orbitron', sans-serif; letter-spacing: 1px; font-size: 1.1rem;">📊 3. What Should Users Observe?</h4>
<ul style="padding-left: 20px; font-family: 'Share Tech Mono', monospace; color: #6b6b8a; margin-bottom: 20px;">
    <li><span style="color: #e8e8f0;">Histogram changes</span> as data is cleaned</li>
    <li><span style="color: #e8e8f0;">Distribution shifts</span> and tightened spreads</li>
    <li><span style="color: #e8e8f0;">Outlier effects</span> vanishing from the boxplot</li>
</ul>

<h4 style="color: #ADFF2F; font-family: 'Orbitron', sans-serif; letter-spacing: 1px; font-size: 1.1rem;">🎓 4. Learning Outcome</h4>
<p style="margin-bottom: 0;">Students learn how raw, unpredictable data becomes clean, reliable, and analysis-ready.</p>
</div>""", unsafe_allow_html=True)

    if 'raw_df' not in st.session_state:
        st.session_state.raw_df = get_sample_data()
    if 'processed_df' not in st.session_state:
        st.session_state.processed_df = None

    df = st.session_state.raw_df

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(cyber_card(
            '<p style="color: #6b6b8a; font-family: \'Share Tech Mono\', monospace;">Configure data sources and parameters.</p>',
            title="Control Panel"
        ), unsafe_allow_html=True)
        st.selectbox("Select Dataset", ["Sample Dataset: User Analytics"])
        st.markdown("<br>", unsafe_allow_html=True)
        missing_val_opt = st.selectbox("Missing Values Handling", ["Mean", "Median", "Drop Rows"])
        outlier_threshold = st.slider("Outlier Threshold (Z-score)", 1.0, 5.0, 3.0, 0.1)
        remove_duplicates = st.toggle("Remove Duplicates", value=True)
        st.markdown("<br>", unsafe_allow_html=True)
        run_sim = st.button("RUN SIMULATION", use_container_width=True)

    with col2:
        st.markdown(cyber_card(
            '<p style="color: #6b6b8a; font-family: \'Share Tech Mono\', monospace;">Inspect your dataset before transformation.</p>',
            title="Data Preview (Raw)"
        ), unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, height=270)

    if run_sim:
        with st.spinner("Processing Data..."):
            time.sleep(1)
            proc_df = df.copy()
            if remove_duplicates:
                proc_df = proc_df.drop_duplicates()
            if missing_val_opt == "Drop Rows":
                proc_df = proc_df.dropna()
            else:
                for c in proc_df.select_dtypes(include=np.number).columns:
                    if missing_val_opt == "Mean":
                        proc_df[c] = proc_df[c].fillna(proc_df[c].mean())
                    elif missing_val_opt == "Median":
                        proc_df[c] = proc_df[c].fillna(proc_df[c].median())
            for c in proc_df.select_dtypes(include=np.number).columns:
                mean = proc_df[c].mean()
                std = proc_df[c].std()
                proc_df[c] = np.clip(proc_df[c], mean - outlier_threshold * std, mean + outlier_threshold * std)
            st.session_state.processed_df = proc_df

    if st.session_state.processed_df is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        res_col1, res_col2 = st.columns([1, 1])

        with res_col1:
            st.markdown(cyber_card('', accent="purple", title="Cleaned Dataset"), unsafe_allow_html=True)
            st.dataframe(st.session_state.processed_df, use_container_width=True, height=250)

        with res_col2:
            st.markdown(cyber_card('', accent="purple", title="Data Distribution (Income)"), unsafe_allow_html=True)
            chart_df = st.session_state.processed_df.copy()

            # ✅ FIX: No background='transparent' in .properties() on sub-charts.
            # Define each chart cleanly, then combine, then configure once.
            hist = (
                alt.Chart(chart_df)
                .mark_bar(color='#9D4EDD')
                .encode(
                    alt.X("Income:Q", bin=alt.Bin(maxbins=20), title="Income"),
                    alt.Y('count():Q', title="Count")
                )
                .properties(height=200)          # ← no background here
            )

            box = (
                alt.Chart(chart_df)
                .mark_boxplot(
                    extent='min-max',
                    color='#9D4EDD',
                    outliers=alt.MarkConfig(color='#FF007A')
                )
                .encode(
                    x=alt.X('Income:Q', title="Income Distribution")
                )
                .properties(height=100)          # ← no background here
            )

            # Combine with & (vconcat), then apply config once
            combined = hist & box
            st.altair_chart(apply_chart_config(combined), use_container_width=True)


def render_data_insights():
    st.markdown(cyber_card(
        '<p style="color: #6b6b8a; font-family: \'Share Tech Mono\', monospace;">Automated analytics, correlations, and statistical summaries.</p>',
        title="Data Insights",
        accent="purple"
    ), unsafe_allow_html=True)

    if 'processed_df' not in st.session_state or st.session_state.processed_df is None:
        if 'raw_df' in st.session_state:
            df = st.session_state.raw_df
        else:
            st.warning("Please go to the Data Playground and process or load data first.")
            return
    else:
        df = st.session_state.processed_df

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if len(numeric_cols) < 2:
        st.warning("Not enough numeric columns for full insights.")
        return

    corr_matrix = df[numeric_cols].corr()

    # Find max correlation pair
    max_corr = 0
    top_corr_pair = ("None", "None")
    for i in range(len(numeric_cols)):
        for j in range(i + 1, len(numeric_cols)):
            c = abs(corr_matrix.iloc[i, j])
            if c > max_corr:
                max_corr = c
                top_corr_pair = (numeric_cols[i], numeric_cols[j])

    corr_status = (
        "STRONG RELATIONSHIP" if max_corr > 0.7
        else "MODERATE RELATIONSHIP" if max_corr > 0.3
        else "WEAK RELATIONSHIP"
    )

    # Outlier detection
    outlier_col = "NONE"
    has_outliers = "NO"
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
        if not outliers.empty:
            has_outliers = "YES"
            outlier_col = col
            break

    skew_val = df[numeric_cols[0]].skew()
    skew_status = (
        "RIGHT-SKEWED" if skew_val > 0.5
        else "LEFT-SKEWED" if skew_val < -0.5
        else "SYMMETRIC"
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(cyber_card(
            '<p style="color:#6b6b8a; font-family: \'Share Tech Mono\';">How numeric features relate to each other.</p>',
            title="Correlation Heatmap",
            accent="purple"
        ), unsafe_allow_html=True)

        corr_df = corr_matrix.reset_index().melt(id_vars='index')
        corr_df.columns = ['var1', 'var2', 'correlation']

        # ✅ FIX: No background='transparent' in .properties() on either sub-chart.
        # Build heatmap and text layer cleanly, then layer with +, then configure once.
        heatmap = (
            alt.Chart(corr_df)
            .mark_rect()
            .encode(
                x=alt.X('var1:O', title='', axis=alt.Axis(labelAngle=-45)),
                y=alt.Y('var2:O', title=''),
                color=alt.Color(
                    'correlation:Q',
                    scale=alt.Scale(scheme='purples'),
                    legend=alt.Legend(title="Correlation")
                ),
                tooltip=['var1', 'var2', 'correlation']
            )
            .properties(height=350)              # ← no background here
        )

        text = (
            heatmap
            .mark_text(baseline='middle')
            .encode(
                text=alt.Text('correlation:Q', format='.2f'),
                color=alt.condition(
                    abs(alt.datum.correlation) > 0.5,
                    alt.value('white'),
                    alt.value('black')
                )
            )
        )

        # Layer first, configure once
        st.altair_chart(apply_chart_config(heatmap + text), use_container_width=True)

    with col2:
        insight_content = f"""<div style="font-family: 'Share Tech Mono', monospace; font-size: 1.1rem; color: #ADFF2F; margin-bottom: 1.5rem; border-left: 3px solid #ADFF2F; padding-left: 10px;">
CORRELATION: {max_corr:.2f}<br>
<span style="color:#6b6b8a; font-size:0.9rem;">({top_corr_pair[0]} & {top_corr_pair[1]})</span><br>
STATUS: {corr_status}
</div>
<div style="font-family: 'Share Tech Mono', monospace; font-size: 1.1rem; color: #FF007A; margin-bottom: 1.5rem; border-left: 3px solid #FF007A; padding-left: 10px;">
OUTLIERS DETECTED: {has_outliers}<br>
<span style="color:#6b6b8a; font-size:0.9rem;">AFFECTED COLUMN: {outlier_col}</span>
</div>
<div style="font-family: 'Share Tech Mono', monospace; font-size: 1.1rem; color: #9D4EDD; border-left: 3px solid #9D4EDD; padding-left: 10px;">
DISTRIBUTION ({numeric_cols[0]}):<br>
STATUS: {skew_status}
</div>"""
        st.markdown(cyber_card(insight_content, title="Auto Insights", accent="volt"), unsafe_allow_html=True)


def render_how_it_works():
    st.markdown(cyber_card(
        '<p style="color: #6b6b8a; font-family: \'Share Tech Mono\', monospace;">A step-by-step interactive guide to Exploratory Data Analysis.</p>',
        title="How It Works (EDA Tutorial)"
    ), unsafe_allow_html=True)

    if 'eda_step' not in st.session_state:
        st.session_state.eda_step = 0

    steps = [
        {
            "title": "1. Load Data",
            "code": "import pandas as pd\n\ndf = pd.read_csv('data.csv')",
            "explanation": "Before analyzing data, we must load it into memory. pandas.read_csv() reads the file and creates a DataFrame — a table-like structure with rows and columns.",
            "tip": "Always check if your file path is correct!"
        },
        {
            "title": "2. View Data",
            "code": "> df.head()\n\n   Age  Income\n0 30.2   50000\n1 28.5   45000",
            "explanation": "df.head() shows the first 5 rows of the dataset. It's the quickest way to understand your data's structure, column names, and value types.",
            "tip": "Use df.tail() to see the last few rows!"
        },
        {
            "title": "3. Check Missing",
            "code": "> df.isnull().sum()\n\nAge         10\nIncome       8\nRegion       5\ndtype: int64",
            "explanation": "Real-world data is rarely perfect. isnull().sum() counts missing (NaN) values per column so you know exactly where the gaps are.",
            "tip": "Missing values can bias your analysis if not handled."
        },
        {
            "title": "4. Clean Data",
            "code": "df.fillna(df.mean(), inplace=True)\ndf.drop_duplicates(inplace=True)",
            "explanation": "Once we identify issues, we fix them. fillna() replaces missing values and drop_duplicates() removes repeated rows to keep the data clean and reliable.",
            "tip": "Don't drop too many rows — you may lose important signal!"
        },
        {
            "title": "5. Analyze Data",
            "code": "> df.describe()\n\n         Age      Income\nmean   30.25   50123.4\nstd     9.87   14983.2\nmin    10.00   -50000.0\nmax    65.00  250000.0",
            "explanation": "df.describe() generates a statistical summary — count, mean, std, min, max — for all numeric columns. Great for spotting oddities at a glance.",
            "tip": "Look for very high max values — they're likely outliers."
        },
        {
            "title": "6. Visualize Data",
            "code": "> df.corr()\n\n          Age  Income\nAge      1.00    0.72\nIncome   0.72    1.00",
            "explanation": "The correlation matrix shows how strongly pairs of features relate. Values close to 1 or -1 indicate strong relationships worth investigating further.",
            "tip": "Correlation near 1 is strong positive — near -1 is strong negative!"
        }
    ]

    col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
    with col_nav1:
        if st.button("⬅️ PREVIOUS", use_container_width=True, disabled=(st.session_state.eda_step == 0)):
            st.session_state.eda_step -= 1
            st.rerun()
    with col_nav2:
        st.markdown(
            f"<div style='text-align:center; color:#6b6b8a; font-family:\"Share Tech Mono\"; padding-top: 10px;'>"
            f"Step {st.session_state.eda_step + 1} of {len(steps)}: "
            f"<b style='color:#ADFF2F;'>{steps[st.session_state.eda_step]['title']}</b></div>",
            unsafe_allow_html=True
        )
    with col_nav3:
        if st.button("NEXT ➡️", use_container_width=True, disabled=(st.session_state.eda_step == len(steps) - 1)):
            st.session_state.eda_step += 1
            st.rerun()

    curr_step = steps[st.session_state.eda_step]

    left_col, right_col = st.columns([1.2, 1])
    with left_col:
        code_html = f"""
        <div data-augmented-ui="tl-clip br-clip both" style="--aug-tl: 12px; --aug-br: 12px; --aug-border-all: 1px; --aug-border-bg: #1E1E2F; background-color: #05050A; padding: 20px; height: 350px;">
            <div style="color: #9D4EDD; font-size: 0.8rem; margin-bottom: 15px; font-family: 'Share Tech Mono', monospace; text-transform: uppercase;">// Terminal View</div>
            <pre style="color: #ADFF2F; font-family: 'Share Tech Mono', monospace; font-size: 1.1rem; text-shadow: 0 0 5px rgba(173, 255, 47, 0.2); white-space: pre-wrap; background: transparent; border: none; overflow-x: auto;">{curr_step['code']}</pre>
        </div>
        """
        st.markdown(code_html, unsafe_allow_html=True)
    with right_col:
        expl_html = f"""
        <div data-augmented-ui="tl-clip br-clip both" style="--aug-tl: 12px; --aug-br: 12px; --aug-border-all: 1px; --aug-border-bg: #ADFF2F; background-color: #0d0d1a; padding: 25px; height: 350px; display: flex; flex-direction: column; justify-content: center;">
            <h3 style="color: #FFFFFF; font-family: 'Orbitron', sans-serif;">{curr_step['title']}</h3>
            <p style="color: #e8e8f0; font-size: 1.1rem; font-family: 'Rajdhani', sans-serif;">{curr_step['explanation']}</p>
            <div style="margin-top: 25px; padding: 15px; border-left: 3px solid #FF007A; background-color: rgba(255, 0, 122, 0.05);">
                <span style="color: #6b6b8a; font-family: 'Share Tech Mono', monospace; font-size: 0.95rem;">{curr_step['tip']}</span>
            </div>
        </div>
        """
        st.markdown(expl_html, unsafe_allow_html=True)


def render_easy_explanation():
    st.markdown(cyber_card(
        '<p style="color: #6b6b8a; font-family: \'Share Tech Mono\', monospace;">Learn concepts in simple English & Hinglish</p>',
        title="Easy Explanation",
        accent="volt"
    ), unsafe_allow_html=True)

    lang = st.radio("Select Language", ["English", "Hinglish"], horizontal=True)


    if lang == "English":
        main_exp = """<div style="background-color:#0d0d1a; border:1px solid #1E1E2F; padding:25px; color:white; font-family:'Rajdhani', sans-serif; line-height:1.8;">
<b style="color:#ADFF2F; font-size:1.3rem;">
Think of EDA like cleaning and organizing your room before a big study session.
</b>
<br><br>
You wouldn't just sit down in a messy room and expect to study well, right?
<br><br>
<ul style="padding-left:20px;">
<li style="margin-bottom:12px;">
<b style="color:#9D4EDD;">1. Look at data:</b> Like scanning your room to see what books you have.
</li>
<li style="margin-bottom:12px;">
<b style="color:#9D4EDD;">2. Clean data:</b> Throwing away old notes and useless garbage.
</li>
<li style="margin-bottom:12px;">
<b style="color:#9D4EDD;">3. Understand patterns:</b> Realizing you study better when math books are together.
</li>
<li style="margin-bottom:12px;">
<b style="color:#FF007A;">4. Detect outliers:</b> Finding a toy hidden under your desk and removing it.
</li>
</ul>
</div>"""

    else:
        main_exp = """<div style="background-color:#0d0d1a; border:1px solid #1E1E2F; padding:25px; color:white; font-family:'Rajdhani', sans-serif; line-height:1.8;">
<b style="color:#ADFF2F; font-size:1.3rem;">
EDA ko aise samjho jaise exam se pehle apna messy room clean aur organize karna.
</b>
<br><br>
Tum ek bikhre hue room mein thik se padhai nahi kar sakte, right?
<br><br>
<ul style="padding-left:20px;">
<li style="margin-bottom:12px;">
<b style="color:#9D4EDD;">1. Look at data:</b> Jaise room mein dekhna ki kaunsi books kahan rakhi hain.
</li>
<li style="margin-bottom:12px;">
<b style="color:#9D4EDD;">2. Clean data:</b> Faltu purane notes aur kachra bahar phekna.
</li>
<li style="margin-bottom:12px;">
<b style="color:#9D4EDD;">3. Understand patterns:</b> Ye samajhna ki maths ki books ek sath rakhne se padhna easy hota hai.
</li>
<li style="margin-bottom:12px;">
<b style="color:#FF007A;">4. Detect outliers:</b> Desk ke neeche se chote bhai ka khilona mil jana.
</li>
</ul>
</div>"""

    st.markdown(cyber_card(main_exp, title="Analogy", accent="purple"), unsafe_allow_html=True)


def render_quiz_arena():
    st.markdown(cyber_card(
        '<p style="color: #6b6b8a; font-family: \'Share Tech Mono\', monospace;">Test your knowledge and track your progress.</p>',
        title="Quiz Arena",
        accent="magenta"
    ), unsafe_allow_html=True)

    questions = [
        {
            "q": "Which plot is best for detecting outliers?",
            "options": ["Histogram", "Boxplot", "Pie chart", "Line chart"],
            "correct": 1,
            "explanation": "Boxplots show the spread and extreme values clearly, making outliers easy to spot."
        },
        {
            "q": "What does EDA mainly help with?",
            "options": ["Writing code", "Understanding data", "Building hardware", "Networking"],
            "correct": 1,
            "explanation": "EDA is about understanding patterns and structure in data before building models."
        },
        {
            "q": "What does isnull().sum() return?",
            "options": ["Row count", "Missing value count per column", "Duplicate count", "Column data types"],
            "correct": 1,
            "explanation": "isnull() creates a boolean mask; .sum() counts True (missing) values per column."
        },
        {
            "q": "A correlation value of 0.95 means:",
            "options": ["Weak relationship", "No relationship", "Strong positive relationship", "Strong negative relationship"],
            "correct": 2,
            "explanation": "Values close to +1 indicate a strong positive correlation between two features."
        },
        {
            "q": "Which method fills missing numeric values with the column average?",
            "options": ["fillna(median)", "dropna()", "fillna(mean())", "interpolate()"],
            "correct": 2,
            "explanation": "fillna(mean()) replaces NaN values with the arithmetic mean of that column."
        }
    ]

    if 'quiz_index' not in st.session_state:
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_streak = 0
        st.session_state.quiz_answered = False
        st.session_state.quiz_selected_option = None

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(
            f'<div style="font-family: \'Share Tech Mono\', monospace; color: #FFFFFF; font-size: 1.2rem;">'
            f'Score: <span style="color: #ADFF2F;">{st.session_state.quiz_score} / {len(questions)}</span></div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f'<div style="font-family: \'Share Tech Mono\', monospace; color: #FFFFFF; font-size: 1.2rem; text-align: right;">'
            f'🔥 STREAK: <span style="color: #FF007A;">{st.session_state.quiz_streak}</span></div>',
            unsafe_allow_html=True
        )

    if st.session_state.quiz_index >= len(questions):
        final_pct = int((st.session_state.quiz_score / len(questions)) * 100)
        if final_pct == 100:
            grade_msg = "🏆 PERFECT SCORE — EDA MASTER!"
        elif final_pct >= 80:
            grade_msg = "⚡ EXCELLENT WORK!"
        elif final_pct >= 60:
            grade_msg = "✅ SOLID UNDERSTANDING. KEEP GOING!"
        else:
            grade_msg = "📖 REVIEW THE BASICS AND RETRY."

        st.markdown(cyber_card(
            f'<h1 style="font-size: 4rem; color: #ADFF2F; text-align: center;">{st.session_state.quiz_score} / {len(questions)}</h1>'
            f'<p style="text-align:center; font-family:\'Share Tech Mono\'; color:#e8e8f0;">{grade_msg}</p>',
            title="Quiz Completed!"
        ), unsafe_allow_html=True)

        if st.button("RETAKE QUIZ", use_container_width=True):
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_streak = 0
            st.session_state.quiz_answered = False
            st.session_state.quiz_selected_option = None
            st.rerun()
        return

    q_data = questions[st.session_state.quiz_index]

    # Progress bar
    progress_pct = int((st.session_state.quiz_index / len(questions)) * 100)
    st.markdown(
        f'<div style="height:3px; background:#1E1E2F; margin-bottom:16px;">'
        f'<div style="height:3px; width:{progress_pct}%; background:#ADFF2F; box-shadow: 0 0 8px rgba(173,255,47,0.5);"></div>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(cyber_card(
        f'<p style="font-size: 1.2rem; color: #FFFFFF; font-family: \'Rajdhani\', sans-serif;">{q_data["q"]}</p>',
        title=f"Question {st.session_state.quiz_index + 1} of {len(questions)}",
        accent="purple"
    ), unsafe_allow_html=True)

    if not st.session_state.quiz_answered:
        opt = st.radio("Select an answer:", q_data['options'], index=None, label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("SUBMIT ANSWER", disabled=(opt is None), use_container_width=True):
            st.session_state.quiz_selected_option = q_data['options'].index(opt)
            st.session_state.quiz_answered = True
            if st.session_state.quiz_selected_option == q_data['correct']:
                st.session_state.quiz_score += 1
                st.session_state.quiz_streak += 1
            else:
                st.session_state.quiz_streak = 0
            st.rerun()
    else:
        selected = st.session_state.quiz_selected_option
        correct = q_data['correct']

        for i, option_text in enumerate(q_data['options']):
            if i == correct:
                st.markdown(
                    f'<div style="background-color: rgba(173,255,47,0.1); border: 1px solid #ADFF2F; padding: 15px; margin-bottom: 10px; color: #ADFF2F; font-family: \'Share Tech Mono\';">✅ {option_text}</div>',
                    unsafe_allow_html=True
                )
            elif i == selected and selected != correct:
                st.markdown(
                    f'<div style="background-color: rgba(255,0,122,0.1); border: 1px solid #FF007A; padding: 15px; margin-bottom: 10px; color: #FF007A; font-family: \'Share Tech Mono\';">❌ {option_text}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div style="border: 1px solid #1E1E2F; padding: 15px; margin-bottom: 10px; color: #6b6b8a; font-family: \'Share Tech Mono\';">⬜ {option_text}</div>',
                    unsafe_allow_html=True
                )

        result_color = "#ADFF2F" if selected == correct else "#FF007A"
        result_label = "✓ CORRECT" if selected == correct else "✗ INCORRECT"
        st.markdown(
            f'<div style="margin-top: 20px; padding: 14px; border-left: 3px solid {result_color}; background: rgba(0,0,0,0.3);">'
            f'<span style="color:{result_color}; font-family:\'Share Tech Mono\'; font-size:0.9rem;">{result_label}</span><br>'
            f'<span style="color:#e8e8f0; font-family:\'Rajdhani\'; font-size:1rem;">{q_data["explanation"]}</span>'
            f'</div><br>',
            unsafe_allow_html=True
        )

        if st.button("NEXT QUESTION ➡️", use_container_width=True):
            st.session_state.quiz_index += 1
            st.session_state.quiz_answered = False
            st.session_state.quiz_selected_option = None
            st.rerun()


def main():
    load_css()

    st.markdown("""
        <div class="status-header">
            <div class="status-left">
                <h1 style="margin: 0; color: #FFFFFF; letter-spacing: 2px;">EXPLORA<span style="color: #ADFF2F;">AI</span></h1>
                <div data-augmented-ui="tl-clip br-clip both" style="--aug-tl: 4px; --aug-br: 4px; --aug-border-all: 1px; --aug-border-bg: #ADFF2F; background: rgba(173,255,47,0.1); padding: 4px 10px; font-family: 'Share Tech Mono'; font-size: 0.8rem; color: #ADFF2F; display: flex; align-items: center; gap: 8px;">
                    <div class="blinking-dot"></div> SYSTEM ONLINE
                </div>
            </div>
            <div class="status-right">
                <span style="font-family: 'Share Tech Mono'; color: #6b6b8a; font-size: 0.9rem;">v2.0_CYBER</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    t_playground, t_insights, t_how_it_works, t_easy_exp, t_quiz = st.tabs([
        "01 / Data Playground",
        "02 / Data Insights",
        "03 / How It Works",
        "04 / Easy Explanation",
        "05 / Quiz Arena"
    ])

    with t_playground: render_data_playground()
    with t_insights: render_data_insights()
    with t_how_it_works: render_how_it_works()
    with t_easy_exp: render_easy_explanation()
    with t_quiz: render_quiz_arena()

    inject_js()


if __name__ == "__main__":
    main()