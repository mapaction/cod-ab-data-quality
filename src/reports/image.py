from logging import getLogger

from geopandas import read_file
from plotly.graph_objects import Choropleth, Figure

from src.config import EPSG_WGS84, PLOTLY_SIMPLIFY, boundaries_dir, images_dir

logger = getLogger(__name__)


def create_png(iso3: str, level: int) -> None:
    """Creates a PNG for an admin boundary.

    Args:
        iso3: ISO3 of admin boundary.
        level: Admin level of boundary.
    """
    file = boundaries_dir / f"{iso3.lower()}_adm{level}.gpkg"
    if file.exists():
        gdf = read_file(file, use_arrow=True).to_crs(EPSG_WGS84)
        gdf = gdf[~gdf.geometry.is_empty]
        gdf.geometry = gdf.geometry.simplify(PLOTLY_SIMPLIFY)
        min_x, min_y, max_x, max_y = gdf.geometry.total_bounds
        fig = Figure(
            Choropleth(
                geojson=gdf.geometry.__geo_interface__,
                locations=gdf.index,
                z=gdf.index,
                colorscale=["#1F77B4", "#1F77B4"],
                marker_line_color="white",
            ),
        )
        fig.update_geos(
            bgcolor="rgba(0,0,0,0)",
            visible=False,
            lonaxis_range=[min_x, max_x],
            lataxis_range=[min_y, max_y],
        )
        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
        )
        fig.update_traces(showscale=False)
        fig.write_image(images_dir / f"{file.stem}.png", height=2000, width=2000)
