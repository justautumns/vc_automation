# monitoring.py
import logging
from prometheus_client import start_http_server, Counter, Histogram
import time

# ✅ EKLE: startup_analyzer.py'den import et
from startup_analyzer import StartupAnalyzerOllama

# Metrics
pdf_processed = Counter('pdf_processed_total', 'Total PDFs processed')
analysis_duration = Histogram('analysis_duration_seconds', 'Analysis duration')
errors = Counter('analysis_errors_total', 'Total errors')

class MonitoredAnalyzer(StartupAnalyzerOllama):
    def analyze_pitch_deck(self, pdf_path: str):
        with analysis_duration.time():
            try:
                result = super().analyze_pitch_deck(pdf_path)
                pdf_processed.inc()
                return result
            except Exception as e:
                errors.inc()
                logging.error(f"Error: {e}")
                raise

if __name__ == "__main__":
    # Logging ayarla
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Prometheus metrics sunucusu başlat
    start_http_server(8000)
    print("📊 Prometheus metrics: http://localhost:8000/metrics")
    
    # Analyzer'ı çalıştır
    analyzer = MonitoredAnalyzer()
    
    # Örnek kullanım
    import os
    pdf_folder = "pitch_decks"
    
    if os.path.exists(pdf_folder):
        for filename in os.listdir(pdf_folder):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(pdf_folder, filename)
                print(f"\n📄 Analyzing: {filename}")
                try:
                    result = analyzer.analyze_pitch_deck(pdf_path)
                    print(f"✅ Success: {filename}")
                except Exception as e:
                    print(f"❌ Error: {e}")
    
    # Sunucuyu açık tut
    print("\n⏳ Metrics server running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")