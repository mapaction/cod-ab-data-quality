from logging import getLogger

from src.config import tables_dir
from src.utils import read_csv

from . import (
    geometry_areas,
    geometry_topology,
    geometry_validity,
    output,
    table_areas,
    table_dates,
    table_languages,
    table_names,
    table_pcodes,
)

logger = getLogger(__name__)


def main() -> None:
    """Applies scoring to the summarized values in "checks.csv".

    1. Create an iterable with each item containing the scoring function.

    2. Iterate through the score functions, generating a list of new DataFrames.

    3. After all the scoring has been performed, join the DataFrames together by ISO3
    and admin level.

    4. Output the final result to Excel: "data/tables/cod_ab_data_quality.xlsx".
    """
    logger.info("Starting")

    # NOTE: Register scores here.
    score_functions = (
        geometry_validity,
        geometry_topology,
        geometry_areas,
        table_pcodes,
        table_names,
        table_languages,
        table_dates,
        table_areas,
    )

    metadata = read_csv(tables_dir / "metadata.csv")
    checks = read_csv(tables_dir / "checks.csv")
    score_results = []
    for function in score_functions:
        partial = function.main(checks)
        score_results.append(partial)
    output_table = None
    for partial in score_results:
        if output_table is None:
            output_table = partial
        else:
            output_table = output_table.merge(
                partial,
                on=["iso3", "level"],
                how="outer",
            )
    if output_table is not None:
        output.main(metadata, output_table)
    logger.info("Finished")


if __name__ == "__main__":
    main()
