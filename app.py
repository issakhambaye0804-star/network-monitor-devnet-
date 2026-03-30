#!/usr/bin/env python3
"""
NetWatch-L3RI - Application de Monitoring de Conteneurs Docker
Projet d'Examen DEVNET - L3 RI ISI Keur Massar

Application Flask qui surveille la disponibilité (UP/DOWN) des conteneurs Docker
sur un réseau isolé avec interface web moderne.
"""

import os
import subprocess
import socket
import time
from datetime import datetime
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Configuration des services à surveiller
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
    },
    {
        'name': 'Service Cache',
        'container': 'redis',
        'ip': '172.20.0.4', 
        'port': 6379
    }
]

def ping_service(ip, port, timeout=2):
    """
    Vérifie si un service est joignable en utilisant socket
    Retourne True si joignable, False sinon
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Erreur de connexion à {ip}:{port} - {e}")
        return False

def ping_container(container_name):
    """
    Alternative: Utilise ping système pour vérifier le conteneur
    """
    try:
        # Ping avec timeout de 1 seconde
        result = subprocess.run(
            ['ping', '-c', '1', '-W', '1', container_name],
            capture_output=True,
            text=True,
            timeout=3
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Erreur ping {container_name}: {e}")
        return False

def check_service_status(service):
    """
    Vérifie le statut d'un service
    """
    # Essai avec socket en premier (plus rapide)
    if ping_service(service['ip'], service['port']):
        return {
            'status': 'UP',
            'badge_class': 'badge-success',
            'text_class': 'text-success',
            'last_check': datetime.now().strftime('%H:%M:%S')
        }
    else:
        # Alternative avec ping système
        if ping_container(service['container']):
            return {
                'status': 'UP', 
                'badge_class': 'badge-success',
                'text_class': 'text-success',
                'last_check': datetime.now().strftime('%H:%M:%S')
            }
        else:
            return {
                'status': 'DOWN',
                'badge_class': 'badge-danger', 
                'text_class': 'text-danger',
                'last_check': datetime.now().strftime('%H:%M:%S')
            }

def get_all_services_status():
    """
    Récupère le statut de tous les services
    """
    services_status = []
    for service in SERVICES:
        status = check_service_status(service)
        services_status.append({
            'name': service['name'],
            'container': service['container'],
            'ip': service['ip'],
            'port': service['port'],
            'status': status['status'],
            'badge_class': status['badge_class'],
            'text_class': status['text_class'],
            'last_check': status['last_check']
        })
    return services_status

@app.route('/')
def index():
    """
    Page principale avec le tableau de monitoring
    """
    services_status = get_all_services_status()
    
    # Statistiques globales
    total_services = len(services_status)
    up_services = len([s for s in services_status if s['status'] == 'UP'])
    down_services = total_services - up_services
    
    return render_template('index.html', 
                        services=services_status,
                        total=total_services,
                        up=up_services,
                        down=down_services,
                        last_refresh=datetime.now().strftime('%H:%M:%S'))

@app.route('/api/status')
def api_status():
    """
    API endpoint pour le statut des services (format JSON)
    """
    services_status = get_all_services_status()
    return jsonify({
        'services': services_status,
        'timestamp': datetime.now().isoformat(),
        'total': len(services_status),
        'up': len([s for s in services_status if s['status'] == 'UP']),
        'down': len([s for s in services_status if s['status'] == 'DOWN'])
    })

@app.route('/api/refresh')
def api_refresh():
    """
    API endpoint pour rafraîchir manuellement les statuts
    """
    services_status = get_all_services_status()
    return jsonify({
        'message': 'Services refreshed',
        'services': services_status,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    """
    Health check pour Docker
    """
    return jsonify({
        'status': 'healthy',
        'service': 'NetWatch-L3RI',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🌐 Démarrage de NetWatch-L3RI")
    print("📊 Application de monitoring de conteneurs Docker")
    print("🔍 Surveillance des services sur réseau isolé")
    print(f"🌐 Accès: http://localhost:5000")
    print(f"📅 Démarré à: {datetime.now().strftime('%H:%M:%S')}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
