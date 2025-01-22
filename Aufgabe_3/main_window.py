import mbsModel
# Importiere Path, um mit Dateipfaden zu arbeiten
from pathlib import Path
# Importiere wichtige Klassen aus PySide6 (GUI-Komponenten)
from PySide6.QtWidgets import (QMainWindow, QWidget, QTreeWidget, QTreeWidgetItem, QHBoxLayout,
                               QFileDialog, QMenuBar, QStatusBar, QMessageBox,QSplitter)
from PySide6.QtGui import QAction, QKeySequence,QColor
from PySide6.QtWidgets import QMainWindow, QFileDialog, QStatusBar, QMessageBox, QColorDialog,QDialog, QPushButton, QVBoxLayout, QGroupBox,QLabel, QSlider, QHBoxLayout, QLineEdit
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
        # VTK widget erstellen und konfig
        self.initUI()
 
    def create_menu(self):
        menubar = self.menuBar()
       
        # Datei-Menü hinzufügen
        file_menu = menubar.addMenu('File')
        view_menu = menubar.addMenu('View')
        settings_menu = menubar.addMenu('Settings') # für die Hintergrundfarbe

        # 'Backroundcolor' Aktion hinzufügen
        backgroundcolor_action = QAction('Background', self)
        backgroundcolor_action.triggered.connect(self.backgroundaction)
        settings_menu.addAction(backgroundcolor_action)

        # 'Backroundcolor' Aktion hinzufügen
        bodycolor_action = QAction('BodyColor', self)
        bodycolor_action.triggered.connect(self.bodycolorfunction)
        settings_menu.addAction(bodycolor_action)

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
 
    def backgroundaction(self):
        print('Test123')
        backgroundcolor  = QColorDialog.getColor()
        if backgroundcolor.isValid():
            # z.B. direkt Float-Werte im Bereich [0..1]:
            r = backgroundcolor.redF()
            g = backgroundcolor.greenF()
            b = backgroundcolor.blueF()

            # Renderer-Hintergrund setzen
            self.vtkWidget.renderer.SetBackground(r, g, b)

            # Neu zeichnen
            self.vtkWidget.GetRenderWindow().Render()
            self.myModel.backgroundcolor = r,g,b
        self.statusBar().showMessage(f"new Background color")

    def bodycolorfunction(self):
        bodywindow = QDialog()
        bodywindow.setWindowTitle("Eigenschaften fur Korper")
        mainlayout = QVBoxLayout(bodywindow)
        #bodywindow.setGeometry(150,150,600,400)
        self.listofBodies = []
        for obj in  self.myModel.getlistofMBSObjects(): 
            if obj.getType() == "Body":
                self.listofBodies.append(obj)
        self.Anzeigefarbe = []
        for body in self.listofBodies: 
            unterwindow = QGroupBox(f"properties for {body.parameter["name"]["value"]}") 
            layout = QVBoxLayout(unterwindow)
            mainlayout.addWidget(unterwindow)

            label_color = QLabel("Farbe")
            layout.addWidget(label_color)

            self.Anzeigefarbe.append(QLineEdit())
            self.Anzeigefarbe[self.listofBodies.index(body)].setReadOnly(True)
            color_show = QColor(body.parameter["color"]["value"][0]*255,body.parameter["color"]["value"][1]*255,body.parameter["color"]["value"][2]*255)
            self.Anzeigefarbe[self.listofBodies.index(body)].setStyleSheet(f"background-color: {color_show.name()};")      
            layout.addWidget(self.Anzeigefarbe[self.listofBodies.index(body)])
            
            Color_button = QPushButton("Farbe wählen")
            Color_button.clicked.connect(lambda checked, bodycolor = body, index=self.listofBodies.index(body) :self.bodycolor(bodycolor, index))
            layout.addWidget(Color_button)

            label_transparency = QLabel("Transparenz")
            layout.addWidget(label_transparency)
            layout_slider = QHBoxLayout()
            label_left = QLabel("0%")
            layout_slider.addWidget(label_left)
            transparency_slider = QSlider(Qt.Horizontal)
            transparency_slider.setMinimum(0)
            transparency_slider.setMaximum(100)
            transparency_slider.setValue(body.parameter["transparency"]["value"]/255*100) # von 255 max auf 100 max
            transparency_slider.valueChanged.connect(lambda value,bodyslider = body: self.transparency_update(value, bodyslider))
            layout_slider.addWidget(transparency_slider)
            label_right = QLabel("100%")
            layout_slider.addWidget(label_right)
            layout.addLayout(layout_slider)

        OK_Button = QPushButton("bast perfect")
        OK_Button.clicked.connect(lambda: self.push_ok(bodywindow))
        mainlayout.addWidget(OK_Button)
        bodywindow.exec()
    
    def transparency_update(self,value,body):
        body.parameter["transparency"]["value"] = value *255/100
        self.statusBar().showMessage(f"transparenz geändert")
       
    def bodycolor(self,body, indexbody):
        bodycolor = QColorDialog.getColor()
        if bodycolor.isValid():
            r = bodycolor.redF()  # r .. 0 - 1
            g = bodycolor.greenF()
            b = bodycolor.blueF()

            # Renderer-Körper setzen
            body.parameter["color"]["value"] = [r,g,b,1.0]
            self.Anzeigefarbe[indexbody].setStyleSheet(f"background-color: {bodycolor.name()};")

            self.myModel.bodycolor = r,g,b
            self.vtkWidget.GetRenderWindow().Render()
        self.statusBar().showMessage(f"New Body color(s)")

    def push_ok(self,window):
        for body in self.listofBodies: 
            body.hide(self.vtkWidget.renderer)
            body.updateActor()
            body.show(self.vtkWidget.renderer)
        window.accept()

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
                self.vtkWidget.renderer.SetBackground(self.myModel.backgroundcolor)
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
        self.statusBar().showMessage(f"set top view")

        self.vtkWidget.GetRenderWindow().Render()

    def set_front_view(self):
        camera = self.vtkWidget.renderer.GetActiveCamera()
        # Position = 0,-100,0 (Blick Richtung +y, also "nach oben" in Y)
        camera.SetPosition(0, -100, 0)
        # Focal point
        camera.SetFocalPoint(0, 0, 0)
        # "Oben" = Z-Achse
        camera.SetViewUp(0, 0, 1)
        self.statusBar().showMessage(f"set front view")
        # Optional:
        self.vtkWidget.renderer.ResetCamera()
        
        self.vtkWidget.GetRenderWindow().Render()

    def zoom_in(self):
        camera = self.vtkWidget.renderer.GetActiveCamera()
        camera.Zoom(1.2)  # 20% reinzoomen
        self.vtkWidget.GetRenderWindow().Render()
        self.statusBar().showMessage(f"zoomed in ")

    def fit_view_to_all(self):
        # Ermittelt den Bounding-Box-Umfang aller sichtbaren Props/Actors im Renderer 
        # und stellt die Kamera so ein, dass sie alles vollständig erfasst:
        self.vtkWidget.renderer.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()
        self.statusBar().showMessage(f"fit to 100%")

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

        # größe des Struckturbaum
        splitter.setSizes([200, 600])

        # Setze diesen Splitter als zentrales Widget des MainWindow
        self.setCentralWidget(splitter)

        # Hintergrund & erster Render-Durchlauf
        self.vtkWidget.renderer.SetBackground(0,0,0) #hinzufügen der Farben, Normierung zwischen 0,1
        self.vtkWidget.GetRenderWindow().Render()

    def updateTreeWidget(self):
        self.treeWidget.clear()
        
        root_item = QTreeWidgetItem(["Model"])
        self.treeWidget.addTopLevelItem(root_item)
        
        category_nodes = {}
        type_counts = {}  # wenn kein name vorhanden ist wird mit Force 1 bis n gezählt 

        for obj in self.myModel.mbsObjectList:
            main_type = obj.getType()    #  Body, Force, ...
            sub_type  = obj.getSubType() # vorher gelöst mit diesre variante bis auf name umgestellt wurde

            if main_type not in category_nodes:
                category_item = QTreeWidgetItem([main_type + "s"])
                root_item.addChild(category_item)
                category_nodes[main_type] = category_item
                type_counts[main_type] = 0

            # Namen aus den Objekten auslesen
            if "name" in obj.parameter and "value" in obj.parameter["name"]:
                display_name = obj.parameter["name"]["value"]
            else:
                # Fallback, falls kein "name" vorhanden:
                type_counts[main_type] += 1
                display_name = f"{main_type} {type_counts[main_type]}"

            object_item = QTreeWidgetItem([display_name])
            category_nodes[main_type].addChild(object_item)

        root_item.setExpanded(True)
        self.statusBar().showMessage(f"updated Tree")
