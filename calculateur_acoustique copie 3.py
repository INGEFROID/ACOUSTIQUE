#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculateur Acoustique Complet - Hôtel L'Uciole (Crans-Montana)
Étude acoustique du condenseur LU-VE LMC6S-3526 H EC
Calculs selon l'Ordonnance sur la Protection contre le Bruit (OPB) - Suisse
Version finale corrigée
"""

import math
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

class CalculateurAcoustiqueComplet:
    def __init__(self):
        self.nom_projet = "Hôtel L'Uciole (ancien Mirabeau)"
        self.lieu = "Crans-Montana, Valais, Suisse"
        self.equipement = "Condenseur LU-VE LMC6S-3526 H EC (1X2)"
        self.date_etude = datetime.now().strftime("%d/%m/%Y")
        self.ingenieur = "Étude Acoustique Environnementale"
        
    def calculer_attenuation(self, distance_ref, distance_cible):
        """Calcul de l'atténuation selon la formule OPB"""
        return 20 * math.log10(distance_ref / distance_cible)
    
    def calculer_lpx(self, lp1, attenuation):
        """Calcul du niveau de pression sonore à la distance cible"""
        return lp1 + attenuation
    
    def calculer_lr(self, lpx, k1, k2, k3, reflexion):
        """Calcul du niveau d'évaluation selon l'OPB"""
        return lpx + k1 + k2 + k3 + reflexion
    
    def effectuer_calculs(self):
        """Effectue tous les calculs acoustiques"""
        # Paramètres du condenseur LU-VE LMC6S-3526 H EC
        lp1 = 31.0  # dB(A) à 10 mètres
        puissance_sonore = 63.0  # dB(A)
        puissance_frigorifique = 21.0  # kW
        distance_ref = 10.0  # mètres
        distance_cible = 18.0  # mètres à la fenêtre
        
        # Facteurs de correction OPB (selon vos calculs originaux)
        k1_jour = 5.0  # dB(A) - correction temporelle jour
        k1_nuit = 10.0  # dB(A) - correction temporelle nuit
        k2 = 4.0  # dB(A) - composante tonale
        k3 = 0.0  # dB(A) - composante impulsive
        reflexion = 1.0  # dB(A) - correction de réflexion
        
        # Calculs
        attenuation = self.calculer_attenuation(distance_ref, distance_cible)
        lpx = self.calculer_lpx(lp1, attenuation)
        lr_jour = self.calculer_lr(lpx, k1_jour, k2, k3, reflexion)
        lr_nuit = self.calculer_lr(lpx, k1_nuit, k2, k3, reflexion)
        
        # Limites réglementaires DS II (vos valeurs corrigées)
        limite_jour = 50.0  # dB(A) - 07h00 à 22h00
        limite_nuit = 45.0  # dB(A) - 22h00 à 07h00
        
        # Évaluation de conformité
        conforme_jour = lr_jour <= limite_jour
        conforme_nuit = lr_nuit <= limite_nuit
        
        return {
            'attenuation': attenuation,
            'lpx': lpx,
            'lr_jour': lr_jour,
            'lr_nuit': lr_nuit,
            'limite_jour': limite_jour,
            'limite_nuit': limite_nuit,
            'conforme_jour': conforme_jour,
            'conforme_nuit': conforme_nuit,
            'parametres': {
                'lp1': lp1,
                'puissance_sonore': puissance_sonore,
                'puissance_frigorifique': puissance_frigorifique,
                'distance_ref': distance_ref,
                'distance_cible': distance_cible,
                'k1_jour': k1_jour,
                'k1_nuit': k1_nuit,
                'k2': k2,
                'k3': k3,
                'reflexion': reflexion
            }
        }
    
    def generer_pdf(self, resultats, nom_fichier="rapport_acoustique_uciole_final.pdf"):
        """Génère le rapport PDF complet"""
        try:
            # Configuration du document
            doc = SimpleDocTemplate(
                nom_fichier,
                pagesize=A4,
                rightMargin=2.5*cm,
                leftMargin=2.5*cm,
                topMargin=3*cm,
                bottomMargin=2.5*cm
            )
            
            # Styles
            styles = getSampleStyleSheet()
            
            # Styles personnalisés
            style_titre = ParagraphStyle(
                'TitrePrincipal',
                parent=styles['Title'],
                fontSize=18,
                spaceAfter=25,
                spaceBefore=10,
                alignment=TA_CENTER,
                textColor=colors.darkblue,
                fontName='Helvetica-Bold'
            )
            
            style_sous_titre = ParagraphStyle(
                'SousTitre',
                parent=styles['Heading1'],
                fontSize=14,
                spaceAfter=12,
                spaceBefore=8,
                alignment=TA_CENTER,
                textColor=colors.darkblue,
                fontName='Helvetica-Bold'
            )
            
            style_section = ParagraphStyle(
                'Section',
                parent=styles['Heading1'],
                fontSize=13,
                spaceAfter=12,
                spaceBefore=18,
                textColor=colors.darkblue,
                fontName='Helvetica-Bold'
            )
            
            style_normal = ParagraphStyle(
                'Normal',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=6,
                spaceBefore=3,
                alignment=TA_JUSTIFY,
                fontName='Helvetica'
            )
            
            style_formule = ParagraphStyle(
                'Formule',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=8,
                spaceBefore=8,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold',
                backColor=colors.lightgrey,
                borderWidth=1,
                borderColor=colors.grey,
                borderPadding=6
            )
            
            # Contenu du document
            story = []
            
            # En-tête
            story.append(Spacer(1, 15))
            story.append(Paragraph("ETUDE ACOUSTIQUE ENVIRONNEMENTALE", style_titre))
            story.append(Spacer(1, 8))
            story.append(Paragraph(self.nom_projet, style_sous_titre))
            story.append(Paragraph(self.lieu, style_sous_titre))
            story.append(Spacer(1, 25))
            
            # Informations du projet
            info_data = [
                ['Projet :', self.nom_projet],
                ['Localisation :', self.lieu],
                ['Equipement etudie :', self.equipement],
                ['Date de l\'etude :', self.date_etude],
                ['Reglementation :', 'Ordonnance sur la Protection contre le Bruit (OPB)'],
                ['Degre de sensibilite :', 'DS II (Zone d\'habitation)']
            ]
            
            info_table = Table(info_data, colWidths=[5.5*cm, 9.5*cm])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            story.append(info_table)
            story.append(Spacer(1, 25))
            
            # Section 1 : Paramètres techniques
            story.append(Paragraph("1. PARAMETRES TECHNIQUES DE L'EQUIPEMENT", style_section))
            story.append(Spacer(1, 8))
            
            tech_data = [
                ['Parametre', 'Valeur', 'Unite'],
                ['Niveau de pression sonore (Lp1)', f"{resultats['parametres']['lp1']:.1f}", 'dB(A) a 10m'],
                ['Niveau de puissance sonore', f"{resultats['parametres']['puissance_sonore']:.1f}", 'dB(A)'],
                ['Puissance frigorifique', f"{resultats['parametres']['puissance_frigorifique']:.1f}", 'kW'],
                ['Distance de reference', f"{resultats['parametres']['distance_ref']:.0f}", 'm'],
                ['Distance a la fenetre', f"{resultats['parametres']['distance_cible']:.0f}", 'm'],
            ]
            
            tech_table = Table(tech_data, colWidths=[7*cm, 4*cm, 4*cm])
            tech_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            
            story.append(tech_table)
            story.append(Spacer(1, 18))
            
            # Section 2 : Facteurs de correction
            story.append(Paragraph("2. FACTEURS DE CORRECTION SELON L'OPB", style_section))
            story.append(Spacer(1, 8))
            
            correction_data = [
                ['Facteur', 'Periode', 'Valeur', 'Description'],
                ['K1', 'Jour (07h-22h)', f"{resultats['parametres']['k1_jour']:.0f} dB(A)", 'Correction temporelle'],
                ['K1', 'Nuit (22h-07h)', f"{resultats['parametres']['k1_nuit']:.0f} dB(A)", 'Correction temporelle'],
                ['K2', 'Jour/Nuit', f"{resultats['parametres']['k2']:.0f} dB(A)", 'Composante tonale'],
                ['K3', 'Jour/Nuit', f"{resultats['parametres']['k3']:.0f} dB(A)", 'Composante impulsive'],
                ['Reflexion', 'Jour/Nuit', f"{resultats['parametres']['reflexion']:.0f} dB(A)", 'Correction de reflexion'],
            ]
            
            correction_table = Table(correction_data, colWidths=[2.5*cm, 4*cm, 3*cm, 5.5*cm])
            correction_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            
            story.append(correction_table)
            story.append(Spacer(1, 18))
            
            # Section 3 : Calculs acoustiques
            story.append(Paragraph("3. CALCULS ACOUSTIQUES", style_section))
            story.append(Spacer(1, 8))
            
            story.append(Paragraph("3.1 Attenuation due a la distance", ParagraphStyle('Heading3', parent=styles['Heading2'], fontSize=12, spaceAfter=6)))
            
            # Formule correctement formatée
            formule_text = f"Attenuation = 20 x log10(d1/d2)"
            story.append(Paragraph(f"Formule : {formule_text}", style_formule))
            
            calcul_text = f"Calcul : 20 x log10({resultats['parametres']['distance_ref']:.0f}/{resultats['parametres']['distance_cible']:.0f}) = {resultats['attenuation']:.2f} dB(A)"
            story.append(Paragraph(calcul_text, style_normal))
            story.append(Spacer(1, 12))
            
            story.append(Paragraph("3.2 Niveau de pression sonore a la distance cible", ParagraphStyle('Heading3', parent=styles['Heading2'], fontSize=12, spaceAfter=6)))
            
            lpx_text = f"Lpx = Lp1 + Attenuation = {resultats['parametres']['lp1']:.1f} + ({resultats['attenuation']:.2f}) = {resultats['lpx']:.2f} dB(A)"
            story.append(Paragraph(lpx_text, style_formule))
            story.append(Spacer(1, 18))
            
            # Section 4 : Résultats
            story.append(Paragraph("4. NIVEAUX D'EVALUATION ET CONFORMITE", style_section))
            story.append(Spacer(1, 8))
            
            # Détermination des statuts de conformité
            statut_jour = "CONFORME" if resultats['conforme_jour'] else "NON CONFORME"
            statut_nuit = "CONFORME" if resultats['conforme_nuit'] else "NON CONFORME"
            
            resultats_data = [
                ['Periode', 'Formule de Calcul', 'Niveau Lr', 'Limite OPB', 'Conformite'],
                [
                    'Jour (07h-22h)', 
                    f"Lpx + K1 + K2 + K3 + Refl.\n{resultats['lpx']:.1f} + {resultats['parametres']['k1_jour']:.0f} + {resultats['parametres']['k2']:.0f} + {resultats['parametres']['k3']:.0f} + {resultats['parametres']['reflexion']:.0f}",
                    f"{resultats['lr_jour']:.1f} dB(A)",
                    f"{resultats['limite_jour']:.0f} dB(A)",
                    statut_jour
                ],
                [
                    'Nuit (22h-07h)', 
                    f"Lpx + K1 + K2 + K3 + Refl.\n{resultats['lpx']:.1f} + {resultats['parametres']['k1_nuit']:.0f} + {resultats['parametres']['k2']:.0f} + {resultats['parametres']['k3']:.0f} + {resultats['parametres']['reflexion']:.0f}",
                    f"{resultats['lr_nuit']:.1f} dB(A)",
                    f"{resultats['limite_nuit']:.0f} dB(A)",
                    statut_nuit
                ]
            ]
            
            resultats_table = Table(resultats_data, colWidths=[2.5*cm, 5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
            resultats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                # Coloration des cellules de conformité
                ('BACKGROUND', (4, 1), (4, 1), colors.lightgreen if resultats['conforme_jour'] else colors.pink),
                ('BACKGROUND', (4, 2), (4, 2), colors.lightgreen if resultats['conforme_nuit'] else colors.pink),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            story.append(resultats_table)
            story.append(Spacer(1, 18))
            
            # Section 5 : Conclusion
            story.append(Paragraph("5. CONCLUSION", style_section))
            story.append(Spacer(1, 8))
            
            if resultats['conforme_jour'] and resultats['conforme_nuit']:
                conclusion_text = f"""INSTALLATION CONFORME
                
                L'etude acoustique du condenseur LU-VE LMC6S-3526 H EC de l'Hotel L'Uciole demontre que les niveaux d'evaluation 
                respectent les valeurs limites d'immission fixees par l'Ordonnance sur la Protection contre le Bruit (OPB) 
                pour une zone de degre de sensibilite II.
                
                Niveaux calcules :
                • Periode diurne : {resultats['lr_jour']:.1f} dB(A) < {resultats['limite_jour']:.0f} dB(A)
                • Periode nocturne : {resultats['lr_nuit']:.1f} dB(A) < {resultats['limite_nuit']:.0f} dB(A)
                
                Recommandations :
                • Aucune mesure d'attenuation supplementaire n'est requise
                • Validation recommandee par mesures in-situ apres installation
                • Controle periodique du bon fonctionnement de l'equipement
                """
            else:
                conclusion_text = """MESURES D'ATTENUATION NECESSAIRES
                
                L'etude acoustique revele un depassement des valeurs limites d'immission. Des mesures d'attenuation 
                doivent etre mises en place avant la mise en service de l'installation."""
            
            story.append(Paragraph(conclusion_text, style_normal))
            story.append(Spacer(1, 18))
            
            # Section 6 : Références
            story.append(Paragraph("6. REFERENCES REGLEMENTAIRES", style_section))
            story.append(Spacer(1, 8))
            
            references_text = """• Ordonnance sur la Protection contre le Bruit (OPB) du 15 decembre 1986 (Etat le 1er juillet 2016)
            • Annexe 6 de l'OPB : Methodes de calcul et de mesure
            • Articles 33.1 a 33.3 : Facteurs de correction
            • Loi federale sur la protection de l'environnement (LPE)"""
            
            story.append(Paragraph(references_text, style_normal))
            
            # Construction du PDF
            doc.build(story)
            
            return True, f"Rapport PDF genere avec succes : {nom_fichier}"
            
        except Exception as e:
            return False, f"Erreur lors de la generation du PDF : {str(e)}"
    
    def afficher_resultats(self, resultats):
        """Affiche les résultats dans le terminal"""
        print("\n" + "="*60)
        print(f"🔊 ÉTUDE ACOUSTIQUE - {self.nom_projet}")
        print("="*60)
        print(f"📍 Lieu: {self.lieu}")
        print(f"🏭 Équipement: {self.equipement}")
        print(f"📅 Date: {self.date_etude}")
        print("="*60)
        
        print("\n📊 PARAMÈTRES TECHNIQUES:")
        print(f"• Niveau de pression sonore (Lp1): {resultats['parametres']['lp1']:.1f} dB(A) à {resultats['parametres']['distance_ref']:.0f}m")
        print(f"• Distance à la fenêtre: {resultats['parametres']['distance_cible']:.0f} mètres")
        print(f"• Facteur K1 jour: {resultats['parametres']['k1_jour']:.0f} dB(A)")
        print(f"• Facteur K1 nuit: {resultats['parametres']['k1_nuit']:.0f} dB(A)")
        print(f"• Facteur K2 (tonale): {resultats['parametres']['k2']:.0f} dB(A)")
        print(f"• Facteur K3 (impulsive): {resultats['parametres']['k3']:.0f} dB(A)")
        print(f"• Correction réflexion: {resultats['parametres']['reflexion']:.0f} dB(A)")
        
        print("\n🧮 CALCULS ACOUSTIQUES:")
        print(f"• Atténuation (distance): {resultats['attenuation']:.2f} dB(A)")
        print(f"• Niveau à 18m (Lpx): {resultats['lpx']:.2f} dB(A)")
        
        print("\n📈 NIVEAUX D'ÉVALUATION (Lr):")
        print(f"• Jour (07h-22h): {resultats['lr_jour']:.1f} dB(A)")
        print(f"• Nuit (22h-07h): {resultats['lr_nuit']:.1f} dB(A)")
        
        print("\n⚖️ CONFORMITÉ RÉGLEMENTAIRE (DS II):")
        statut_jour = "✅ CONFORME" if resultats['conforme_jour'] else "❌ NON CONFORME"
        statut_nuit = "✅ CONFORME" if resultats['conforme_nuit'] else "❌ NON CONFORME"
        
        print(f"• Jour: {resultats['lr_jour']:.1f} dB(A) / {resultats['limite_jour']:.0f} dB(A) → {statut_jour}")
        print(f"• Nuit: {resultats['lr_nuit']:.1f} dB(A) / {resultats['limite_nuit']:.0f} dB(A) → {statut_nuit}")
        
        print("\n" + "="*60)
        if resultats['conforme_jour'] and resultats['conforme_nuit']:
            print("🎉 CONCLUSION: Installation conforme aux normes OPB")
        else:
            print("⚠️  CONCLUSION: Mesures d'atténuation nécessaires")
        print("="*60)

def main():
    """Fonction principale"""
    print("🚀 Lancement du calculateur acoustique complet...")
    print("📍 Projet: Hôtel L'Uciole, Crans-Montana")
    print("")
    
    calculateur = CalculateurAcoustiqueComplet()
    resultats = calculateur.effectuer_calculs()
    
    # Affichage des résultats
    calculateur.afficher_resultats(resultats)
    
    # Génération du PDF
    print("\n📄 Génération du rapport PDF en cours...")
    succes, message = calculateur.generer_pdf(resultats)
    
    if succes:
        print(f"✅ {message}")
        print("📂 Le fichier PDF a été créé dans le même dossier que ce script")
    else:
        print(f"❌ {message}")
        print("💡 Vérifiez que ReportLab est installé : pip install reportlab")
    
    # Pause pour Mac
    print("\n\nAppuyez sur Entrée pour fermer...")
    input()

if __name__ == "__main__":
    main()
