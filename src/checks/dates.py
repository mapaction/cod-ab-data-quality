"""Check for validating dates."""

from geopandas import GeoDataFrame


def main(result: list, iso3: str, gdfs: list[GeoDataFrame]):
    for level, gdf in enumerate(gdfs):
        row = {"iso3": iso3, "level": level}
        try:
            gdf_date = gdf["date"].dt.date.drop_duplicates()
            for index, value in enumerate(gdf_date):
                row[f"date_{index+1}"] = value
            gdf_update = gdf["validOn"].dt.date.drop_duplicates()
            for index, value in enumerate(gdf_update):
                row[f"update_{index+1}"] = value
        except KeyError:
            pass
        result.append(row)
