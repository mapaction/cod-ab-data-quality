"""The main entry point to the script."""

from .checks.__main__ import main as checks
from .download.__main__ import main as download
from .metadata.__main__ import main as metadata
from .scores.__main__ import main as scores


def main():
    """Main function."""
    metadata()
    download()
    checks()
    scores()


if __name__ == "__main__":
    main()
