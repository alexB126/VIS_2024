import mbsModel
# Importiere Path, um mit Dateipfaden zu arbeiten
from pathlib import Path
# Importiere wichtige Klassen aus PySide6 (GUI-Komponenten)
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QFileDialog, QStatusBar, QMessageBox
from PySide6.QtCore import Qt
# Importiere das MainWidget für das Rendering
from main_widget import MainWidget
# Importiere den Renderer aus VTK
from vtkmodules.vtkRenderingCore import vtkRenderer
# Importiere QVTKRenderWindowInteractor für die Interaktion mit dem VTK-Renderfenster
import QVTKRenderWindowInteractor as QVTK
 
QVTKRenderWindowInteractor = QVTK.QVTKRenderWindowInteractor  # Alias für das QVTKRenderWindowInteractor-Modul
 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
 
        # Hauptfenster konfigurieren
        self.setWindowTitle("3D Modell in Qt mit VTK")  # Setze den Titel des Fensters
        self.setGeometry(100, 100, 800, 600)  # Setze die Fenstergröße und Position
       
        # Menüleiste erstellen
        self.create_menu()
        # Statusleiste erstellen
        self.create_status_bar()
 
        # VTK-Widget und -Renderer initialisieren
        self.widget = MainWidget(self)  # Erstelle ein VTK-Widget
       
        # Setze den Hintergrund des Renderers auf Schwarz
        self.widget.renderer.SetBackground(0.0, 0.0, 0.0)  # Hintergrund für den Renderer auf Schwarz
 
        # Setze das Widget als zentrales Widget des Fensters
        self.setCentralWidget(self.widget)
 
        # Initialisiere das RenderWindow, um den Hintergrund anzuzeigen
        self.widget.GetRenderWindow().Render()  # Rendere das Fenster, um den schwarzen Hintergrund zu sehen
 
    def create_menu(self):
        menubar = self.menuBar()
       
        # Datei-Menü hinzufügen
        file_menu = menubar.addMenu('File')
        view_menu = menubar.addMenu('View')

        # 'Load' Aktion hinzufügen
        load_action = QAction('Load', self)
        load_action.triggered.connect(self.load_model)
        file_menu.addAction(load_action)
 
        # 'Save' Aktion hinzufügen
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_model)
        file_menu.addAction(save_action)
 
        # 'Import FDD' Aktion hinzufügen
        import_action = QAction('ImportFdd', self)
        import_action.triggered.connect(self.import_fdd)
        file_menu.addAction(import_action)
 
        # 'Exit' Aktion hinzufügen
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
 
    def create_status_bar(self):
        """Erstellt die Statusleiste und zeigt eine Nachricht an."""
        self.statusBar().showMessage("Kein Modell geladen")
 
 # verbesserung möglich indem man mehr files einlesen kann
    def load_model(self):
        """Lädt ein Modell aus einer JSON-Datei."""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json)", options=options) # filename = pfad, _ = art des files 
       
        if filename:
            if filename.lower().endswith(".json"):  # Überprüfe, ob die Datei eine JSON-Datei ist
                self.load_json_model(filename)
            else:
                self.show_error_message("Ungültige Datei", "Bitte wählen Sie eine gültige JSON-Datei aus.")
        else:
            self.statusBar().showMessage("Modell-Laden abgebrochen")
 
    def load_json_model(self, filename):
        """Lädt das Modell aus einer JSON-Datei und zeigt es im VTK-Renderer."""
        try:
            self.myModel = mbsModel.mbsModel()  # Erstelle ein neues Modell
            self.myModel.loadDatabase(Path(filename))  # Lade das Modell aus der JSON-Datei
            self.statusBar().showMessage(f"Modell geladen: {filename}")
            self.widget.update_renderer(self.myModel)  # ohne update sieht man es noch ned 
        except Exception as e:
            self.statusBar().showMessage(f"Fehler beim Laden des Modells: {e}")
 
    def save_model(self):
        """Speichert das Modell in einer JSON-Datei."""
        options = QFileDialog.Options()     # dialog öffnen vom explorer
        filename, _ = QFileDialog.getSaveFileName(self, "Save Model File", "", "JSON Files (*.json)", options=options)
        if filename:
            self.myModel.saveDatabase(Path(filename))  # Speichert das Modell bzw den Pfad + Pfadnahme
            self.statusBar().showMessage(f"Modell gespeichert: {filename}")
 
    def import_fdd(self):
        """Importiert ein FDD-Modell aus einer Datei."""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Import FDD File", "", "FDD Files (*.fdd *.json)", options=options)
        if filename:
            if filename.lower().endswith(".fdd"):  # Überprüfe, ob die Datei eine JSON-Datei ist
                self.import_fdd_file(filename)
            else:
                self.show_error_message("Ungültige Datei", "Bitte wählen Sie eine gültige FDD-Datei aus.")
        else:
            self.statusBar().showMessage("Modell-Laden abgebrochen")

    def import_fdd_file(self, filename):
        """Lädt das Modell aus einer FDD-Datei."""
        try:
            self.myModel = mbsModel.mbsModel()
            self.myModel.importFddFile(filename)
            self.statusBar().showMessage(f"FDD-Datei importiert: {filename}")
            self.widget.update_renderer(self.myModel)
        except Exception as e:
            self.statusBar().showMessage(f"Fehler beim Importieren der FDD-Datei: {e}")
 
    def show_error_message(self, title, message):
        """Zeigt eine Fehlermeldung an."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()
        