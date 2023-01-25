from pathlib import Path
from .italy import Italy

readme = Path(__file__).parent / "ReadMe.md"

__all__ = [
    Italy,
    readme,
]
