"""Tests for the HTTP client directory listing parser."""

from dwd.util.http_client import parse_directory_listing


SAMPLE_LISTING = """\
<html><body>
<pre><a href="../">../</a>
<a href="10minutenwerte_TU_00044_now.zip">10minutenwerte_TU_00044_now.zip</a>                    02-Apr-2026 06:20:00                 718
<a href="10minutenwerte_TU_00073_now.zip">10minutenwerte_TU_00073_now.zip</a>                    02-Apr-2026 06:20:00                 711
<a href="zehn_now_tu_Beschreibung_Stationen.txt">zehn_now_tu_Beschreibung_Stationen.txt</a>             15-Mar-2026 12:00:00               48000
</pre></body></html>
"""


class TestDirectoryListingParser:
    def test_parses_entries(self):
        entries = parse_directory_listing(SAMPLE_LISTING)
        assert len(entries) == 3

    def test_filenames(self):
        entries = parse_directory_listing(SAMPLE_LISTING)
        names = [e.name for e in entries]
        assert "10minutenwerte_TU_00044_now.zip" in names
        assert "10minutenwerte_TU_00073_now.zip" in names

    def test_timestamp(self):
        entries = parse_directory_listing(SAMPLE_LISTING)
        assert entries[0].modified.year == 2026
        assert entries[0].modified.month == 4
        assert entries[0].modified.day == 2

    def test_skips_parent(self):
        entries = parse_directory_listing(SAMPLE_LISTING)
        names = [e.name for e in entries]
        assert "../" not in names

    def test_empty(self):
        entries = parse_directory_listing("")
        assert entries == []
