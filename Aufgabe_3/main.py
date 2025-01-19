# Importiere sys und QApplication für die Qt-Anwendung

import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
 
def main():
    """Initialisiert die Qt-Anwendung und startet das Hauptfenster."""
    app = QApplication(sys.argv)     # Erstelle eine Qt-Anwendung
    window = MainWindow()            # Erstelle das Hauptfenster
    window.show()                    # Zeige das Fenster an
    sys.exit(app.exec())             # Starte die Anwendung und blockiere die weitere Ausführung, bis die Anwendung geschlossen wird
 
if __name__ == "__main__":
    main()  