# auto_analyzer.py
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from startup_analyzer import StartupAnalyzerOllama
import json

class PDFHandler(FileSystemEventHandler):
    def __init__(self):
        self.analyzer = StartupAnalyzerOllama()
    
    def on_created(self, event):
        if event.src_path.endswith('.pdf'):
            print(f"🔍 Yeni PDF tespit edildi: {event.src_path}")
            time.sleep(1)  # Dosya yazımının bitmesini bekle
            
            try:
                result = self.analyzer.analyze_pitch_deck(event.src_path)
                
                # Sonucu kaydet
                output_file = f"results/{os.path.basename(event.src_path)}.json"
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2)
                
                print(f"✅ Analiz tamamlandı: {output_file}")
            except Exception as e:
                print(f"❌ Hata: {e}")

if __name__ == "__main__":
    print("👀 Watching pitch_decks/ klasörü...")
    print("📄 Yeni PDF eklendiğinde otomatik analiz yapılacak")
    
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, "pitch_decks/", recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()