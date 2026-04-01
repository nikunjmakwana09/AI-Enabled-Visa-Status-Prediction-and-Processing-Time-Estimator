import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from data.offices import OFFICE_DATA


# ==========================================================
# EMBASSY PROCESSING TIME VARIABILITY CHART
# ==========================================================

def processing_time_variability_chart(top_n=10):
    """
    Shows embassies with highest and lowest processing time variability (std deviation).
    """
    try:
        df = load_dataset()
        office_names = df['processing_office'].map(lambda code: OFFICE_DATA.get(code, {}).get('name', code))
        df = df.assign(Embassy=office_names)
        grouped = (
            df.groupby(['processing_office', 'Embassy'])['processing_time_days']
            .std()
            .reset_index()
            .rename(columns={'processing_time_days': 'StdDev'})
        )
        most_var = grouped.sort_values('StdDev', ascending=False).head(top_n)
        least_var = grouped.sort_values('StdDev', ascending=True).head(top_n)
    except Exception:
        most_var = pd.DataFrame({
            'Embassy': ['London', 'New York', 'Delhi', 'Mexico City', 'Sydney', 'Berlin', 'Singapore', 'Paris', 'Toronto', 'Dubai'],
            'StdDev': [80, 75, 70, 68, 65, 63, 60, 59, 58, 57]
        })
        least_var = pd.DataFrame({
            'Embassy': ['Oslo', 'Helsinki', 'Wellington', 'Lisbon', 'Dublin', 'Prague', 'Vienna', 'Brussels', 'Stockholm', 'Copenhagen'],
            'StdDev': [10, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        })

    fig_most = px.bar(
        most_var,
        x='StdDev',
        y='Embassy',
        orientation='h',
        title=f'Top {top_n} Most Variable Embassies',
        labels={'StdDev': 'Std Deviation (days)', 'Embassy': 'Embassy'},
        color='StdDev',
        color_continuous_scale='Magma'
    )
    fig_most.update_layout(
        template='plotly_dark',
        height=420,
        margin=dict(l=140, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Std Deviation (days)',
        yaxis_title='Embassy'
    )
    fig_most.update_traces(marker_line_color='white', marker_line_width=1)

    fig_least = px.bar(
        least_var,
        x='StdDev',
        y='Embassy',
        orientation='h',
        title=f'Top {top_n} Most Consistent Embassies',
        labels={'StdDev': 'Std Deviation (days)', 'Embassy': 'Embassy'},
        color='StdDev',
        color_continuous_scale='Greens'
    )
    fig_least.update_layout(
        template='plotly_dark',
        height=420,
        margin=dict(l=140, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Std Deviation (days)',
        yaxis_title='Embassy'
    )
    fig_least.update_traces(marker_line_color='white', marker_line_width=1)

    return fig_most, fig_least


# ==========================================================
# GLOBAL THEME SETTINGS
# ==========================================================

PRIMARY = "#38BDF8"
SECONDARY = "#2563EB"
ACCENT = "#22C55E"


# ==========================================================
# PROCESSING TIME DISTRIBUTION CHART
# ==========================================================

def processing_time_distribution_chart():

    try:
        df = load_dataset()
        df = df[['processing_time_days']].copy()
        title = "Processing Time Distribution"
    except Exception:
        df = pd.DataFrame({"processing_time_days": [610, 620, 605, 600, 595, 590, 585, 590, 600, 610, 615, 620]})
        title = "Processing Time Distribution (Fallback)"

    fig = px.histogram(
        df,
        x='processing_time_days',
        nbins=25,
        title=title,
        labels={'processing_time_days': 'Processing Time (days)'},
        marginal='box'
    )

    fig.update_traces(marker_color=PRIMARY, marker_line_color='white', marker_line_width=1)

    fig.update_layout(
        template='plotly_dark',
        height=420,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Processing Time (days)',
        yaxis_title='Number of Cases'
    )

    return fig


# ==========================================================
# YEARLY PROCESSING TIME TREND CHART
# ==========================================================

def processing_time_yearly_trend_chart():

    try:
        df = load_dataset()
        df = df.groupby('application_year')['processing_time_days'].mean().reset_index()
        df.rename(columns={'processing_time_days': 'AvgProcessingTime'}, inplace=True)
        title = 'Average Processing Time by Year'
    except Exception:
        df = pd.DataFrame({
            'application_year': [2018, 2019, 2020, 2021, 2022, 2023, 2024],
            'AvgProcessingTime': [650, 630, 620, 610, 600, 595, 590]
        })
        title = 'Average Processing Time by Year (Fallback)'

    fig = px.line(
        df,
        x='application_year',
        y='AvgProcessingTime',
        markers=True,
        title=title,
        labels={'application_year': 'Year', 'AvgProcessingTime': 'Average Processing Time (days)'}
    )

    fig.update_traces(line=dict(color=ACCENT, width=3), marker=dict(size=8, color=SECONDARY))

    fig.update_layout(
        template='plotly_dark',
        height=420,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Year',
        yaxis_title='Average Processing Time (days)',
        hovermode='x unified'
    )

    return fig


# ==========================================================
# OFFICE PROCESSING TIME RANKING CHART
# ==========================================================


def processing_time_office_ranking_charts(top_n=10):
    """
    Returns two figures: slowest and fastest embassies by average processing time.
    """
    try:
        df = load_dataset()
        office_names = df['processing_office'].map(lambda code: OFFICE_DATA.get(code, {}).get('name', code))
        df = df.assign(Embassy=office_names)
        grouped = (
            df.groupby(['processing_office', 'Embassy'])['processing_time_days']
            .mean()
            .reset_index()
        )
        slowest = grouped.sort_values('processing_time_days', ascending=False).head(top_n)
        fastest = grouped.sort_values('processing_time_days', ascending=True).head(top_n)
        slowest.rename(columns={'processing_time_days': 'AvgProcessingTime'}, inplace=True)
        fastest.rename(columns={'processing_time_days': 'AvgProcessingTime'}, inplace=True)
    except Exception:
        slowest = pd.DataFrame({
            'Embassy': ['London', 'New York', 'Delhi', 'Mexico City', 'Sydney', 'Berlin', 'Singapore', 'Paris', 'Toronto', 'Dubai'],
            'AvgProcessingTime': [680, 670, 660, 650, 645, 640, 635, 630, 625, 620]
        })
        fastest = pd.DataFrame({
            'Embassy': ['Oslo', 'Helsinki', 'Wellington', 'Lisbon', 'Dublin', 'Prague', 'Vienna', 'Brussels', 'Stockholm', 'Copenhagen'],
            'AvgProcessingTime': [400, 410, 415, 420, 425, 430, 435, 440, 445, 450]
        })

    fig_slowest = px.bar(
        slowest,
        x='AvgProcessingTime',
        y='Embassy',
        orientation='h',
        title=f'Top {top_n} Slowest Embassies',
        labels={'AvgProcessingTime': 'Avg Processing Time (days)', 'Embassy': 'Embassy'},
        color='AvgProcessingTime',
        color_continuous_scale='Inferno'
    )
    fig_slowest.update_layout(
        template='plotly_dark',
        height=420,
        margin=dict(l=140, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Average Processing Time (days)',
        yaxis_title='Embassy'
    )
    fig_slowest.update_traces(marker_line_color='white', marker_line_width=1)

    fig_fastest = px.bar(
        fastest,
        x='AvgProcessingTime',
        y='Embassy',
        orientation='h',
        title=f'Top {top_n} Fastest Embassies',
        labels={'AvgProcessingTime': 'Avg Processing Time (days)', 'Embassy': 'Embassy'},
        color='AvgProcessingTime',
        color_continuous_scale='Tealgrn'
    )
    fig_fastest.update_layout(
        template='plotly_dark',
        height=420,
        margin=dict(l=140, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Average Processing Time (days)',
        yaxis_title='Embassy'
    )
    fig_fastest.update_traces(marker_line_color='white', marker_line_width=1)

    return fig_slowest, fig_fastest


# ==========================================================
# SEASONALITY PROCESSING TIME CHART
# ==========================================================

def processing_time_seasonality_chart():

    try:
        df = load_dataset()
        df['quarter'] = ((df['application_month'] - 1) // 3 + 1).astype(str)
        df = (
            df.groupby('quarter')['processing_time_days']
            .mean()
            .reset_index()
            .sort_values('quarter')
        )
        title = 'Average Processing Time by Quarter'
    except Exception:
        df = pd.DataFrame({
            'quarter': ['1', '2', '3', '4'],
            'processing_time_days': [620, 600, 590, 605]
        })
        title = 'Average Processing Time by Quarter (Fallback)'

    fig = px.bar(
        df,
        x='quarter',
        y='processing_time_days',
        title=title,
        labels={'quarter': 'Quarter', 'processing_time_days': 'Avg Processing Time (days)'},
        color='processing_time_days',
        color_continuous_scale='Tealgrn'
    )

    fig.update_layout(
        template='plotly_dark',
        height=420,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Quarter',
        yaxis_title='Average Processing Time (days)'
    )

    return fig


# ==========================================================
# LOAD DATASET
# ==========================================================

@st.cache_data
def load_dataset():
    return pd.read_csv("data/processed/engineered_dataset.csv")


# ==========================================================
# GLOBAL PROCESSING OFFICE MAP WITH FULL NAMES
# ==========================================================

@st.cache_data
def office_processing_map(selected_office=None):

    df = load_dataset()

    office_stats = (
        df.groupby("processing_office")["processing_time_days"]
        .mean()
        .reset_index()
    )

    rows = []

    for code, data in OFFICE_DATA.items():

        if code in office_stats["processing_office"].values:

            avg_time = office_stats[
                office_stats["processing_office"] == code
            ]["processing_time_days"].values[0]

            rows.append({
                "Office": data["name"],
                "Code": code,
                "lat": data["lat"],
                "lon": data["lon"],
                "ProcessingTime": int(round(avg_time))
            })

    map_df = pd.DataFrame(rows)

    fig = px.scatter_geo(
        map_df,
        lat="lat",
        lon="lon",
        color="ProcessingTime",
        size="ProcessingTime",
        size_max=20,
        hover_name="Office",
        labels={"ProcessingTime": "Processing Time"},
        projection="natural earth",
        color_continuous_scale="Turbo",
        title="Global Visa Processing Embassies"
    )

    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>Processing Time = %{marker.color}<extra></extra>"
    )

    fig.update_geos(
        showland=True,
        landcolor='rgba(0,0,0,0)',
        oceancolor='rgba(0,0,0,0)',
        showocean=True,
        showcountries=True,
        countrycolor="#334155"
    )

    # ======================================================
    # ZOOM + BLINK AI STATUS DOT
    # ======================================================

    if selected_office:

        office_data = OFFICE_DATA[selected_office]
        
        if not office_data:
            st.error("Selected office data not found.")
            return fig

        lat = office_data["lat"]
        lon = office_data["lon"]

        match = office_stats[
            office_stats["processing_office"] == selected_office
        ]

        if len(match) == 0:
            avg_time = 0
        else:
            avg_time = match["processing_time_days"].values[0]

        fig.add_trace(
            go.Scattergeo(
                lat=[lat],
                lon=[lon],
                mode="markers",
                marker=dict(
                    size=70,
                    color="rgba(34,197,94,0.08)",
                    line=dict(width=2,color="#22c55e")
                ),
                showlegend=False
            )
        )

        fig.add_trace(
            go.Scattergeo(
                lat=[lat],
                lon=[lon],
                mode="markers",
                marker=dict(
                    size=40,
                    color="rgba(34,197,94,0.15)",
                    line=dict(width=2,color="#22c55e")
                ),
                showlegend=False
            )
        )

        fig.update_geos(
            center=dict(lat=lat, lon=lon),
            projection_scale=3
        )

    fig.update_layout(
        template="plotly_dark",
        height=650,
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',  
        geo=dict(
            bgcolor='rgba(0,0,0,0)',   
            showcoastlines=True
        )
    )

    return fig


# ==========================================================
# REGION COMPARISON CHART
# ==========================================================

def region_comparison_chart():

    try:
        df = load_dataset()
        df = df.groupby('region')['processing_time_days'].mean().reset_index()
        df.rename(columns={'processing_time_days': 'AvgTime', 'region': 'Region'}, inplace=True)
    except Exception:
        df = pd.DataFrame({
            "Region": ["AF", "AS", "EU", "OC", "SA"],
            "AvgTime": [640, 610, 590, 570, 600]
        })

    fig = px.bar(
        df,
        x="Region",
        y="AvgTime",
        title="Average Processing Time by Region",
        color="AvgTime",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        template="plotly_dark",
        height=420,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        geo=dict(
            bgcolor='rgba(0,0,0,0)',   
            showcoastlines=True,
        )
    )

    return fig
