#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculateur Acoustique Interactif - Version Universelle
Saisie personnalisée des données via terminal
Génération de rapport PDF professionnel sur 2 pages
"""

import math
import sys
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

class CalculateurAcoustiqueInteractif:
    def __init__(self):
        self.data = {}
        self.date_etude = datetime.now().strftime("%d/%m/%Y")
        
    def saisir_donnees_projet(self):
        """Saisie interactive des données du projet"""
        print("\n" + "="*70)
        print("🔊 CALCULATEUR ACOUSTIQUE INTERACTIF")
        print("="*70)
        print("📝 Veuillez saisir les informations de votre projet acoustique")
        print("="*70)
        
        # Informations générales du projet
        print("\n📋 INFORMATIONS GENERALES DU PROJET")
        print("-" * 50)
        
        self.data['nom_projet'] = input("Nom du projet : ").strip()
        if not self.data['nom_projet']:
            self.data['nom_projet'] = "Projet Acoustique"
            
        self.data['localisation'] = input("Localisation (ville, canton, pays) : ").strip()
        if not self.data['localisation']:
            self.data['localisation'] = "Non spécifié"
            
        self.data['equipement'] = input("Équipement étudié (modèle complet) : ").strip()
        if not self.data['equipement']:
            self.data['equipement'] = "Équipement non spécifié"
            
        # Zone de sensibilité
        print("\n🏘️ ZONE DE SENSIBILITE")
        print("-" * 30)
        print("Zones disponibles :")
        print("1. DS I  - Zone de silence (hôpitaux, écoles)")
        print("2. DS II - Zone d'habitation mixte")
        print("3. DS III- Zone d'habitation et artisanat")
        print("4. DS IV - Zone industrielle")
        
        while True:
            try:
                choix_ds = input("\nChoisissez le degré de sensibilité (1-4) : ").strip()
                if choix_ds == "1":
                    self.data['zone_sensibilite'] = "DS I (Zone de silence)"
                    self.data['limite_jour'] = 45.0
                    self.data['limite_nuit'] = 35.0
                    break
                elif choix_ds == "2":
                    self.data['zone_sensibilite'] = "DS II (Zone d'habitation)"
                    self.data['limite_jour'] = 55.0
                    self.data['limite_nuit'] = 45.0
                    break
                elif choix_ds == "3":
                    self.data['zone_sensibilite'] = "DS III (Zone mixte)"
                    self.data['limite_jour'] = 60.0
                    self.data['limite_nuit'] = 50.0
                    break
                elif choix_ds == "4":
                    self.data['zone_sensibilite'] = "DS IV (Zone industrielle)"
                    self.data['limite_jour'] = 65.0
                    self.data['limite_nuit'] = 55.0
                    break
                else:
                    print("❌ Choix invalide. Veuillez entrer 1, 2, 3 ou 4.")
            except:
                print("❌ Erreur de saisie. Veuillez recommencer.")
        
        print(f"✅ Zone sélectionnée : {self.data['zone_sensibilite']}")
        print(f"   Limites : Jour {self.data['limite_jour']:.0f} dB(A) / Nuit {self.data['limite_nuit']:.0f} dB(A)")
        
        # Option pour personnaliser les limites
        personnaliser = input("\nSouhaitez-vous personnaliser les limites réglementaires ? (o/n) : ").strip().lower()
        if personnaliser in ['o', 'oui', 'y', 'yes']:
            try:
                self.data['limite_jour'] = float(input(f"Limite jour (actuellement {self.data['limite_jour']:.0f} dB(A)) : "))
                self.data['limite_nuit'] = float(input(f"Limite nuit (actuellement {self.data['limite_nuit']:.0f} dB(A)) : "))
                print(f"✅ Nouvelles limites : Jour {self.data['limite_jour']:.0f} dB(A) / Nuit {self.data['limite_nuit']:.0f} dB(A)")
            except:
                print("⚠️ Valeurs invalides, conservation des limites par défaut")
    
    def saisir_parametres_techniques(self):
        """Saisie des paramètres techniques de l'équipement"""
        print("\n🔧 PARAMETRES TECHNIQUES DE L'EQUIPEMENT")
        print("-" * 50)
        
        while True:
            try:
                self.data['lp1'] = float(input("Niveau de pression sonore Lp1 (dB(A)) : "))
                if 0 <= self.data['lp1'] <= 120:
                    break
                else:
                    print("❌ Valeur invalide. Le niveau sonore doit être entre 0 et 120 dB(A).")
            except:
                print("❌ Veuillez entrer une valeur numérique valide.")
        
        while True:
            try:
                self.data['distance_ref'] = float(input("Distance de référence pour Lp1 (mètres) : "))
                if self.data['distance_ref'] > 0:
                    break
                else:
                    print("❌ La distance doit être positive.")
            except:
                print("❌ Veuillez entrer une valeur numérique valide.")
        
        while True:
            try:
                self.data['distance_cible'] = float(input("Distance à la fenêtre la plus proche (mètres) : "))
                if self.data['distance_cible'] > 0:
                    break
                else:
                    print("❌ La distance doit être positive.")
            except:
                print("❌ Veuillez entrer une valeur numérique valide.")
        
        # Paramètres optionnels
        try:
            puissance_sonore = input("Niveau de puissance sonore (dB(A)) [Optionnel, Entrée pour ignorer] : ").strip()
            self.data['puissance_sonore'] = float(puissance_sonore) if puissance_sonore else None
        except:
            self.data['puissance_sonore'] = None
            
        try:
            puissance_frigo = input("Puissance frigorifique (kW) [Optionnel, Entrée pour ignorer] : ").strip()
            self.data['puissance_frigorifique'] = float(puissance_frigo) if puissance_frigo else None
        except:
            self.data['puissance_frigorifique'] = None
    
    def saisir_facteurs_correction(self):
        """Saisie des facteurs de correction OPB"""
        print("\n⚙️ FACTEURS DE CORRECTION SELON L'OPB")
        print("-" * 50)
        print("💡 Conseil : Laissez vide pour utiliser les valeurs par défaut")
        
        # K1 - Correction temporelle
        print("\n🕐 Facteur K1 - Correction temporelle")
        try:
            k1_jour_input = input("K1 jour (dB(A)) [défaut: 5] : ").strip()
            self.data['k1_jour'] = float(k1_jour_input) if k1_jour_input else 5.0
        except:
            self.data['k1_jour'] = 5.0
            
        try:
            k1_nuit_input = input("K1 nuit (dB(A)) [défaut: 10] : ").strip()
            self.data['k1_nuit'] = float(k1_nuit_input) if k1_nuit_input else 10.0
        except:
            self.data['k1_nuit'] = 10.0
        
        # K2 - Composante tonale
        print("\n🎵 Facteur K2 - Composante tonale")
        print("0 = Pas de composante tonale")
        print("4 = Composante tonale audible")
        print("6 = Composante tonale très marquée")
        try:
            k2_input = input("K2 (dB(A)) [défaut: 4] : ").strip()
            self.data['k2'] = float(k2_input) if k2_input else 4.0
        except:
            self.data['k2'] = 4.0
        
        # K3 - Composante impulsive
        print("\n⚡ Facteur K3 - Composante impulsive")
        print("0 = Pas de composante impulsive")
        print("5 = Composante impulsive audible")
        try:
            k3_input = input("K3 (dB(A)) [défaut: 0] : ").strip()
            self.data['k3'] = float(k3_input) if k3_input else 0.0
        except:
            self.data['k3'] = 0.0
        
        # Correction de réflexion
        print("\n🏢 Correction de réflexion")
        print("0 = Terrain libre")
        print("1 = Réflexion sur une surface")
        print("3 = Réflexion en angle (coin de bâtiment)")
        try:
            reflexion_input = input("Correction réflexion (dB(A)) [défaut: 1] : ").strip()
            self.data['reflexion'] = float(reflexion_input) if reflexion_input else 1.0
        except:
            self.data['reflexion'] = 1.0
    
    def afficher_resume_donnees(self):
        """Affiche un résumé des données saisies pour validation"""
        print("\n" + "="*70)
        print("📋 RESUME DES DONNEES SAISIES")
        print("="*70)
        
        print(f"📍 Projet : {self.data['nom_projet']}")
        print(f"📍 Localisation : {self.data['localisation']}")
        print(f"🏭 Équipement : {self.data['equipement']}")
        print(f"🏘️ Zone de sensibilité : {self.data['zone_sensibilite']}")
        print(f"⚖️ Limites : Jour {self.data['limite_jour']:.0f} dB(A) / Nuit {self.data['limite_nuit']:.0f} dB(A)")
        
        print(f"\n🔧 Paramètres techniques :")
        print(f"   • Lp1 : {self.data['lp1']:.1f} dB(A) à {self.data['distance_ref']:.0f}m")
        print(f"   • Distance fenêtre : {self.data['distance_cible']:.0f}m")
        if self.data['puissance_sonore']:
            print(f"   • Puissance sonore : {self.data['puissance_sonore']:.1f} dB(A)")
        if self.data['puissance_frigorifique']:
            print(f"   • Puissance frigorifique : {self.data['puissance_frigorifique']:.1f} kW")
        
        print(f"\n⚙️ Facteurs de correction :")
        print(f"   • K1 jour : {self.data['k1_jour']:.0f} dB(A)")
        print(f"   • K1 nuit : {self.data['k1_nuit']:.0f} dB(A)")
        print(f"   • K2 (tonale) : {self.data['k2']:.0f} dB(A)")
        print(f"   • K3 (impulsive) : {self.data['k3']:.0f} dB(A)")
        print(f"   • Réflexion : {self.data['reflexion']:.0f} dB(A)")
        
        print("="*70)
        
        while True:
            confirmation = input("\n✅ Ces données sont-elles correctes ? (o/n/m pour modifier) : ").strip().lower()
            if confirmation in ['o', 'oui', 'y', 'yes']:
                return True
            elif confirmation in ['n', 'non', 'no']:
                return False
            elif confirmation in ['m', 'modifier', 'mod']:
                self.modifier_donnees()
                return True
            else:
                print("❌ Veuillez répondre par 'o' (oui), 'n' (non) ou 'm' (modifier)")
    
    def modifier_donnees(self):
        """Permet de modifier des données spécifiques"""
        print("\n🔧 MODIFICATION DES DONNEES")
        print("-" * 30)
        print("Que souhaitez-vous modifier ?")
        print("1. Informations du projet")
        print("2. Paramètres techniques")
        print("3. Facteurs de correction")
        print("4. Zone de sensibilité")
        
        choix = input("Votre choix (1-4) : ").strip()
        
        if choix == "1":
            self.saisir_donnees_projet()
        elif choix == "2":
            self.saisir_parametres_techniques()
        elif choix == "3":
            self.saisir_facteurs_correction()
        elif choix == "4":
            # Re-saisie zone de sensibilité seulement
            print("\n🏘️ ZONE DE SENSIBILITE")
            print("1. DS I - Zone de silence")
            print("2. DS II - Zone d'habitation")
            print("3. DS III - Zone mixte")
            print("4. DS IV - Zone industrielle")
            
            choix_ds = input("Nouveau choix (1-4) : ").strip()
            if choix_ds == "1":
                self.data['zone_sensibilite'] = "DS I (Zone de silence)"
                self.data['limite_jour'] = 45.0
                self.data['limite_nuit'] = 35.0
            elif choix_ds == "2":
                self.data['zone_sensibilite'] = "DS II (Zone d'habitation)"
                self.data['limite_jour'] = 55.0
                self.data['limite_nuit'] = 45.0
            elif choix_ds == "3":
                self.data['zone_sensibilite'] = "DS III (Zone mixte)"
                self.data['limite_jour'] = 60.0
                self.data['limite_nuit'] = 50.0
            elif choix_ds == "4":
                self.data['zone_sensibilite'] = "DS IV (Zone industrielle)"
                self.data['limite_jour'] = 65.0
                self.data['limite_nuit'] = 55.0
        else:
            print("❌ Choix invalide")
    
    def effectuer_calculs(self):
        """Effectue les calculs acoustiques avec les données saisies"""
        print("\n🧮 CALCULS EN COURS...")
        
        # Calcul de l'atténuation
        attenuation = 20 * math.log10(self.data['distance_ref'] / self.data['distance_cible'])
        
        # Calcul du niveau de pression sonore à la distance cible
        lpx = self.data['lp1'] + attenuation
        
        # Calcul des niveaux d'évaluation
        lr_jour = lpx + self.data['k1_jour'] + self.data['k2'] + self.data['k3'] + self.data['reflexion']
        lr_nuit = lpx + self.data['k1_nuit'] + self.data['k2'] + self.data['k3'] + self.data['reflexion']
        
        # Évaluation de conformité
        conforme_jour = lr_jour <= self.data['limite_jour']
        conforme_nuit = lr_nuit <= self.data['limite_nuit']
        
        resultats = {
            'attenuation': attenuation,
            'lpx': lpx,
            'lr_jour': lr_jour,
            'lr_nuit': lr_nuit,
            'limite_jour': self.data['limite_jour'],
            'limite_nuit': self.data['limite_nuit'],
            'conforme_jour': conforme_jour,
            'conforme_nuit': conforme_nuit,
            'parametres': self.data.copy()
        }
        
        return resultats
    
    def afficher_resultats(self, resultats):
        """Affiche les résultats des calculs"""
        print("\n" + "="*70)
        print("📊 RESULTATS DE L'ETUDE ACOUSTIQUE")
        print("="*70)
        
        print(f"\n🧮 CALCULS ACOUSTIQUES :")
        print(f"   • Atténuation due à la distance : {resultats['attenuation']:.2f} dB(A)")
        print(f"   • Niveau de pression à {self.data['distance_cible']:.0f}m : {resultats['lpx']:.2f} dB(A)")
        
        print(f"\n📈 NIVEAUX D'EVALUATION (Lr) :")
        print(f"   • Période jour (07h-22h) : {resultats['lr_jour']:.1f} dB(A)")
        print(f"   • Période nuit (22h-07h) : {resultats['lr_nuit']:.1f} dB(A)")
        
        print(f"\n⚖️ CONFORMITE {self.data['zone_sensibilite']} :")
        statut_jour = "✅ CONFORME" if resultats['conforme_jour'] else "❌ NON CONFORME"
        statut_nuit = "✅ CONFORME" if resultats['conforme_nuit'] else "❌ NON CONFORME"
        
        print(f"   • Jour : {resultats['lr_jour']:.1f} dB(A) / {resultats['limite_jour']:.0f} dB(A) → {statut_jour}")
        print(f"   • Nuit : {resultats['lr_nuit']:.1f} dB(A) / {resultats['limite_nuit']:.0f} dB(A) → {statut_nuit}")
        
        print("\n" + "="*70)
        if resultats['conforme_jour'] and resultats['conforme_nuit']:
            print("🎉 CONCLUSION : Installation conforme aux normes OPB")
        else:
            print("⚠️  CONCLUSION : Mesures d'atténuation nécessaires")
        print("="*70)
    
    def generer_pdf_interactif(self, resultats):
        """Génère le rapport PDF avec les données personnalisées"""
        nom_fichier = f"rapport_acoustique_{self.data['nom_projet'].replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        
        try:
            doc = SimpleDocTemplate(
                nom_fichier, pagesize=A4,
                rightMargin=2*cm, leftMargin=2*cm,
                topMargin=2.5*cm, bottomMargin=2*cm
            )
            
            styles = getSampleStyleSheet()
            
            # Styles
            style_titre = ParagraphStyle(
                'TitrePrincipal', fontSize=16, spaceAfter=20, spaceBefore=10,
                alignment=TA_CENTER, textColor=colors.HexColor('#1f4e79'), fontName='Helvetica-Bold'
            )
            
            style_sous_titre = ParagraphStyle(
                'SousTitre', fontSize=13, spaceAfter=15, spaceBefore=8,
                alignment=TA_CENTER, textColor=colors.HexColor('#2f5f8f'), fontName='Helvetica-Bold'
            )
            
            style_section = ParagraphStyle(
                'Section', fontSize=12, spaceAfter=10, spaceBefore=15,
                textColor=colors.HexColor('#1f4e79'), fontName='Helvetica-Bold',
                borderWidth=1, borderColor=colors.HexColor('#1f4e79'),
                borderPadding=4, backColor=colors.HexColor('#f0f4f8')
            )
            
            style_normal = ParagraphStyle(
                'Normal', fontSize=10, spaceAfter=6, spaceBefore=3,
                alignment=TA_JUSTIFY, fontName='Helvetica'
            )
            
            style_formule = ParagraphStyle(
                'Formule', fontSize=10, spaceAfter=8, spaceBefore=8,
                alignment=TA_CENTER, fontName='Helvetica-Bold',
                backColor=colors.HexColor('#f8f9fa'), borderWidth=1,
                borderColor=colors.HexColor('#dee2e6'), borderPadding=6
            )
            
            story = []
            
            # Page 1
            story.append(Paragraph("ETUDE ACOUSTIQUE ENVIRONNEMENTALE", style_titre))
            story.append(Paragraph(self.data['nom_projet'], style_sous_titre))
            story.append(Paragraph(self.data['localisation'], style_sous_titre))
            story.append(Spacer(1, 20))
            
            # Informations du projet
            info_data = [
                ['Projet :', self.data['nom_projet']],
                ['Localisation :', self.data['localisation']],
                ['Equipement etudie :', self.data['equipement']],
                ['Date de l\'etude :', self.date_etude],
                ['Reglementation :', 'Ordonnance sur la Protection contre le Bruit (OPB)'],
                ['Degre de sensibilite :', self.data['zone_sensibilite']]
            ]
            
            info_table = Table(info_data, colWidths=[5*cm, 10*cm])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0fe')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#1f4e79')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            story.append(info_table)
            story.append(Spacer(1, 20))
            
            # Paramètres techniques
            story.append(Paragraph("1. PARAMETRES TECHNIQUES DE L'EQUIPEMENT", style_section))
            story.append(Spacer(1, 8))
            
            tech_data = [
                ['Parametre', 'Valeur', 'Unite'],
                ['Niveau de pression sonore (Lp1)', f"{self.data['lp1']:.1f}", f"dB(A) a {self.data['distance_ref']:.0f}m"],
            ]
            
            if self.data['puissance_sonore']:
                tech_data.append(['Niveau de puissance sonore', f"{self.data['puissance_sonore']:.1f}", 'dB(A)'])
            if self.data['puissance_frigorifique']:
                tech_data.append(['Puissance frigorifique', f"{self.data['puissance_frigorifique']:.1f}", 'kW'])
                
            tech_data.extend([
                ['Distance de reference', f"{self.data['distance_ref']:.0f}", 'm'],
                ['Distance a la fenetre', f"{self.data['distance_cible']:.0f}", 'm'],
            ])
            
            tech_table = Table(tech_data, colWidths=[7*cm, 4*cm, 4*cm])
            tech_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            
            story.append(tech_table)
            story.append(Spacer(1, 20))
            
            # Facteurs de correction
            story.append(Paragraph("2. FACTEURS DE CORRECTION SELON L'OPB", style_section))
            story.append(Spacer(1, 8))
            
            correction_data = [
                ['Facteur', 'Periode', 'Valeur', 'Description'],
                ['K1', 'Jour (07h-22h)', f"{self.data['k1_jour']:.0f} dB(A)", 'Correction temporelle'],
                ['K1', 'Nuit (22h-07h)', f"{self.data['k1_nuit']:.0f} dB(A)", 'Correction temporelle'],
                ['K2', 'Jour/Nuit', f"{self.data['k2']:.0f} dB(A)", 'Composante tonale'],
                ['K3', 'Jour/Nuit', f"{self.data['k3']:.0f} dB(A)", 'Composante impulsive'],
                ['Reflexion', 'Jour/Nuit', f"{self.data['reflexion']:.0f} dB(A)", 'Correction de reflexion'],
            ]
            
            correction_table = Table(correction_data, colWidths=[2.5*cm, 4*cm, 3*cm, 5.5*cm])
            correction_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            
            story.append(correction_table)
            story.append(PageBreak())
            
            # Page 2
            story.append(Paragraph("3. CALCULS ACOUSTIQUES", style_section))
            story.append(Spacer(1, 10))
            
            story.append(Paragraph("3.1 Attenuation due a la distance", 
                                 ParagraphStyle('Heading3', parent=styles['Heading2'], fontSize=11, spaceAfter=6)))
            
            formule_text = f"Attenuation = 20 x log10(d1/d2)"
            story.append(Paragraph(f"Formule : {formule_text}", style_formule))
            
            calcul_text = f"Calcul : 20 x log10({self.data['distance_ref']:.0f}/{self.data['distance_cible']:.0f}) = {resultats['attenuation']:.2f} dB(A)"
            story.append(Paragraph(calcul_text, style_normal))
            story.append(Spacer(1, 12))
            
            story.append(Paragraph("3.2 Niveau de pression sonore a la distance cible", 
                                 ParagraphStyle('Heading3', parent=styles['Heading2'], fontSize=11, spaceAfter=6)))
            
            lpx_text = f"Lpx = Lp1 + Attenuation = {self.data['lp1']:.1f} + ({resultats['attenuation']:.2f}) = {resultats['lpx']:.2f} dB(A)"
            story.append(Paragraph(lpx_text, style_formule))
            story.append(Spacer(1, 20))
            
            # Résultats
            story.append(Paragraph("4. NIVEAUX D'EVALUATION ET CONFORMITE", style_section))
            story.append(Spacer(1, 10))
            
            statut_jour = "CONFORME" if resultats['conforme_jour'] else "NON CONFORME"
            statut_nuit = "CONFORME" if resultats['conforme_nuit'] else "NON CONFORME"
            
            resultats_data = [
                ['Periode', 'Formule de Calcul', 'Niveau Lr', 'Limite OPB', 'Conformite'],
                [
                    'Jour\n(07h-22h)', 
                    f"Lpx + K1 + K2 + K3 + Refl.\n{resultats['lpx']:.1f} + {self.data['k1_jour']:.0f} + {self.data['k2']:.0f} + {self.data['k3']:.0f} + {self.data['reflexion']:.0f}",
                    f"{resultats['lr_jour']:.1f} dB(A)",
                    f"{resultats['limite_jour']:.0f} dB(A)",
                    statut_jour
                ],
                [
                    'Nuit\n(22h-07h)', 
                    f"Lpx + K1 + K2 + K3 + Refl.\n{resultats['lpx']:.1f} + {self.data['k1_nuit']:.0f} + {self.data['k2']:.0f} + {self.data['k3']:.0f} + {self.data['reflexion']:.0f}",
                    f"{resultats['lr_nuit']:.1f} dB(A)",
                    f"{resultats['limite_nuit']:.0f} dB(A)",
                    statut_nuit
                ]
            ]
            
            resultats_table = Table(resultats_data, colWidths=[2.5*cm, 5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
            resultats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
                ('BACKGROUND', (4, 1), (4, 1), colors.HexColor('#d4edda') if resultats['conforme_jour'] else colors.HexColor('#f8d7da')),
                ('BACKGROUND', (4, 2), (4, 2), colors.HexColor('#d4edda') if resultats['conforme_nuit'] else colors.HexColor('#f8d7da')),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            story.append(resultats_table)
            story.append(Spacer(1, 20))
            
            # Conclusion
            story.append(Paragraph("5. CONCLUSION", style_section))
            story.append(Spacer(1, 10))
            
            if resultats['conforme_jour'] and resultats['conforme_nuit']:
                conclusion_text = f"""
                INSTALLATION CONFORME aux normes OPB
                
                L'etude acoustique de l'equipement {self.data['equipement']} du projet {self.data['nom_projet']} demontre que les niveaux d'evaluation 
                respectent les valeurs limites d'immission fixees par l'Ordonnance sur la Protection contre le Bruit (OPB) 
                pour une {self.data['zone_sensibilite']}.
                
                Niveaux calcules :
                • Periode diurne : {resultats['lr_jour']:.1f} dB(A) < {resultats['limite_jour']:.0f} dB(A)
                • Periode nocturne : {resultats['lr_nuit']:.1f} dB(A) < {resultats['limite_nuit']:.0f} dB(A)
                
                Recommandations :
                • Aucune mesure d'attenuation supplementaire n'est requise
                • Validation recommandee par mesures in-situ apres installation
                • Controle periodique du bon fonctionnement de l'equipement
                """
            else:
                conclusion_text = f"""
                MESURES D'ATTENUATION NECESSAIRES
                
                L'etude acoustique revele un depassement des valeurs limites d'immission pour la {self.data['zone_sensibilite']}. 
                Des mesures d'attenuation doivent etre mises en place avant la mise en service de l'installation.
                """
            
            story.append(Paragraph(conclusion_text, style_normal))
            story.append(Spacer(1, 15))
            
            # Références
            story.append(Paragraph("6. REFERENCES REGLEMENTAIRES", style_section))
            story.append(Spacer(1, 8))
            
            references_text = """
            • Ordonnance sur la Protection contre le Bruit (OPB) du 15 decembre 1986 (Etat le 1er juillet 2016)
            • Annexe 6 de l'OPB : Methodes de calcul et de mesure
            • Articles 33.1 a 33.3 : Facteurs de correction
            • Loi federale sur la protection de l'environnement (LPE)
            """
            
            story.append(Paragraph(references_text, style_normal))
            
            doc.build(story)
            
            return True, nom_fichier
            
        except Exception as e:
            return False, f"Erreur : {str(e)}"
    
    def sauvegarder_configuration(self):
        """Propose de sauvegarder la configuration pour réutilisation"""
        sauvegarder = input("\n💾 Souhaitez-vous sauvegarder cette configuration pour un usage futur ? (o/n) : ").strip().lower()
        
        if sauvegarder in ['o', 'oui', 'y', 'yes']:
            try:
                nom_config = input("Nom du fichier de configuration (sans extension) : ").strip()
                if not nom_config:
                    nom_config = f"config_{self.data['nom_projet'].replace(' ', '_').lower()}"
                
                nom_fichier_config = f"{nom_config}.txt"
                
                with open(nom_fichier_config, 'w', encoding='utf-8') as f:
                    f.write("# Configuration Calculateur Acoustique\n")
                    f.write(f"# Créée le {self.date_etude}\n\n")
                    
                    for cle, valeur in self.data.items():
                        f.write(f"{cle} = {valeur}\n")
                
                print(f"✅ Configuration sauvegardée dans : {nom_fichier_config}")
                print("💡 Vous pourrez modifier ce fichier texte et le charger lors d'une prochaine utilisation")
                
            except Exception as e:
                print(f"❌ Erreur lors de la sauvegarde : {e}")

def main():
    """Fonction principale interactive"""
    calculateur = CalculateurAcoustiqueInteractif()
    
    print("🚀 Bienvenue dans le Calculateur Acoustique Interactif")
    print("📋 Cet outil va vous guider pour réaliser votre étude acoustique")
    
    try:
        # Processus de saisie des données
        calculateur.saisir_donnees_projet()
        calculateur.saisir_parametres_techniques()
        calculateur.saisir_facteurs_correction()
        
        # Validation des données
        while not calculateur.afficher_resume_donnees():
            print("\n🔄 Reprise de la saisie des données...")
            calculateur.saisir_donnees_projet()
            calculateur.saisir_parametres_techniques()
            calculateur.saisir_facteurs_correction()
        
        # Calculs
        resultats = calculateur.effectuer_calculs()
        calculateur.afficher_resultats(resultats)
        
        # Génération du PDF
        generer_pdf = input("\n📄 Souhaitez-vous générer le rapport PDF ? (o/n) : ").strip().lower()
        if generer_pdf in ['o', 'oui', 'y', 'yes']:
            print("\n📄 Génération du rapport PDF en cours...")
            succes, nom_fichier = calculateur.generer_pdf_interactif(resultats)
            
            if succes:
                print(f"✅ Rapport PDF généré avec succès : {nom_fichier}")
                print("📏 Format professionnel sur 2 pages")
            else:
                print(f"❌ {nom_fichier}")
        
        # Sauvegarde de la configuration
        calculateur.sauvegarder_configuration()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Processus interrompu par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
        sys.exit(1)
    
    print("\n🎉 Merci d'avoir utilisé le Calculateur Acoustique Interactif !")
    print("\nAppuyez sur Entrée pour fermer...")
    input()

if __name__ == "__main__":
    main()
