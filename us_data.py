import streamlit as st
import plotly.graph_objects as go
from data_loader import fetch_data_by_frequency
from data_transformer import transform_quarterly_data, transform_monthly_data,transform_weekly_data
from charts import plot_quarterly_line_chart, plot_monthly_line_chart, plot_weekly_line_chart
from utils import get_yaxis_label
import plotly.express as px 
import pandas as pd
import matplotlib.pyplot as plt
import textwrap

import matplotlib as mpl
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.size'] = 12


st.set_page_config(
    page_title="US Economic Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("US Economic Outlook")

# --- Load and Transform Data ---
@st.cache_data
def load_data():
    df_quarterly, df_monthly, df_weekly = fetch_data_by_frequency()
    df_quarterly = transform_quarterly_data(df_quarterly)
    df_monthly = transform_monthly_data(df_monthly)

    # If you have a transform function for weekly data, use it here; else keep None
    # df_weekly = transform_weekly_data(df_weekly)
    df_weekly = transform_weekly_data(df_weekly)  # <-- Set None if no weekly data available

    return df_quarterly, df_monthly, df_weekly

# --- Load into session state only if not already stored ---
if "df_quarterly" not in st.session_state or "df_monthly" not in st.session_state or "df_weekly" not in st.session_state:
    df_quarterly, df_monthly, df_weekly = load_data()
    st.session_state.df_quarterly = df_quarterly
    st.session_state.df_monthly = df_monthly
    st.session_state.df_weekly = df_weekly
else:
    df_quarterly = st.session_state.df_quarterly
    df_monthly = st.session_state.df_monthly
    df_weekly = st.session_state.df_weekly

def show_metric_with_change(df, column_name, label):
    data = df[[column_name]].dropna().sort_index()
    if len(data) < 2:
        return

    current = data.iloc[-1][column_name]
    previous = data.iloc[-2][column_name]

    inflation_keywords = ["inflation", "cpi", "pce", "deflator"]

    if any(key in column_name.lower() for key in inflation_keywords):
        # Show delta as absolute change
        delta_value = current - previous
        main_value = f"{delta_value:+,.2f}"
        delta_pct = ((current - previous) / previous) * 100 if previous != 0 else 0
        delta_text = f"{delta_pct:+.2f}%"
    else:
        # Show delta as percentage change, main value is the delta
        delta_pct = ((current - previous) / previous) * 100 if previous != 0 else 0
        main_value = f"{delta_pct:+.2f}%"
        delta_value = current - previous
        delta_text = f"{delta_value:+,.2f}"

    st.metric(
        label="",
        value=main_value,
        delta=delta_text,
        delta_color="normal"  # no color change, just plain
    )

# Tabs for sections
tabs = st.tabs(["Labor Market", "Monetary Metrics", "Fiscal Metrics", "Debtonomics", "Workforce Flows", "Custom Charts"])

# 1. Labor Market
with tabs[0]:
    st.subheader("Labor Market Trends")
    labor_vars = [
        "Unemployment Rate",
        "Labor Force Participation Rate",
        "Initial Claims",
        "Unemployment Level",
        "Job Openings Total Nonfarm"
    ]
    for var in labor_vars:
        if df_monthly is not None and var in df_monthly.columns:
            source_df = df_monthly
            chart_func = plot_monthly_line_chart
        elif df_weekly is not None and var in df_weekly.columns:
            source_df = df_weekly
            chart_func = plot_weekly_line_chart
        else:
            continue

        show_metric_with_change(source_df, var, var)
        fig = chart_func(source_df, [var], title=var, yaxis_title=get_yaxis_label(var))
        st.plotly_chart(fig, use_container_width=True)

# 2. Monetary Metrics
with tabs[1]:
    st.subheader("Monetary Indicators")
    monetary_vars = [
        "CPI YoY Inflation",
        "PCE YoY Inflation",
        "GDP Deflator",
        "University of Michigan: Inflation Expectation",
        "M1",
        "M2",
        "Federal Funds Effective Rate"
    ]
    for var in monetary_vars:
        source_df = df_monthly if var in df_monthly.columns else df_quarterly
        chart_func = plot_monthly_line_chart if source_df is df_monthly else plot_quarterly_line_chart
        if var in source_df.columns:
            show_metric_with_change(source_df, var, var)
            fig = chart_func(source_df, [var], title=var, yaxis_title=get_yaxis_label(var))
            st.plotly_chart(fig, use_container_width=True)

# 3. Fiscal Metrics
with tabs[2]:
    st.subheader("Fiscal Indicators")
    fiscal_vars = [
        "GDP",
        "Real GDP",
        "GDP Growth",
        "Exports",
        "Imports",
        "Net Exports"
    ]
    for var in fiscal_vars:
        if var in df_quarterly.columns:
            show_metric_with_change(df_quarterly, var, var)
            fig = plot_quarterly_line_chart(df_quarterly, [var], title=var, yaxis_title=get_yaxis_label(var))
            st.plotly_chart(fig, use_container_width=True)


# 4. Debtonomics
with tabs[3]:
    st.subheader("Federal Debt Breakdown")
    debt_vars = [
        "Federal Debt Total Public Debt",
        "Federal Debt Held by the Public",
        "Federal Debt Held by Federal Reserve Banks",
        "Federal Debt Held by Foreign and International Investors",
        "Federal Debt Held by Agencies and Trusts",
        "Federal Debt: Total Public Debt as Percent of GDP"
    ]
    for var in debt_vars:
        if var in df_quarterly.columns:
            show_metric_with_change(df_quarterly, var, var)
            fig = plot_quarterly_line_chart(df_quarterly, [var], title=var, yaxis_title=get_yaxis_label(var))
            st.plotly_chart(fig, use_container_width=True)

    # Federal Debt Stacked Area Chart
    exclude_col = "Federal Debt: Total Public Debt as Percent of GDP"
    debt_cols = [col for col in df_quarterly.columns if col.startswith("Federal Debt") and col != exclude_col]
    df_debt = df_quarterly[debt_cols].dropna()
    fig = go.Figure()
    for col in df_debt.columns:
        fig.add_trace(go.Scatter(
            x=df_debt.index,
            y=df_debt[col],
            mode='lines',
            name=col,
            stackgroup='one',
            line=dict(width=0.5),
            hoverinfo='x+y'
        ))
    fig.update_layout(
        title=dict(text="Federal Debt Components (Quarterly, Billions)", x=0.5),
        xaxis_title="Date",
        yaxis_title="USD (Billions)",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True, key="debt_stack_chart")

# 5. Workforce Flows
with tabs[4]:

    # Beveridge Curve
    if df_monthly is not None and 'Job Openings Total Nonfarm' in df_monthly.columns and 'Unemployment Rate' in df_monthly.columns:
        x = df_monthly['Unemployment Rate']
        y = df_monthly['Job Openings Total Nonfarm']
        years = df_monthly.index.year.astype(str)

        fig_beveridge = px.scatter(
            x=x, y=y, color=years,
            labels={"x": "Unemployment Rate (%)", "y": "Job Openings (Thousands)"},
            title="Beveridge Curve: Unemployment vs Job Openings"
        )

        fig_beveridge.update_layout(
            title=dict(text="Beveridge Curve: Unemployment vs Job Openings", x=0.5, font=dict(size=16, family="Times New Roman")),
            font=dict(family="Times New Roman"),
            height=450,
            legend=dict(font=dict(size=10, family="Times New Roman"), orientation="v", yanchor="top", y=1.02, xanchor="left", x=0)
        )

        st.plotly_chart(fig_beveridge, use_container_width=True)
        
    # Vacancy-to-Unemployment Ratio Matplotlib
    if df_monthly is not None and 'Job Vacancy-to-Unemployment Ratio' in df_monthly.columns:
        dataset = df_monthly[['Job Vacancy-to-Unemployment Ratio']].dropna().reset_index()
        dataset.rename(columns={'index': 'Periods', 'Job Vacancy-to-Unemployment Ratio': 'vacancy_to_unemployment'}, inplace=True)
        dataset['Periods'] = pd.to_datetime(dataset['Periods'])
        dataset['rolling_avg'] = dataset['vacancy_to_unemployment'].rolling(window=4, min_periods=1).mean()

        plt.rc('font', family='Times New Roman')
        plt.rcParams.update({'font.family': 'Times New Roman'})
        fig, ax = plt.subplots(figsize=(12, 3.8))

        ax.plot(dataset['Periods'], dataset['vacancy_to_unemployment'], color='red', label='Vacancy to Unemployment Ratio', alpha=0.8)
        ax.plot(dataset['Periods'], dataset['rolling_avg'], color='darkred', linestyle='--', label='1-Year Moving Average', linewidth=2)

        ax.axvspan(pd.to_datetime('2020-03-01'), pd.to_datetime('2021-12-31'), color='gray', alpha=0.3, label='COVID-19 Period')

        last_period = dataset['Periods'].iloc[-1]
        last_ratio = dataset['vacancy_to_unemployment'].iloc[-1]
        last_rolling_avg = dataset['rolling_avg'].iloc[-1]
        ax.text(last_period, last_ratio, f'{last_ratio:.2f}', color='red', fontsize=10, ha='left', va='center')
        ax.text(last_period, last_rolling_avg, f'{last_rolling_avg:.2f}', color='darkred', fontsize=10, ha='left', va='center')

        max_ratio = dataset['vacancy_to_unemployment'].max()
        max_ratio_period = dataset.loc[dataset['vacancy_to_unemployment'].idxmax(), 'Periods']
        ax.text(max_ratio_period, max_ratio, f'{max_ratio:.2f}', color='red', fontsize=10, ha='left', va='bottom')
        ax.scatter(max_ratio_period, max_ratio, color='red', s=50, label='Peak of Vacancy to Unemployment ratio')

        ax.set_title("Jobseekers vs Job Vacancies", fontsize=11, fontweight='bold', pad=10)
        ax.axhline(y=1, color='black', linestyle='--', linewidth=1)

        mid_period = dataset['Periods'].iloc[len(dataset) // 2]
        ax.annotate('▲ More jobs than unemployed',
                    xy=(mid_period, 1), xytext=(mid_period, 1.05),
                    fontsize=10, fontweight='bold', ha='center', color='black')
        ax.annotate('▼ Fewer jobs than unemployed',
                    xy=(mid_period, 1), xytext=(mid_period, 0.9),
                    fontsize=10, fontweight='bold', ha='center', color='black')

        ax.set_xticks(pd.date_range(start=dataset['Periods'].min(),
                                    end=dataset['Periods'].max(), freq='2YS'))
        ax.tick_params(axis='x', which='both', direction='out', bottom=True)

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.legend(loc='upper left', fontsize=10, frameon=True,edgecolor='black')
        ax.grid(False)
        fig.tight_layout(pad=1.5)

        st.pyplot(fig)

    # Your existing transition_columns dict here
    transition_columns = {
        'Monthly Transition Rate of All U.S. Workers From Employment to Non-Employment Due to a Layoff': 'EMELASA',
        'Monthly Transition Rate of Prime-Age U.S. Workers From Employment to Non-Employment Due to a Layoff': 'EMELPSA',
        'Monthly Transition Rate of All U.S. Workers From Employment to Non-Employment Due to a Quit': 'EMEQASA',
        'Monthly Transition Rate of Prime-Age U.S. Workers From Employment to Non-Employment Due to a Quit': 'EMEQPSA'
    }

    # Color and line style maps
    color_map = {
        'Layoff': 'red',
        'Quit': 'green'
    }
    line_style_map = {
        'Prime-Age': 'dash',
        'All': 'solid'
    }

    if df_monthly is not None:
        valid_cols = [label for label in transition_columns if label in df_monthly.columns]
        if valid_cols:
            df_transitions = df_monthly[valid_cols].dropna()

            fig_transitions = go.Figure()

            for col in valid_cols:
                # Determine label short form for legend
                label_short = col.split('Monthly Transition Rate of ')[-1]
                # Decide color & line style
                is_prime = 'Prime-Age' in label_short
                is_layoff = 'Layoff' in label_short

                color = color_map['Layoff'] if is_layoff else color_map['Quit']
                line_dash = line_style_map['Prime-Age'] if is_prime else line_style_map['All']

                fig_transitions.add_trace(go.Scatter(
                    x=df_transitions.index,
                    y=df_transitions[col],
                    mode='lines',
                    name=label_short,
                    line=dict(color=color, width=3, dash=line_dash)
                ))

            # Wrap title nicely
            wrapped_title = "<br>".join(textwrap.wrap(
                "Layoffs vs. Quits: The Push and Pull of the Labor Market", 70))

            # Create quarterly tickvals for x-axis to reduce clutter
            dates = pd.to_datetime(df_transitions.index)
            tickvals = [date for date in dates if date.month in [1, 7] and date.day == 1]
            ticktext = [date.strftime('%b %Y') for date in tickvals]




            fig_transitions.update_layout(
                title=dict(
                    text=wrapped_title,
                    x=0.35,
                    font=dict(size=16, family="Times New Roman")
                ),
                xaxis=dict(
                    title="Date",
                    showline=True,
                    linecolor='black',
                    tickvals=tickvals,
                    tickformat="%b %Y",
                    tickangle=45,
                    tickfont=dict(size=12, family="Times New Roman"),
                    showgrid=False
                ),
                yaxis=dict(
                    title="Transition Rate (%)",
                    showline=True,
                    linecolor='black',
                    showgrid=False,
                    gridcolor='lightgray',
                    zeroline=False
                ),
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Times New Roman", size=14),
                hovermode="x unified",
                height=500,
                width=900,  # wider figure for more room
                margin=dict(l=50, r=150, t=70, b=70),  # extra right margin for legend
                legend=dict(
                    font=dict(size=12),
                    orientation="v",
                    yanchor="top",
                    y=0.95,
                    xanchor="right",
                    x=0.38,
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='black',
                    borderwidth=1
                )
            )

            st.plotly_chart(fig_transitions, use_container_width=True)

    df_weekly_filtered = df_weekly[[
        'Continued Claims (Insured Unemployment)',
        '4-Week Moving Average of Continued Claims (Insured Unemployment)'
    ]].dropna()

    # Choose a transition series to overlay
    transition_key = 'Monthly Transition Rate of All U.S. Workers From Employment to Non-Employment Due to a Layoff'
    transition_series = df_monthly[[transition_key]].dropna()

    # Build the figure
    fig = go.Figure()

    # Plot continued claims
    fig.add_trace(go.Scatter(
        x=df_weekly_filtered.index,
        y=df_weekly_filtered['Continued Claims (Insured Unemployment)'],
        name='Continued Claims',
        line=dict(color='crimson', width=3),
        hovertemplate='%{x|%Y-%m-%d}<br>Claims: %{y:,.0f}<extra></extra>'
    ))

    # 4-week moving average
    fig.add_trace(go.Scatter(
        x=df_weekly_filtered.index,
        y=df_weekly_filtered['4-Week Moving Average of Continued Claims (Insured Unemployment)'],
        name='4-Week Moving Avg',
        line=dict(color='blue', dash='dash', width=3),
        hovertemplate='%{x|%Y-%m-%d}<br>4W Avg: %{y:,.0f}<extra></extra>'
    ))

    # Layoff transition rate
    fig.add_trace(go.Scatter(
        x=transition_series.index,
        y=transition_series[transition_key],
        name='Layoff Transition Rate',
        yaxis='y2',
        line=dict(color='darkgreen', width=2),
        hovertemplate='%{x|%Y-%m}<br>Rate: %{y:.2f}%<extra></extra>'
    ))

    # COVID annotation
    fig.add_vrect(
        x0="2020-03-01", x1="2020-05-01",
        fillcolor="gray", opacity=0.2,
        layer="below", line_width=0,
        annotation_text="COVID Layoff Spike", annotation_position="top left"
    )

    fig.update_layout(
        title=dict(
            text='Unemployment Continuity & Layoff Dynamics (Pandemic Impact)',
            x=0.5,
            xanchor='center',
            font=dict(size=20)
        ),
        xaxis=dict(
            title='Date',
            tickformat='%Y-%m',
            showgrid=False,
            showline=True,
            linecolor='black',
            mirror=False,     # No mirror so no top line
            ticks='outside',
            zeroline=False
        ),
        yaxis=dict(
            title='Unemployment Claims',
            showgrid=False,
            showline=True,
            linecolor='black',
            mirror=False,     # No mirror so no right line here
            ticks='outside',
            zeroline=False
        ),
        yaxis2=dict(
            title='Layoff Transition Rate (%)',
            overlaying='y',
            side='right',
            showgrid=False,
            showline=True,
            linecolor='black',
            mirror=False,     # no extra lines beyond right side
            ticks='outside',
            zeroline=False
        ),
        showlegend=True,
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='gray',
            borderwidth=1,
            yanchor="top",
            y=0.95,
            xanchor="left",
            x=0.01
        ),
        template='plotly_white',
        hovermode='x unified',
        height=550,
        margin=dict(l=40, r=60, t=80, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)


# 6. Custom Charts
with tabs[5]:
    st.subheader("Build Your Own Charts")
    freq = st.radio("Choose frequency:", ["Quarterly", "Monthly", "Weekly"], horizontal=True)

    if freq == "Quarterly":
        df = df_quarterly
        chart_func = plot_quarterly_line_chart
    elif freq == "Monthly":
        df = df_monthly
        chart_func = plot_monthly_line_chart
    else:  # Weekly
        df = df_weekly
        chart_func = plot_weekly_line_chart

    if df is not None:       
        missing_or_empty = [col for col in df.columns if df[col].isna().all()]
        if missing_or_empty:
            st.warning(f"The following variables have no data and won't plot: {missing_or_empty}")
        available_vars = [col for col in df.columns if not df[col].isna().all()]
        selected = st.multiselect("Select variables to plot:", options=available_vars)
        
        for var in selected:
            if var in df.columns:
                show_metric_with_change(df, var, var)  # Pass dataframe, not freq
                fig = chart_func(df, [var], title=var)
                fig.update_yaxes(title_text=get_yaxis_label(var))
                st.plotly_chart(fig, use_container_width=True, key=f"custom_{freq}_{var}")
            else:
                st.warning(f"Column '{var}' not found in the {freq} data.")
        # Get the relevant data



with st.sidebar:
    with st.expander("📂 Download & Manage Data", expanded=True):
        st.markdown("### Dataset Tools")

        monthly_df = st.session_state.get("df_monthly")
        quarterly_df = st.session_state.get("df_quarterly")
        weekly_df = st.session_state.get("df_weekly")

        # Monthly range
        if monthly_df is not None and not monthly_df.empty:
            monthly_range = f"{monthly_df.index.min().strftime('%b %Y')} → {monthly_df.index.max().strftime('%b %Y')}"
        else:
            monthly_range = "No monthly data available"

        # Quarterly range
        if quarterly_df is not None and not quarterly_df.empty:
            if quarterly_df.index.freqstr and 'Q' in quarterly_df.index.freqstr:
                quarterly_range = f"{quarterly_df.index.min().year} Q{quarterly_df.index.min().quarter} → {quarterly_df.index.max().year} Q{quarterly_df.index.max().quarter}"
            else:
                quarterly_range = f"{quarterly_df.index.min().strftime('%b %Y')} → {quarterly_df.index.max().strftime('%b %Y')}"
        else:
            quarterly_range = "No quarterly data available"

        # Weekly range
        if weekly_df is not None and not weekly_df.empty:
            weekly_range = f"{weekly_df.index.min().strftime('%d %b %Y')} → {weekly_df.index.max().strftime('%d %b %Y')}"
        else:
            weekly_range = "No weekly data available"

        st.caption(f"📅 Monthly data range: {monthly_range}")
        st.caption(f"📅 Quarterly data range: {quarterly_range}")
        st.caption(f"📅 Weekly data range: {weekly_range}")

        # Download buttons for all datasets
        if monthly_df is not None and not monthly_df.empty:
            csv_monthly = monthly_df.to_csv().encode('utf-8')
            st.download_button(
                label="⬇️ Download Monthly Data (CSV)",
                data=csv_monthly,
                file_name="monthly_data.csv",
                mime="text/csv"
            )
        if quarterly_df is not None and not quarterly_df.empty:
            csv_quarterly = quarterly_df.to_csv().encode('utf-8')
            st.download_button(
                label="⬇️ Download Quarterly Data (CSV)",
                data=csv_quarterly,
                file_name="quarterly_data.csv",
                mime="text/csv"
            )
        if weekly_df is not None and not weekly_df.empty:
            csv_weekly = weekly_df.to_csv().encode('utf-8')
            st.download_button(
                label="⬇️ Download Weekly Data (CSV)",
                data=csv_weekly,
                file_name="weekly_data.csv",
                mime="text/csv"
            )

    with st.expander("📣 We’re Listening!", expanded=False):
        st.markdown("### Feedback & Support")
        st.markdown("""
        That was me relinquishing my old good uni times — and uni is an agora of ideas, so let's share those.
        - 💡 Got an idea to improve the dashboard?
        - ❤️ Just wanna say hi? We like that too.
        """)
        st.write("Use the form below or [email us directly](mailto:georgios.tsatsoulis@outlook.com).")

        feedback_type = st.selectbox("Type", ["General Feedback", "Bug Report", "Request Data"])
        feedback_text = st.text_area("Your Message", placeholder="Let us know what you think...")

        if st.button("Send Feedback", key="send_feedback"):
            if feedback_text.strip():
                st.success("✅ Thanks for the feedback!")
                with open("feedback_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n---\nType: {feedback_type}\nMessage: {feedback_text}\n")
            else:
                st.error("❗ Please enter a message before submitting.")


