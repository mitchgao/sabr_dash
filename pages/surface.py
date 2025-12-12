import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Input, Output, dcc, html, callback
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from lib.sabr import SABR_market_vol, SABR_calibration


def pct_to_decimal(col):
    if isinstance(col, str) and col.endswith("%"):
        return float(col.replace("%", "")) / 100
    return col


vol_grid = pd.read_csv(
    "https://raw.githubusercontent.com/mitchgao/sabr_dash/main/data/black_vol.csv",
    index_col=0,
)

vol_grid = vol_grid.rename(columns=pct_to_decimal)
vol_grid.index = [int(ix.replace("Yr", "")) for ix in vol_grid.index]

df_vol = vol_grid.iloc[:, :-2]
df_forward = vol_grid.iloc[:, -2]
df_atm_vol = vol_grid.iloc[:, -1]


def get_sabr_vols(t_exp):
    beta = 0.5
    f = df_forward[t_exp] / 100
    atm_sigma = df_atm_vol[t_exp] / 100
    strikes = df_vol.columns
    sigmas = df_vol.loc[t_exp].values / 100
    guess = [0.15, 0.87, -0.5]
    alpha, nu, rho = SABR_calibration(f, t_exp, atm_sigma, beta, strikes, sigmas, guess)
    Ks = strikes
    sabr_vols = SABR_market_vol(Ks, f, t_exp, alpha, beta, nu, rho)
    return list(sabr_vols)


sabr_vol_grid = np.array(
    [get_sabr_vols(i) for i in list(np.arange(1, 11)) + [12, 15, 20, 25, 30]]
)
sh_0, sh_1 = sabr_vol_grid.shape
x, y = np.linspace(0, 1, sh_0), np.linspace(0, 1, sh_1)
sabr3d_fig = go.Figure(
    data=[
        go.Surface(
            z=sabr_vol_grid,
            x=x,
            y=y,
            colorscale="spectral",
            contours={
                "x": {
                    "show": True,
                    "color": "black",
                    "width": 1,
                    "project": {"x": True, "y": False, "z": False},
                },
                "y": {
                    "show": True,
                    "color": "black",
                    "width": 1,
                    "project": {"x": False, "y": True, "z": False},
                },
                "z": {"show": False},
            },
        )
    ]
)
sabr3d_fig.update_layout(
    # scene=dict(
    #     xaxis=dict(
    #         title="Tenor index",
    #         showgrid=True,
    #         gridcolor="black",
    #         gridwidth=2,
    #         zeroline=False,
    #     ),
    #     yaxis=dict(
    #         title="Strike index",
    #         showgrid=True,
    #         gridcolor="black",
    #         gridwidth=2,
    #         zeroline=False,
    #     ),
    #     zaxis=dict(
    #         title="Volatility",
    #         showgrid=True,
    #         gridcolor="black",
    #         gridwidth=2,
    #     ),
    # ),
    title=dict(text="Volatility Cube 3D Chart"),
    autosize=False,
    width=1000,
    height=500,
    margin=dict(l=65, r=50, b=65, t=90),
)

sabr3d_fig.update_yaxes(
    showgrid=True,
    gridwidth=2,
    gridcolor="black",
)
# Show gridlines for the x-axis
sabr3d_fig.update_xaxes(
    showgrid=True,
    gridwidth=2,
    gridcolor="black",
)

surface_page = html.Div(
    [
        dcc.Graph(id="sabr-3d-surface", figure=sabr3d_fig),
        dmc.Select(
            label="Select Tenor (Year)",
            placeholder="1Y",
            id="surface-tenor-select",
            value="1",
            data=[
                {"value": str(i), "label": f"{i}Y"}
                for i in list(np.arange(1, 11)) + [12, 15, 20, 25, 30]
            ],
            w=200,
            mb=10,
        ),
        dcc.Graph(id="sabr-smile-curve-output"),
    ]
)


@callback(
    Output("sabr-smile-curve-output", "figure"),
    Input("surface-tenor-select", "value"),
    # prevent_initial_call=True,
)
def get_sabr_vol(tenor):
    beta = 0.5
    t_exp = int(tenor)
    f = df_forward[t_exp] / 100
    atm_sigma = df_atm_vol[t_exp] / 100
    strikes = df_vol.columns
    sigmas = df_vol.loc[t_exp].values / 100
    guess = [0.15, 0.87, -0.5]
    alpha, nu, rho = SABR_calibration(f, t_exp, atm_sigma, beta, strikes, sigmas, guess)
    Ks = strikes
    sabr_vols = SABR_market_vol(Ks, f, t_exp, alpha, beta, nu, rho)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=Ks,
            y=sabr_vols,
            name="SABR Vols",
            line=dict(color="black", width=4),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=strikes,
            y=sigmas,
            name="Market Vols",
            mode="markers",
            marker=dict(color="firebrick", size=10),
        )
    )

    fig.update_layout(
        height=600,
        width=800,
        title=dict(text="Vol vs. Strike at Tenor " + tenor + "Y"),
        xaxis=dict(title=dict(text="Strike")),
        yaxis=dict(title=dict(text="Volatility")),
    )
    return fig
