import pytest
import sys
import os

# Ana dizini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from startup_analyzer import StartupAnalyzerOllama


@pytest.fixture
def analyzer():
    """Test için analyzer instance"""
    return StartupAnalyzerOllama(ollama_base_url="http://localhost:11434")


def test_analyzer_initialization(analyzer):
    """Analyzer doğru başlatılıyor mu?"""
    assert analyzer.base_url == "http://localhost:11434"


def test_fallback_analysis(analyzer):
    """Fallback analiz çalışıyor mu?"""
    result = analyzer.fallback_analysis("healthcare automation clinic patient")
    
    assert "problem" in result
    assert "solution" in result
    assert "target_market" in result
    assert "score" in result
    assert isinstance(result["score"], int)


def test_find_pattern(analyzer):
    """Pattern matching çalışıyor mu?"""
    text = "Our revenue is $150K and we have a team of 5 engineers."
    
    revenue = analyzer.find_pattern(text, r'revenue.*?(\$?[0-9,.]+[MK]?)')
    assert revenue == "$150K"
    
    team = analyzer.find_pattern(text, r'team.*?of.*?(\d+)')
    assert team == "5"


def test_find_pattern_not_found(analyzer):
    """Pattern bulunamazsa 'Not found' dönüyor mu?"""
    result = analyzer.find_pattern("Hello world", r'revenue.*?(\$\d+)')
    assert result == "Not found"


def test_analyze_startup_text_structure(analyzer):
    """AI analizi doğru yapıyı döndürüyor mu?"""
    text = "AI scheduling for clinics. $150K revenue. 5 people team."
    result = analyzer.analyze_startup_text(text)
    
    # Gerekli anahtarlar var mı?
    assert "problem" in result
    assert "solution" in result
    assert "target_market" in result
    assert "score" in result