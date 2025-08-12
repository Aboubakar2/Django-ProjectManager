# Django Project Manager

Django Project Manager est une application web développée avec Django qui permet de gérer des projets, des tâches, des équipes et des ressources de manière collaborative.

## Fonctionnalités principales

- **Gestion des projets** : création, édition, suppression et recherche de projets, avec description, dates de début et de fin, et attribution à un utilisateur.
- **Gestion des tâches** : chaque projet peut contenir une ou plusieurs todolists, chacune composée de tâches avec description, dates, ressources associées, équipes et logiciels.
- **Gestion des équipes et agents** : création d’équipes, ajout de membres, définition de leaders et gestion des détails d’équipe.
- **Ressources matérielles et logicielles** : association de ressources à des tâches pour un meilleur suivi des moyens alloués.
- **Réunions et comptes-rendus** : planification de réunions liées à des tâches, création et édition de comptes-rendus pour garder l’historique des discussions et décisions.
- **Authentification et permissions** : accès sécurisé aux fonctionnalités principales via authentification Django.

## Installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/Aboubakar2/Django-ProjectManager.git
   cd Django-ProjectManager
   ```
2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Appliquer les migrations :
   ```bash
   python manage.py migrate
   ```
4. Créer un superutilisateur :
   ```bash
   python manage.py createsuperuser
   ```
5. Lancer le serveur de développement :
   ```bash
   python manage.py runserver
   ```

## Utilisation

- Connectez-vous avec votre compte utilisateur.
- Créez un nouveau projet.
- Ajoutez des todolists et des tâches à votre projet.
- Gérez les équipes, affectez des ressources et planifiez des réunions.

## Contribution

Les contributions sont les bienvenues ! Veuillez ouvrir une issue ou une pull request pour proposer des améliorations ou corriger des bugs.

> Développé avec Django.
