import plotly.graph_objects as go
from utils import get_yaxis_label



# Helper: Convert datetime index to quarterly format
def format_quarter(date):
    q = (date.month - 1) // 3 + 1
    return f"{date.year}Q{q}"

# Helper: Convert datetime index to monthly format
def format_month(date):
    return f"{date.year}M{date.month}"

def format_week(date):
    # ISO year and week number, e.g. '2025-W22'
    return f"{date.isocalendar().year}-W{date.isocalendar().week:02d}"


# Quarterly chart
def plot_quarterly_line_chart(df, columns, title="Quarterly Chart", yaxis_title="Value"):
    y_label = get_yaxis_label(columns[0])
    fig = go.Figure()
    df_formatted = df.copy()
    df_formatted.index = df_formatted.index.to_series().apply(format_quarter)

    for col in columns:
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df_formatted.index,
                y=df[col],
                mode='lines',
                name=col,
                line=dict(width=2)
            ))

    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=20)),
        xaxis=dict(
            title='Quarter',
            ticks='outside',
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black'
        ),
        yaxis=dict(
            title=yaxis_title,
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Times New Roman", size=14, color="#222"),
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig

# Monthly chart
def plot_monthly_line_chart(df, columns, title="Monthly Chart", yaxis_title="Value"):
    y_label = get_yaxis_label(columns[0])
    fig = go.Figure()
    df_formatted = df.copy()
    df_formatted.index = df_formatted.index.to_series().apply(format_month)

    for col in columns:
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df_formatted.index,
                y=df[col],
                mode='lines',
                name=col,
                line=dict(width=2)
            ))

    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=20)),
        xaxis=dict(
            title='Month',
            ticks='outside',
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black'
        ),
        yaxis=dict(
            title=yaxis_title,
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Times New Roman", size=14, color="#A84C4C"),
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig

# Monthly chart
def plot_weekly_line_chart(df, columns, title="Weekly_chart", yaxis_title="Value"):
    y_label = get_yaxis_label(columns[0])
    fig = go.Figure()
    df_formatted = df.copy()
    df_formatted.index = df_formatted.index.to_series().apply(format_week)

    for col in columns:
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df_formatted.index,
                y=df[col],
                mode='lines',
                name=col,
                line=dict(width=2)
            ))

    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=20)),
        xaxis=dict(
            title='Week',
            ticks='outside',
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black'
        ),
        yaxis=dict(
            title=y_label,
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Times New Roman", size=14, color="#A84C4C"),
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig