from datetime import UTC, datetime
from logging import getLogger
from typing import Literal

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from src.config import cwd, images_dir, reports_dir

logger = getLogger(__name__)


def get_cod_quality(service: str) -> Literal["Enhanced", "Standard", "Not Available"]:
    """_summary_.

    Args:
        service: _description_

    Returns:
        _description_
    """
    if service == "COD_External":
        return "Enhanced"
    if service == "COD_NO_GEOM_CHECK":
        return "Standard"
    return "Not Available"


def create_report(
    iso3: str,
    levels: int,
    metadata: dict,
    checks: list[dict],
    scores: dict,
) -> None:
    """Creates a PDF report for an admin boundary.

    Args:
        iso3: ISO3 of admin boundary.
        levels: Admin levels of boundary.
        metadata: location metadata.
        checks: location scores.
        scores: location checks.
    """
    environment = Environment(
        loader=FileSystemLoader(cwd / "reports/templates"),
        autoescape=True,
    )
    template = environment.get_template("report.html.j2")
    html = template.render(
        {
            "metadata": metadata,
            "scores": scores,
            "checks": checks,
            "today": datetime.now(tz=UTC).date(),
            "cod_quality": get_cod_quality(metadata["itos_service"]),
            "levels": levels,
            "admin_levels": range(levels + 1),
            "css": cwd / "reports/templates/report.css",
            "images_dir": images_dir,
        },
    )
    pdf_file = reports_dir / f"{iso3.lower()}.pdf"
    HTML(string=html).write_pdf(pdf_file)
