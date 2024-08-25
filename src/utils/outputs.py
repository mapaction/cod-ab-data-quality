"""Module for settings up output directories, and writing to them"""

from datetime import datetime

from src import config


class Output:
    def __init__(self):
        if not self.output_dir_exists():
            self.create_output_dir()

    @staticmethod
    def output_dir_exists(self) -> bool:
        """Check output dir exists"""
        return config.outputs_dir.is_dir()

    @staticmethod
    def create_output_dir(self) -> None:
        """Create output dir if not exists"""
        config.outputs_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def write(self, country_iso: str, check_name: str, data: float) -> None:
        """Write, handling naming and formatting"""
        result_dir = config.outputs_dir / check_name
        result_dir.mkdir(parents=True, exist_ok=True)
        output_file_path = result_dir / f"{country_iso}_{datetime.now().isoformat()}"
        with open(output_file_path, "w") as f:
            f.write(str(data))
