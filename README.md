# Python pour la Datascience

Clément Maurer & Jeremy Demay


## Introduction : 

### Présentation des données :

Le dataset utilisé lors de ce projet est consacré aux Airbnb. 

Ce dataset contient des informations tels que la localisation, les notes ou le prix de près de 270 000 Airbnb réparties dans près 10 villes.

Malheuresement les monnaies utiliser ne sont pas les memes, certaines représentations ne seront donc pas exactes. 

Le dataset est disponible au lien suivant [Dataset](https://www.kaggle.com/mysarahmadbhat/airbnb-listings-reviews).

## Rapport d'analyse : 

### Cartes :

Il y a 2 cartes différentes : 
* Une carte des airbnb colorée en fonction des quartiers
* Une carte des airbnb colorée en fonction du prix   

Ces deux cartes nous permettent d'apprendre plusieurs choses sur les Airbnb.

Grâce à la carte des quartiers on peut facilement se rendre compte de la densité des airbnb et de leur localisation à travers les differentes villes.

Grâce à la heatmap (carte en fonction du prix) on peut voir les lieux les plus huppés de chaque villes. 

Grâce à ces deux cartes on se rend compte du nombre important de airbnb présent un peu partout dans les villes présentés. On peut également se rendre compte que les prix de ces airbnb varient beaucoup en fonction de la localisation des biens.

### Histogrammes : 

Le premier histogramme represente le répartition des prix des airnbnb. 

Cet histogramme permet de se rendre compte que la très grande majoritée des airbnb ont un prix "faible".

Le second histogramme lui represente les notes. 

Celui ci nous permet de voir que les notes globales ont tendance a être très élevées.

### Prix en fonction du nombre de personne : 

Le dernier graphique représente à l'aide d'un scatter plot le prix de chaque airbnb en fonction du nombre de personne. En analysant ce graphique, on se rend compte que le prix n'est pas du tout proportionnel au nombre de personnes. On peut donc en conclure que ce qui joue le plus dans le prix est la localisation du bien ou ces equipements.

## User guide : 

Afin d'executer le code plusieurs étapes sont nécessaires : 

Tout d'abord on peut cloner le projet : `git clone https://github.com/Heliooz/Python_Datascience.git`

Ensuite, il faut télécharge les paquets nécessaires. Ces paquets sont listés dans le fichiers *requirements.txt*.

Afin de les installer on peut utiliser la commande suivante après s'être placé dans le repertoire du projet : `python -m pip install -r requirements.txt`

Après il faut configurer la clef kaggle afin de pouvoir télécharger le dataset.

Pour cela suivez les instructions présentes dans la partie *Authentication* de la page suivante :
[kaggle](https://www.kaggle.com/docs/api)

Enfin on peut lancer le main grace à : 

* Linux / MacOS : `python3 main.py`
* Windows : `python main.py`

A cause de la création des cartes le dashboard met un peu de temps à se lancer. 

Une fois que le dashboard est lancé suivez l'adresse indiquée.

## Developper Guide 

Le code est divisé en plusieurs parties :

Dans un premier on peut trouver, dans le dossier *src*, les fichiers *create_map.py*, *get_data.py* et *read_data.py*.

### *create_map.py*

Le fichier *create_map.py* est lui même divisé en deux fonntions : *generate_colors* et *create_maps*

#### *generate_colors*

Cette fonctions prend en parametre la liste des quartiers d'une ville et génère un dictionnaire avec pour clef le nom du quartier et pour valuer une couleur en hexadecimal. 

Cette fonction a pour but de génèrer une palette de couleur pour l'affichage par quartier.

#### *create_maps*

Cette fonction prend en paramêtre un dictionnaire contenant pour clef le nom de la ville et pour valeur le dataset lui correspondant.

Grace à ce dictionnaire on va iterrer sur les villes afin de récuperer chaque dataset puis récuperer les localisations de chaque airbnb afin de les afficher sur une carte. 

On va grace a ces boucles créer pour chaque ville une heat map et une carte par quartier.

### *get_data.py*

Ce fichier est décomposer en deux fonctions : 

La première *get_data* permet de récuperer le dataset depuis kaggle en utilisant les lignes de commandes puis de decompresser le fichier *.zip* récuperer.

La seconde *get_data_kaggle* sert exactement à la même chose mais utilise elle la biblioteque de python 

### *read_data.py*

Le fichier *read_data.py* est composé d'une seule fonction, cette dernière permet de créer un objet de type *pandas.Dataset* a partir du fichier csv contenant les données.


### *main.py*

Le fichier *main.py* est le fichier principal du projet ce dernier contient 2 fonctions ainsi qu'un code brut executé lors du lancement permettant de créer le dashboard. 

#### *filter_data*

*filter_data* est une fonction utilisée lors de l'affiche des graphiques. Cette fonction prend en parametre les parametres rentrées par l'utilisateur et renvoie le dataset correspondant.


#### *clean_data*

Cette fonction est, comme son nom l'indique, utilisée afin de netoyé le dataframe. Pour cela on supprime toutes les colones non utiles à la création des graphiques et des cartes. 

Elle supprime également les lignes absurdes (où le prix est égal à 0)

#### Dashboard 

La création du dashboard se fait en plusieurs parties : 

1 : Le téléchargement, la récupération puis le netoyage des données.

2 : La création du dictionnaire des villes 

3 : La création des cartes 

4 : La création du dashboard et de son layout

5 : La création des callbacks

Afin de permettre une reprise du code j'ai expliqué le fonctionnement des callback dans les docstrings.

