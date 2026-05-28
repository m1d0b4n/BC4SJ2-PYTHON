# Guide d'installation

## Installation en local

### Initialiser le projet

1. Lancer l'interpreteur python avec la commande et créer l'environnement
```shell
python3 -m venv myenv
```


2. Verifier l'installation Django avec la commande et le code suivant
```shell
python3
```
```python 
>> import django
>> print(django.get_version())
```
Pour quitter l'interpreteur, utiliser la commande ```exit()```

2. Importer le script SQL dans votre base de donnée
```shell
    mysql -u [username] -p [database_name] < ./sql/library.sql
```
Un mot de passe vous sera alors demandé, dans le cas ou aucun mot de passe n'es configuré sur votre base, vous pouvez retirer le `-p`
Par exemple pour un utilisateur root sans mot de passe avec une base de donnée library:
```shell
    mysql -u root library < ./sql/library.sql
```

3. Il faut également installer pymysql avec
```shell
pip install -r ./requirements.txt
```
en console python,
ou
```shell
python3 -m pip install -r ./requirements.txt
```

4. Migrer les données
```shell
python3 manage.py migrate
```

### Lancer le projet

1. Exécuter manage.py pour appeler la fonction runserver
```shell
python3 manage.py runserver
```

2. Accéder à l'Application
Ouvrez votre navigateur et allez sur la page http://localhost:8000.

3. Connexion
Connectez vous à l'aide d'un des comptes via la page Connexion
**Rôle Admin :**
```
john@smith.com
azerty
```

OU
**Rôle utilisateur :**
```
marc@lord.com 
azerty
```

## Installation distant

Le projet est pré-déployé sur le lien reçu au début de votre examen.
Ce lien vous permet d'accèder au projet via un lien HTTPs

Vous avez une connexion SFTP disponible et SSH afin de modifier ce projet en conséquence
Attention, prévoyez bien vos modifications en local et testez bien ces dernières avant de les déployers.