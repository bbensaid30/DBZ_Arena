import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def plot_turns_distribution(
    turns_list: list[int], f1_name: str, f2_name: str
) -> go.Figure:
    """Construit un histogramme Plotly de la durée des combats avec ligne de moyenne."""
    mean_turns = float(np.mean(turns_list))

    fig = px.histogram(
        x=turns_list,
        nbins=15,
        title=f"Distribution de la durée des duels : {f1_name} vs {f2_name}",
        labels={"x": "Nombre de tours", "y": "Nombre de simulations"},
        color_discrete_sequence=["#1f77b4"],
    )

    fig.add_vline(
        x=mean_turns,
        line_dash="dash",
        line_color="#d62728",
        annotation_text=f"Moyenne : {mean_turns:.1f} tours",
        annotation_position="top right",
    )

    fig.update_layout(
        yaxis_title="Nombre de combats",
        bargap=0.05,
        template="plotly_white",
    )
    return fig


def plot_fighters_radar(
    f1_stats: dict[str, int],
    f2_stats: dict[str, int],
    f1_name: str,
    f2_name: str,
) -> go.Figure:
    """Construit un diagramme radar comparant les caractéristiques des deux combattants."""
    categories = list(f1_stats.keys())
    categories_closed = categories + [categories[0]]
    v1 = list(f1_stats.values()) + [list(f1_stats.values())[0]]
    v2 = list(f2_stats.values()) + [list(f2_stats.values())[0]]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=v1,
            theta=categories_closed,
            fill="toself",
            name=f1_name,
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=v2,
            theta=categories_closed,
            fill="toself",
            name=f2_name,
        )
    )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        title=f"Profil Comparatif : {f1_name} vs {f2_name}",
        template="plotly_white",
    )
    return fig

if __name__ == "__main__":
    # Test visuel immédiat des deux fonctions
    fig_hist = plot_turns_distribution([4, 5, 6, 6, 7, 8, 5, 9, 10, 6], "Gohan", "Cell")
    fig_hist.show()

    s1 = {"PV Max": 150, "Attaque": 65, "Ki": 100}
    s2 = {"PV Max": 160, "Attaque": 60, "Ki": 80}
    fig_rad = plot_fighters_radar(s1, s2, "Gohan", "Cell")
    fig_rad.show()