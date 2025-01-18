import matplotlib.pyplot as plt
import pandas as pd

# Excel-Datei einlesen
datei = r'C:\Users\126al\Desktop\Mappe1.xlsx'

# Datei einlesen und Spaltennamen prüfen
df = pd.read_excel(datei)
print("Spaltennamen:", df.columns)

# Sicherstellen, dass alle Leerzeichen entfernt werden
df.columns = df.columns.str.strip()

# Zugriff auf die Spalten
if 'Spannung' in df.columns and 'Frequenz' in df.columns and 'Amplitude' in df.columns:
    spannung = df['Spannung']
    frequenz = df['Frequenz']
    amplitude = df['Amplitude']
else:
    print("Eine oder mehrere benötigte Spalten fehlen!")
    exit()

# Drehzahl berechnen und hinzufügen
df['Drehzahl'] = spannung * 9 - 1.6
drehzahl = df['Drehzahl']

# Plot erstellen
plt.figure(figsize=(10, 6))

# Farbkodierung nach Amplitude
scatter = plt.scatter(drehzahl, frequenz, c=amplitude, cmap='viridis', s=100)
plt.colorbar(scatter, label='Amplitude (dB)')

# Achsentitel
plt.title("Campbell-Diagramm")
plt.xlabel("Drehzahl (V)")
plt.ylabel("Frequenz (Hz)")

# Diagramm anzeigen
plt.grid()
plt.show()
