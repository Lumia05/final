from typing import List, Dict
import re
from collections import Counter

class ProblemAnalyzer:
    # Dictionnaire des domaines ITIL courants et leurs mots-clés associés
    ITIL_DOMAINS = {
        'infrastructure': ['serveur', 'réseau', 'base de données', 'stockage', 'cpu', 'mémoire', 'disque', 'bande passante'],
        'application': ['bug', 'erreur', 'performance', 'crash', 'timeout', 'exception', 'code', 'application'],
        'sécurité': ['accès', 'authentification', 'mot de passe', 'permission', 'violation', 'intrusion', 'firewall'],
        'processus': ['workflow', 'procédure', 'validation', 'approbation', 'étape', 'processus'],
        'utilisateur': ['formation', 'erreur humaine', 'interface', 'expérience utilisateur', 'documentation']
    }

    # Solutions génériques par domaine
    DOMAIN_SOLUTIONS = {
        'infrastructure': [
            "Mettre en place une surveillance proactive des ressources système",
            "Implémenter des seuils d'alerte automatiques",
            "Établir un plan de capacité et de mise à l'échelle",
            "Mettre en place des systèmes redondants"
        ],
        'application': [
            "Implémenter des tests automatisés plus complets",
            "Mettre en place un système de logging plus détaillé",
            "Améliorer le monitoring des performances applicatives",
            "Établir des revues de code systématiques"
        ],
        'sécurité': [
            "Renforcer les politiques de sécurité",
            "Mettre en place une authentification multi-facteurs",
            "Effectuer des audits de sécurité réguliers",
            "Mettre à jour régulièrement les composants de sécurité"
        ],
        'processus': [
            "Documenter et standardiser les processus",
            "Mettre en place des points de contrôle qualité",
            "Automatiser les tâches répétitives",
            "Établir des KPIs pour mesurer l'efficacité"
        ],
        'utilisateur': [
            "Mettre en place un programme de formation continue",
            "Améliorer la documentation utilisateur",
            "Simplifier les interfaces utilisateur",
            "Établir un canal de feedback utilisateur"
        ]
    }

    @staticmethod
    def analyze_root_cause(whys: List[str]) -> str:
        """Analyse les 5 pourquoi pour déterminer la cause racine"""
        # Filtrer les réponses non vides
        valid_whys = [why for why in whys if why and why.strip()]
        
        if not valid_whys:
            return "Cause racine non déterminée"

        # Utiliser la dernière réponse comme base
        last_why = valid_whys[-1]
        
        # Analyser les mots-clés pour identifier le domaine
        domain = ProblemAnalyzer._identify_domain(last_why)
        
        # Enrichir la cause racine avec le contexte du domaine
        return f"[{domain.upper()}] {last_why}"

    @staticmethod
    def suggest_solutions(title: str, description: str, whys: List[str], root_cause: str) -> List[str]:
        """Suggère des solutions basées sur l'analyse complète du problème"""
        # Identifier le domaine principal
        all_text = f"{title} {description} {' '.join(whys)} {root_cause}"
        main_domain = ProblemAnalyzer._identify_domain(all_text)
        
        # Obtenir les solutions spécifiques au domaine
        domain_solutions = ProblemAnalyzer.DOMAIN_SOLUTIONS.get(main_domain, [])
        
        # Analyser la gravité basée sur les mots-clés
        severity = ProblemAnalyzer._analyze_severity(all_text)
        
        # Personnaliser les solutions
        solutions = []
        
        # Ajouter une solution spécifique basée sur la cause racine
        solutions.append(f"Action immédiate : {ProblemAnalyzer._generate_immediate_action(root_cause)}")
        
        # Ajouter des solutions du domaine pertinentes
        solutions.extend(domain_solutions[:2])  # Limiter à 2 solutions génériques
        
        # Ajouter une solution préventive basée sur la sévérité
        if severity == 'high':
            solutions.append("Mettre en place un système de détection précoce avec alertes automatiques")
        
        return solutions

    @staticmethod
    def _identify_domain(text: str) -> str:
        """Identifie le domaine ITIL basé sur les mots-clés"""
        text = text.lower()
        domain_scores = {}
        
        for domain, keywords in ProblemAnalyzer.ITIL_DOMAINS.items():
            score = sum(1 for keyword in keywords if keyword in text)
            domain_scores[domain] = score
        
        # Retourner le domaine avec le score le plus élevé
        return max(domain_scores.items(), key=lambda x: x[1])[0]

    @staticmethod
    def _analyze_severity(text: str) -> str:
        """Analyse la sévérité du problème"""
        high_severity_keywords = ['critique', 'urgent', 'bloquant', 'majeur', 'production', 'sécurité']
        text = text.lower()
        
        severity_score = sum(1 for keyword in high_severity_keywords if keyword in text)
        return 'high' if severity_score > 1 else 'normal'

    @staticmethod
    def _generate_immediate_action(root_cause: str) -> str:
        """Génère une action immédiate basée sur la cause racine"""
        root_cause = root_cause.lower()
        
        if 'configuration' in root_cause:
            return "Standardiser et documenter les paramètres de configuration"
        elif 'formation' in root_cause:
            return "Organiser des sessions de formation ciblées"
        elif 'ressource' in root_cause:
            return "Optimiser l'allocation des ressources"
        elif 'processus' in root_cause:
            return "Réviser et optimiser le processus concerné"
        else:
            return f"Mettre en place des contrôles pour éviter la récurrence de : {root_cause}" 