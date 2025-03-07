#!/bin/bash

# Farben für die Ausgabe
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Initialisiere Git-Repository...${NC}"
git init

echo -e "${GREEN}Füge Remote-Repository hinzu...${NC}"
git remote add origin https://github.com/$1/ha-soyosource.git

echo -e "${GREEN}Aktualisiere Dateien mit GitHub-Benutzernamen...${NC}"
sed -i "s/yourusername/$1/g" README.md
sed -i "s/yourusername/$1/g" INFO.md
sed -i "s/yourusername/$1/g" custom_components/soyosource/manifest.json
sed -i "s/yourusername/$1/g" LICENSE

echo -e "${GREEN}Füge Dateien zum Repository hinzu...${NC}"
git add .

echo -e "${GREEN}Erstelle ersten Commit...${NC}"
git commit -m "Initial commit: Soyosource Controller Integration"

echo -e "${GREEN}Erstelle main Branch...${NC}"
git branch -M main

echo -e "${GREEN}Pushe Code zu GitHub...${NC}"
git push -u origin main

echo -e "${GREEN}Erstelle Release v1.0.0...${NC}"
git tag -a v1.0.0 -m "Erste Version der Soyosource Controller Integration"
git push origin v1.0.0

echo -e "${GREEN}Fertig! Repository wurde erfolgreich auf GitHub veröffentlicht.${NC}"
echo -e "${GREEN}Besuchen Sie https://github.com/$1/ha-soyosource${NC}" 