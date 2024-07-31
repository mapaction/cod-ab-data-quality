import re
from pathlib import Path

import shapefile

# admin_boundary_regex = r"^[aA][dD](Mm)?(Ii)?(Nn)?[0-9].*?"
# admin_boundary_regex = r"^[aA][dD](Mm)?(Ii)?(Nn)?([0-9]+).*?"
admin_boundary_regex = r"^[aA][dD](?:M|I|N)*(\d).*"


def table_data_formatting_has_data_cols(shapefile_path: str) -> float:
    """Check completeness of an admin boundary by checking the columns.

    Args:
        shapefile_path - a string representing the shapefile to analyse.

    Returns:
         1 if _any_ columns match the regex. 0 otherwise.
    """
    sf = shapefile.Reader(shapefile_path)
    field_names = (field[0] for field in sf.fields)
    for name in field_names:
        if re.match(admin_boundary_regex, name, re.IGNORECASE):
            return 1
    return 0


def table_data_formatting_has_hierarchical_cols(shapefile_path: str) -> float:
    """Check completeness of an admin boundary by checking
    column relationships.

    Admin boundaries appear to have a hierarchical structure, where each
    file of "smaller" admin boundaries (i.e. admin4 vs admin3) has column
    names which reference the previous "larger" admin boundary. For example,
    the admin4.shp will have columns called admin3*, admin2*, admin1* and
    admin0*.

    Args:
        shapefile_path - a string representing the shapefile to analyse.

    Returns:
        float, the proportion of expected columns in that file. e.g. if
        admin1.shp had admin1* and admin0* columns it would return 1. If it had
        just admin0* column it would return 0.5. If it had neither it would
        return 0.
    """

    file_name = Path(shapefile_path).name
    match = re.search(r"adm(\d)", file_name, re.IGNORECASE)
    sf = shapefile.Reader(shapefile_path)
    if match:
        admin_level = int(match.group(1))
        seen_numbers = set()
        field_names = (field[0] for field in sf.fields)
        # Find all the numbers in column names (e.g. '3' in ADM3_PCODE).
        for name in field_names:
            if match := re.match(admin_boundary_regex, name, re.IGNORECASE):
                seen_numbers.add(int(match.group(1)))
        number_of_matches = 0
        # Count backwards, checking lower numbers are
        # in col names (e.g. 2,1,0 for ADM2_*).
        for i in range(admin_level, -1, -1):
            if i in seen_numbers:
                number_of_matches += 1
        return number_of_matches / (admin_level + 1)
    return 0
