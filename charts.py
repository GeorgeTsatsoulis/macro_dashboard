import plotly.graph_objects as go
from utils import get_yaxis_label

# Helpers for formatting datetime index
def format_quarter(date):
    q = (date.month - 1) // 3 + 1
    return f"{date.year}Q{q}"

def format_month(date):
    return f"{date.year}M{date.month}"

def format_week(date):
    return f"{date.isocalendar().year}-W{date.isocalendar().week:02d}"


def _plot_time_series(df, columns, title, xaxis_title, yaxis_title, date_formatter):
    y_label = get_yaxis_label(columns[0])
    fig = go.Figure()
    df_formatted = df.copy()
    df_formatted.index = df_formatted.index.to_series().apply(date_formatter)

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
        title=dict(text=title, x=0.2, font=dict(size=20)),
        width=1000,
        xaxis=dict(
            title=xaxis_title,
            ticks='outside',
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black'
        ),
        yaxis=dict(
            title=yaxis_title or y_label,
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Times New Roman", size=14, color="#222"),
        hoverlabel=dict(font=dict(family="Times New Roman")),
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig

# Quarterly chart
def plot_quarterly_line_chart(df, columns, title="Quarterly Chart", yaxis_title="Value"):
    return _plot_time_series(df, columns, title, "Quarter", yaxis_title, format_quarter)

# Monthly chart
def plot_monthly_line_chart(df, columns, title="Monthly Chart", yaxis_title="Value"):
    return _plot_time_series(df, columns, title, "Month", yaxis_title, format_month)

# Weekly chart
def plot_weekly_line_chart(df, columns, title="Weekly Chart", yaxis_title="Value"):
    return _plot_time_series(df, columns, title, "Week", yaxis_title, format_week)
