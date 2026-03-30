# 🛡️ NetWatch-L3RI - Monitoring de Conteneurs Docker

**Projet d'Examen DEVNET - L3 RI ISI Keur Massar**

Application Flask de surveillance de la disponibilité (UP/DOWN) des conteneurs Docker sur un réseau isolé avec interface web moderne et monitoring temps réel.

---

## 📋 Description du Projet

### **Objectif**
Surveiller en temps réel la disponibilité de plusieurs conteneurs Docker déployés sur un réseau personnalisé isolé, avec une interface web intuitive et des alertes visuelles.

### **Problème Résolu**
Dans un environnement Docker, il est crucial de:
- **Surveiller** la santé des services déployés
- **Détecter** rapidement les pannes de conteneurs
- **Visualiser** l'état du réseau de manière claire
- **Automatiser** les vérifications de connectivité

### **Solution Technique**
Une application Flask qui:
- ✅ Vérifie la connectivité des conteneurs via socket/ping
- ✅ Affiche une interface web avec Bootstrap
- ✅ Rafraîchit automatiquement les statuts
- ✅ Fournit des API endpoints pour l'intégration

---

## 🏗️ Architecture du Système

### **Schéma Réseau**
```
┌─────────────────────────────────────────────────────────┐
│                Réseau Docker Isolé                │
│  Subnet: 172.20.0.0/24                        │
│                                                  │
│  ┌─────────────────┐    ┌──────────────────┐   │
│  │   Web Service   │    │  DB Service     │   │
│  │   (Flask App)  │    │  (Nginx)       │   │
│  │  172.20.0.2    │    │  172.20.0.3    │   │
│  │   Port: 5000    │    │  Port: 80       │   │
│  └─────────────────┘    └──────────────────┘   │
│                                                  │
└─────────────────────────────────────────────────────────┘
```

### **Composants Principaux**

| Composant | Rôle | Technologies |
|------------|-------|--------------|
| **App Flask** | Interface web & monitoring | Python 3.9, Flask, Bootstrap |
| **Docker** | Conteneurisation & isolation | Docker, Docker Compose |
| **Réseau** | Communication isolée | Bridge network personnalisé |
| **CI/CD** | Automatisation déploiement | GitHub Actions, Docker Hub |

---

## 🛠️ Technologies Utilisées

### **Backend**
- **Python 3.9**: Langage principal, robuste et performant
- **Flask 2.3.3**: Framework web léger et flexible
- **Socket Programming**: Vérification de connectivité réseau

### **Frontend**
- **Bootstrap 5.3.0**: Design responsive et moderne
- **Bootstrap Icons**: Icônes professionnelles
- **JavaScript**: Rafraîchissement automatique

### **Infrastructure**
- **Docker**: Conteneurisation et isolation
- **Docker Compose**: Orchestration multi-services
- **GitHub Actions**: Pipeline CI/CD automatisé
- **Docker Hub**: Registry d'images publiques

---

## 🚀 Installation et Déploiement

### **Prérequis**
- Docker et Docker Compose installés
- Git pour le versioning
- Compte Docker Hub pour le CI/CD

### **Installation Locale**
```bash
# 1. Cloner le repository
git clone https://github.com/VOTRE_USERNAME/netwatch-l3ri.git
cd netwatch-l3ri

# 2. Construire et démarrer les services
docker-compose up --build -d

# 3. Accéder à l'interface
# Ouvrir http://localhost:5000
```

### **Déploiement Production**
```bash
# 1. Pull de l'image Docker Hub
docker pull VOTRE_USERNAME/network-monitor-devnet:latest

# 2. Lancement avec docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📊 Fonctionnalités

### **Monitoring Temps Réel**
- **Vérification automatique** toutes les 30 secondes
- **Badge visuel**: Vert pour UP, Rouge pour DOWN
- **Horodatage** de chaque vérification
- **Statistiques globales** (total, UP, DOWN)

### **Interface Web Moderne**
- **Design responsive** adapté mobile/desktop
- **Tableau interactif** avec informations détaillées
- **Animations** pour améliorer l'expérience utilisateur
- **Rafraîchissement** manuel et automatique

### **API REST**
- **GET /**: Interface web principale
- **GET /api/status**: Statut JSON des services
- **GET /api/refresh**: Rafraîchissement manuel
- **GET /health**: Health check pour Docker

---

## 🔧 Configuration

### **Services Monitorés**
Les services sont configurés dans `app.py`:
```python
SERVICES = [
    {
        'name': 'Serveur Web Principal',
        'container': 'web',
        'ip': '172.20.0.2',
        'port': 5000
    },
    {
        'name': 'Base de Données', 
        'container': 'db_serveur',
        'ip': '172.20.0.3',
        'port': 80
    }
]
```

### **Réseau Docker**
- **Nom**: `netwatch_network`
- **Type**: Bridge
- **Subnet**: `172.20.0.0/24`
- **Isolation**: Communication uniquement entre conteneurs

---

## 🧪 Tests et Validation

### **Tests de Connectivité**
```bash
# Test de l'application web
curl http://localhost:5000/health

# Test de l'API
curl http://localhost:5000/api/status

# Test de rafraîchissement
curl http://localhost:5000/api/refresh
```

### **Tests Docker**
```bash
# Vérification des conteneurs
docker ps

# Vérification du réseau
docker network ls
docker network inspect netwatch_network

# Logs des services
docker-compose logs -f
```

---

## 🔄 CI/CD Pipeline

### **GitHub Actions Workflow**
Le fichier `.github/workflows/deploy.yml` automatise:

1. **Construction** de l'image Docker multi-architecture
2. **Push** vers Docker Hub avec tags automatiques
3. **Mise à jour** de la description du repository
4. **Notification** de succès du déploiement

### **Configuration requise**
Dans les secrets GitHub:
- `DOCKER_USERNAME`: Votre username Docker Hub
- `DOCKER_PASSWORD`: Votre password ou access token

---

## 📈 Monitoring et Logs

### **Logs Application**
```bash
# Logs en temps réel
docker-compose logs -f web

# Logs de tous les services
docker-compose logs -f
```

### **Métriques Disponibles**
- **Taux de disponibilité**: % de temps UP
- **Temps de réponse**: Vérification toutes les 30s
- **Historique**: Dernières vérifications par service

---

## 🎯 Points d'Extension

### **Évolutions Possibles**
- **Notifications email/Slack** en cas de panne
- **Base de données** pour historique persistant
- **Grafana integration** pour graphiques avancés
- **Multi-réseaux** support pour différents environnements

### **Améliorations Techniques**
- **WebSocket** pour rafraîchissement temps réel
- **Authentication** pour accès sécurisé
- **Configuration dynamique** via interface web

---

## 📝 Développement

### **Structure du Projet**
```
netwatch-l3ri/
├── app.py                    # Application Flask principale
├── templates/
│   └── index.html           # Interface web Bootstrap
├── Dockerfile               # Configuration conteneur
├── docker-compose.yml       # Orchestration services
├── requirements.txt         # Dépendances Python
├── .github/
│   └── workflows/
│       └── deploy.yml       # Pipeline CI/CD
└── README.md              # Documentation projet
```

### **Contribution**
1. Fork du repository
2. Création branche feature
3. Commit des modifications
4. Pull request vers main

---

## 🎓 Contexte Pédagogique

### **Objectifs d'Apprentissage**
Ce projet démontre la maîtrise de:

- ✅ **Développement Web**: Flask, templates, API REST
- ✅ **Virtualisation**: Docker, conteneurisation
- ✅ **Réseaux**: Configuration réseau, monitoring
- ✅ **DevOps**: CI/CD, automatisation
- ✅ **Architecture**: Design système, isolation

### **Compétences Techniques**
- **Python avancé**: Socket programming, monitoring
- **Docker production**: Multi-services, réseaux
- **Frontend moderne**: Bootstrap, JavaScript
- **Git workflow**: Branches, pull requests
- **Cloud integration**: Docker Hub, GitHub Actions

---

## 📞 Support et Contact

### **Documentation Complète**
- **Code source**: Commenté et structuré
- **API documentation**: Endpoints détaillés
- **Installation guide**: Étape par étape
- **Dépannage**: Solutions aux problèmes courants

### **Pour l'Examen**
Ce projet est **100% fonctionnel** et prêt pour démonstration:
- 🎯 **Architecture Docker** complète
- 🌐 **Monitoring réseau** fonctionnel
- 📱 **Interface web** moderne
- 🔄 **CI/CD** automatisé
- 📊 **API REST** opérationnelle

---

**Développé dans le cadre du projet d'examen DEVNET**  
**L3 Réseaux et Informatique - ISI Keur Massar**  
**Année académique 2025-2026**

---

*NetWatch-L3RI - Surveillance intelligente de conteneurs Docker* 🛡️
