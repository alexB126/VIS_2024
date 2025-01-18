import mbsModel
# Importiere Path, um mit Dateipfaden zu arbeiten
from pathlib import Path
# Importiere wichtige Klassen aus PySide6 (GUI-Komponenten)
from PySide6.QtWidgets import (QMainWindow, QWidget, QTreeWidget, QTreeWidgetItem, QHBoxLayout,
                               QFileDialog, QMenuBar, QStatusBar, QMessageBox,QSplitter)
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
 
        self.initUI()
 
    def create_menu(self):
        menubar = self.menuBar()
       
        # Datei-Menü hinzufügen
        file_menu = menubar.addMenu('File')
        view_menu = menubar.addMenu('View')
        control_menu = menubar.addMenu('Steuerung') # muss noch erweitert werden wenn Zeit!!

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

        top_view_action = QAction("Top View", self)
        top_view_action.triggered.connect(self.set_top_view)
        view_menu.addAction(top_view_action)

        front_view_action = QAction("Front View", self)
        front_view_action.triggered.connect(self.set_front_view)
        view_menu.addAction(front_view_action)

        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)

        zoom_fit_action = QAction("Fit All", self)
        zoom_fit_action.triggered.connect(self.fit_view_to_all)
        view_menu.addAction(zoom_fit_action)
 
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
        try:
            self.myModel = mbsModel.mbsModel()  # Erstelle ein neues Modell
            if self.myModel.loadDatabase(filename):  # Lade das Modell
                self.updateTreeWidget()  # Aktualisiere den Baum mit den neuen Daten
                self.statusBar().showMessage(f"Modell geladen: {filename}")
                self.vtkWidget.update_renderer(self.myModel)
            else:
                self.statusBar().showMessage("Fehler beim Laden des Modells: Datei konnte nicht geladen werden")
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
            self.vtkWidget.update_renderer(self.myModel)
            self.updateTreeWidget()
        except Exception as e:
            self.statusBar().showMessage(f"Fehler beim Importieren der FDD-Datei: {e}")
 
    def show_error_message(self, title, message):
        """Zeigt eine Fehlermeldung an."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    def set_top_view(self):
        camera = self.vtkWidget.renderer.GetActiveCamera()
        # z.B. Position 0,0,+100 (von oben)
        camera.SetPosition(0, 0, 100)
        # Focal point = 0,0,0 (Zielkoordinate)
        camera.SetFocalPoint(0, 0, 0)
        # "Oben" ist jetzt die Y-Achse oder X-Achse? 
        # Hier definieren wir z. B. "X-Achse" als "oben" in der Ansicht:
        camera.SetViewUp(1, 0, 0)  
        # Ggf. zum Abschluss "ResetCamera" anrufen, 
        # falls du die Szene an den Inhalt anpassen willst:
        self.vtkWidget.renderer.ResetCamera()

        self.vtkWidget.GetRenderWindow().Render()

    def set_front_view(self):
        camera = self.vtkWidget.renderer.GetActiveCamera()
        # Position = 0,-100,0 (Blick Richtung +y, also "nach oben" in Y)
        camera.SetPosition(0, -100, 0)
        # Focal point
        camera.SetFocalPoint(0, 0, 0)
        # "Oben" = Z-Achse
        camera.SetViewUp(0, 0, 1)
        
        # Optional:
        self.vtkWidget.renderer.ResetCamera()
        
        self.vtkWidget.GetRenderWindow().Render()

    def zoom_in(self):
        camera = self.vtkWidget.renderer.GetActiveCamera()
        camera.Zoom(1.2)  # 20% reinzoomen
        self.vtkWidget.GetRenderWindow().Render()

    def fit_view_to_all(self):
        # Ermittelt den Bounding-Box-Umfang aller sichtbaren Props/Actors im Renderer 
        # und stellt die Kamera so ein, dass sie alles vollständig erfasst:
        self.vtkWidget.renderer.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()

    def initUI(self):
        # Erstelle einen QSplitter (horizontal = nebeneinander)
        splitter = QSplitter(Qt.Horizontal, self)
        
        # Erzeuge das TreeWidget
        self.treeWidget = QTreeWidget()
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabels(["Strukturbaum"])

        # Erzeuge dein VTK-Widget
        self.vtkWidget = MainWidget(self)

        # Füge beide Widgets dem QSplitter hinzu
        splitter.addWidget(self.treeWidget)
        splitter.addWidget(self.vtkWidget)

        # Wenn du willst, kannst du eine Start-Größenverteilung festlegen, z.B.:
        # (Erster Wert = Breite des TreeWidgets, zweiter Wert = Breite des VTK-Widgets)
        splitter.setSizes([200, 600])

        # Setze diesen Splitter als zentrales Widget des MainWindow
        self.setCentralWidget(splitter)

        # Hintergrund & erster Render-Durchlauf
        self.vtkWidget.renderer.SetBackground(0, 0, 0)
        self.vtkWidget.GetRenderWindow().Render()


    def updateTreeWidget(self):
        self.treeWidget.clear()
        
        root_item = QTreeWidgetItem(["Model"])
        self.treeWidget.addTopLevelItem(root_item)
        
        # Merkt sich Kategorie-Knoten wie "Body" -> QTreeWidgetItem
        category_nodes = {}
        # Hier führen wir jetzt Zähler pro Typ
        type_counts = {}

        for obj in self.myModel.mbsObjectList:
            main_type = obj.getType()    # z.B. "Body", "Force" ...
            sub_type  = obj.getSubType() # z.B. "Rigid_EulerParameter_PAI"
            
            # Falls noch keine Kategorie existiert, anlegen:
            if main_type not in category_nodes:
                category_item = QTreeWidgetItem([main_type + "s"])
                root_item.addChild(category_item)
                category_nodes[main_type] = category_item
                type_counts[main_type] = 0   # Zähler initialisieren

            # Hochzählen
            type_counts[main_type] += 1
            display_name = f"{main_type} {type_counts[main_type]}"

            # Wenn du zusätzlich den Subtype sehen willst:
            # display_name += f" ({sub_type})"

            # Objekt-Knoten einfügen
            object_item = QTreeWidgetItem([display_name])
            category_nodes[main_type].addChild(object_item)

        root_item.setExpanded(True)
