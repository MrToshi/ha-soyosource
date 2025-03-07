# Soyosource Controller Integration für Home Assistant

Diese Integration ermöglicht die Einbindung eines Soyosource Controllers in Home Assistant.

## Features

- Abfrage und Anzeige von Leistungsdaten des Soyosource Controllers
- Konfigurierbare IP-Adresse
- Konfigurierbare Aktualisierungszeit (1-3600 Sekunden)
- Folgende Sensoren werden erstellt:
  - L1L2L3 (Leistung in Watt)
  - Max Power (Maximale Leistung in Watt)
  - DC Ampere (Gleichstrom in Ampere)
  - DC Volt (Gleichspannung in Volt)
  - DC Watt (Gleichstromleistung in Watt)
  - Watts Out (Ausgangsleistung in Watt)

## Installation

### HACS (empfohlen)

1. Öffnen Sie HACS in Home Assistant
2. Klicken Sie auf die drei Punkte oben rechts und wählen Sie "Benutzerdefinierte Repositories"
3. Fügen Sie diese URL als "Integration" hinzu
4. Klicken Sie auf "Herunterladen"
5. Starten Sie Home Assistant neu

### Manuelle Installation

1. Laden Sie den Inhalt dieses Repositories herunter
2. Kopieren Sie den Ordner `custom_components/soyosource` in Ihr Home Assistant `custom_components` Verzeichnis
3. Starten Sie Home Assistant neu

## Konfiguration

1. Gehen Sie zu Einstellungen -> Geräte & Dienste -> Integration hinzufügen
2. Suchen Sie nach "Soyosource Controller"
3. Geben Sie die IP-Adresse Ihres Controllers ein
4. Optional: Passen Sie die Aktualisierungszeit an (Standard: 30 Sekunden)

## Unterstützte Geräte

- Soyosource Controller

## API Endpunkte

Die Integration nutzt den folgenden API-Endpunkt des Controllers:
- `http://<ip-adresse>/data`

## Fehlerbehebung

Falls Probleme auftreten:
1. Prüfen Sie, ob der Controller erreichbar ist
2. Überprüfen Sie die IP-Adresse
3. Schauen Sie in die Home Assistant Logs

## Mitwirken

Beiträge sind willkommen! Bitte erstellen Sie einen Pull Request oder ein Issue. 