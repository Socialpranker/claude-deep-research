"""Counting logic verified on a tiny known fixture — independent of live numbers."""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import catalog_counts  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "mini_catalog"


def test_blocks_counts_two_and_excludes_index():
    # fixture has 2 real blocks in frame.md and a decoy line in INDEX.md
    assert catalog_counts._count_blocks(FIX) == 2


def test_channels_counts_one():
    assert catalog_counts._count_channels(FIX) == 1
