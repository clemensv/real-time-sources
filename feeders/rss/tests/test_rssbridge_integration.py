"""
Integration tests for RSS Bridge with mocked external services.
Tests interactions with RSS/Atom feeds and web pages.
"""

import pytest
import requests
from unittest.mock import Mock, patch
from rssbridge.rssbridge import (
    extract_feed_urls_from_webpage,
)


@pytest.mark.integration
class TestFeedDiscovery:
    """Tests for RSS/Atom feed discovery from web pages"""

    @pytest.fixture
    def mock_webpage_with_feeds(self):
        """Create mock HTML with RSS/Atom feed links"""
        html = """
        <html>
        <head>
            <link rel="alternate" type="application/rss+xml" title="RSS Feed" href="https://example.com/feed.rss">
            <link rel="alternate" type="application/atom+xml" title="Atom Feed" href="https://example.com/feed.atom">
            <link rel="stylesheet" href="/style.css">
        </head>
        <body>Content</body>
        </html>
        """
        return html

    @pytest.fixture
    def mock_webpage_with_relative_feeds(self):
        """Create mock HTML with relative RSS feed links"""
        html = """
        <html>
        <head>
            <link rel="alternate" type="application/rss+xml" href="/feed.rss">
            <link rel="alternate" type="application/atom+xml" href="feed.atom">
        </head>
        <body>Content</body>
        </html>
        """
        return html

    def test_extract_feed_urls_from_webpage_absolute(self, mock_webpage_with_feeds):
        """Test extracting absolute feed URLs from web page"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = mock_webpage_with_feeds.encode('utf-8')
        
        with patch('requests.get', return_value=mock_response):
            feeds = extract_feed_urls_from_webpage('https://example.com')
            
            assert len(feeds) == 2
            assert 'https://example.com/feed.rss' in feeds
            assert 'https://example.com/feed.atom' in feeds

    def test_extract_feed_urls_from_webpage_relative(self, mock_webpage_with_relative_feeds):
        """Test extracting relative feed URLs and converting to absolute"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = mock_webpage_with_relative_feeds.encode('utf-8')
        
        with patch('requests.get', return_value=mock_response):
            feeds = extract_feed_urls_from_webpage('https://example.com')
            
            assert len(feeds) == 2
            assert any('https://example.com/feed.rss' in feed for feed in feeds)
            assert any('https://example.com/feed.atom' in feed for feed in feeds)

    def test_extract_feed_urls_no_feeds(self):
        """Test extracting from page with no feed links"""
        html = "<html><head></head><body>No feeds here</body></html>"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = html.encode('utf-8')
        
        with patch('requests.get', return_value=mock_response):
            feeds = extract_feed_urls_from_webpage('https://example.com')
            
            assert feeds == []

    def test_extract_feed_urls_http_error(self):
        """Test handling HTTP errors when fetching page"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        
        with patch('requests.get', return_value=mock_response):
            with pytest.raises(requests.exceptions.HTTPError):
                extract_feed_urls_from_webpage('https://example.com/notfound')

    def test_extract_feed_urls_timeout(self):
        """Test handling request timeout"""
        with patch('requests.get', side_effect=requests.exceptions.Timeout):
            with pytest.raises(requests.exceptions.Timeout):
                extract_feed_urls_from_webpage('https://example.com')


@pytest.mark.integration
class TestRSSFeedParsing:
    """Tests for RSS feed parsing with feedparser"""

    @pytest.fixture
    def mock_rss_feed(self):
        """Create a mock RSS feed XML"""
        rss = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <title>Test Feed</title>
                <link>https://example.com</link>
                <description>A test RSS feed</description>
                <item>
                    <title>Test Article 1</title>
                    <link>https://example.com/article1</link>
                    <description>First test article</description>
                    <pubDate>Mon, 01 Jan 2024 12:00:00 GMT</pubDate>
                    <guid>article1</guid>
                </item>
                <item>
                    <title>Test Article 2</title>
                    <link>https://example.com/article2</link>
                    <description>Second test article</description>
                    <pubDate>Tue, 02 Jan 2024 12:00:00 GMT</pubDate>
                    <guid>article2</guid>
                </item>
            </channel>
        </rss>
        """
        return rss

    @pytest.fixture
    def mock_atom_feed(self):
        """Create a mock Atom feed XML"""
        atom = """<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
            <title>Test Atom Feed</title>
            <link href="https://example.com"/>
            <updated>2024-01-01T12:00:00Z</updated>
            <entry>
                <title>Test Entry</title>
                <link href="https://example.com/entry1"/>
                <id>entry1</id>
                <updated>2024-01-01T12:00:00Z</updated>
                <summary>Test entry content</summary>
            </entry>
        </feed>
        """
        return atom

    def test_feedparser_can_parse_rss(self, mock_rss_feed):
        """Test that feedparser can parse RSS feed"""
        import feedparser
        
        feed = feedparser.parse(mock_rss_feed)
        
        assert feed.feed.title == 'Test Feed'
        assert len(feed.entries) == 2
        assert feed.entries[0].title == 'Test Article 1'
        assert feed.entries[0].link == 'https://example.com/article1'

    def test_feedparser_can_parse_atom(self, mock_atom_feed):
        """Test that feedparser can parse Atom feed"""
        import feedparser
        
        feed = feedparser.parse(mock_atom_feed)
        
        assert feed.feed.title == 'Test Atom Feed'
        assert len(feed.entries) == 1
        assert feed.entries[0].title == 'Test Entry'

    def test_feedparser_handles_malformed_feed(self):
        """Test handling of malformed feed"""
        import feedparser
        
        malformed = "<rss><channel><item>Missing closing tags"
        feed = feedparser.parse(malformed)
        
        # feedparser is lenient and won't raise errors
        assert feed is not None

    def test_feedparser_handles_empty_feed(self):
        """Test handling of empty feed"""
        import feedparser
        
        empty = ""
        feed = feedparser.parse(empty)
        
        assert feed is not None
        assert len(feed.entries) == 0


@pytest.mark.integration
class TestProducerClientIntegration:
    """Tests for Kafka producer client integration"""

    def test_producer_client_can_be_imported(self):
        """Test that producer client can be imported"""
        from rssbridge_producer_kafka_producer.producer import MicrosoftOpenDataRssFeedsEventProducer
        
        assert MicrosoftOpenDataRssFeedsEventProducer is not None

    def test_producer_data_classes_can_be_imported(self):
        """Test that producer data classes can be imported"""
        from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditem import FeedItem
        from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemtitle import FeedItemTitle
        from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemcontent import FeedItemContent
        
        assert FeedItem is not None
        assert FeedItemTitle is not None
        assert FeedItemContent is not None


@pytest.mark.integration
class TestOPMLParsing:
    """Tests for OPML file parsing"""

    def test_listparser_can_parse_opml(self):
        """Test that listparser can parse OPML files"""
        import listparser
        
        opml = """<?xml version="1.0"?>
        <opml version="1.0">
            <head><title>Test OPML</title></head>
            <body>
                <outline type="rss" text="Feed 1" xmlUrl="https://example.com/feed1.xml"/>
                <outline type="rss" text="Feed 2" xmlUrl="https://example.com/feed2.xml"/>
            </body>
        </opml>
        """
        
        result = listparser.parse(opml)
        
        assert len(result.feeds) == 2
        assert result.feeds[0].url == 'https://example.com/feed1.xml'
        assert result.feeds[1].url == 'https://example.com/feed2.xml'

    def test_listparser_handles_nested_outlines(self):
        """Test parsing OPML with nested outline elements"""
        import listparser
        
        opml = """<?xml version="1.0"?>
        <opml version="1.0">
            <body>
                <outline text="Category 1">
                    <outline type="rss" xmlUrl="https://example.com/feed1.xml"/>
                    <outline type="rss" xmlUrl="https://example.com/feed2.xml"/>
                </outline>
            </body>
        </opml>
        """
        
        result = listparser.parse(opml)
        
        assert len(result.feeds) == 2
