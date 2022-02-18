# Projet File rouge IOT auprès de M2i du 10/02/2022 au 22/02/2022

## Le cahier des charges 
Le cahier des charges et l'ensemble des fichiers annexes on été fournis par M. Youssef Elmoti, formateur et asistant pour ce projet fil rouge de fin de formation FD-DATA-0921-AURA auprès de M2i. Il s'agit :
<ul>
<li>Du cahier des charges : "<i><b>Prop-JEMS-FITEC IOT.docx</b></i>" </i></b></li>
<li>Du jeu de données fourni à considérer :</li>
<ul><b><i>
<li>X46789_2018-01-19T05-37-42.612Z.csv</li> 
<li>X46789_2018-01-19T05-56-20.307Z.csv</li> 
<li>X46789_2018-01-19T07-20-52.339Z.csv</li> 
<li>X46789_2018-01-19T07-39-30.012Z.csv</li> 
<li>X46789_2018-01-19T07-58-07.733Z.csv</li> 
<li>X46789_2018-01-19T09-00-42.821Z.csv</li> 
<li>X46789_2018-01-19T09-19-24.965Z.csv</li> 
<li>X46789_2018-01-19T09-56-40.312Z.csv</li> 
<li>X46789_2018-01-19T10-19-41.226Z.csv</li> 
<li>X46789_2018-01-19T10-38-18.941Z.csv</li> 
<li>X46789_2018-01-22T03-15-35.111Z.csv</li> 
<li>X46789_2018-01-22T03-56-59.619Z.csv</li> 
<li>X46789_2018-01-19T10-38-18.941Z.csv</li> 
<li>X46789_2018-01-22T09-17-43.409Z.csv</li> 
<li>X46789_2018-01-22T09-36-24.545Z.csv</li> 
<li>X46789_2018-01-22T10-13-39.943Z.csv</li> 
</ul></b></i>
</ul>

## Gestion de projet
Sont listés ci-dessous les livrables au titre de la g4estion de projet  Project Charter IOT.odt
Ce document énonce l'approche globale adoptée pour la réalisation du projet et contient notamment:

<ul>
    <li> Le Project Charter (au sens PMI) "<i><b>Project Charter IOT.odt</b></i>" : énonce l'approche globale, ainsi que les aspects liés à la portée, budget/coût, temps, communication, etc., </li>
    <li> Le plan prévisionnel "<i><b>Project Plan IOT.ods</b></i>": Le plan de projet tel qu'immaginé au premier jour du lancement. Le projet étant de courte durée, et les délais respectés dans l'ensemble et à tout moment, il n'a pas été nécessaire de l'amender au cours du projet.</li>
</ul>

## Livrables 
De par le cahier des charges, au sens strict de la donnée, ce projet se situe plutôt dans l'axe data engineering faisant d'avantage appel à des compétences techniques plutôt qu'à des compétences analytiques. Il s'agira pour l'essentiel de démontrer les capacités à gérer et à visualiser des flux continus de données générés par des IOTs (Internet Of Objects). Ci dessous, figurent l'ensembe des livrables regroupés par catégorie. 
### Conception
Le projet se subdivise en deux étapes. Une première, consiste simplement à charger le jeu de données fourni dans un outil de visualisation type Tableau; cette étape ne nécessite pas la mise en oeuvre d'une architecture particulière. La deuxième qui consiste à simuler un flux continu de données génré par des IOTs nécessite quant à elle, la mise en place d'une architecture conséquente pour assurer le transport de la donnée de bout en bout depuis la production jusqu'au rendu et ce de manière quasi-instantanée.
En outre, afin de sattisfaire les exigeances du projet en matière d'intégration de flux additionnels, il a été nécessaire de rechercher, concevoir et mettre en oeuvre des méchanismes permettant à l'emsemble du système de s'adapter à des schémas de données aussi variés qu'il y a de types  de IOTs différents. 

<ul>
<li> Le modèle de conception technique pour les données en mouvements générés par les IOT : <i><b>"Conception Architecture Technique Data Streaming IOT.pdf",</i></b></li>
<li> Le jeu de données récupéré et considéré au titre de l'évolutivité du système en terme d'ajout de flux aditionnel : <i><b>ORNEK_200KM_UZUN_YOL_LOG_COROLLA der version attention date peut etre (1).csv</i></b>.</li>
</ul>

### Partie Statique (Mode Batch)
<ul>
<li>Le tableau de bord statique montrant les défférentes métriques des fichier csv fournis et chargés tels quels dans l'application Tableau. Le lien ci-contre permet d'y accéder <a haref=https://public.tableau.com/app/profile/voiturin/viz/Projet-Iot/Tableaudebord1?publish=yes>https://public.tableau.com/app/profile/voiturin/viz/Projet-Iot/Tableaudebord1?publish=yes</a>.</li>
</ul>

### Partie Dynamique (Temps Réel)

#### Simulations des IOTs
Pour simuler des IOTs produisant des données en flux continu, il a été nécessaire de mettre en oeuvre un certain nombre de composants.
<ul>
<li>Base de données MySQL contenant les données à produire pour la simulaton des IOTs et chargés initialement par les fichiers csv fournis,</li>
<li>Les scripts de chargement des données fournie,</li>
<li>Le/Les programmes Python lisant les donnés de la base données MySQL et produisant un flux continu et cadencé à raison d'une mesure selon une fréquence adaptable en fonction du type de IOT. Les données sont communiquées au format JSON à un microservice par une a requête POST via API REST / HTTP.</li>
</ul>

#### Data Streaming
Le déclouplage entre les producteurs de données en flux continu, dans notre cas des IOTs, et les consomateurs de ces mêmes données à des fin de analyse/monitoring en tems réel, dans notre cas,  deux couples base de données Elastisearch et Kibana, sera assuré par Apache Kafka. Vu le contexte académique, les aspects liés l'équilibrage de charges n'est pas pris en compte dans le cadre de ce projet mais pourrait être aisément mis en oeuvre sans trop d'effort par le couple nginx / Docker (voir Kubernetes) en amont des microservices d'ingestion. 
<ul>
<li> Le script d'installation et configuration de Apache Kafka sous Linux : <i><b>Installation kafka linux 3.0.0.txt</i></b>,</li>
<li> Le microservice d'ingestion des données produites par IOTs en flux continu pour découplage écrit en python : "<i><b>kafka_producer_microservice2.py</i></b>",</li>
<li>Le programme qui consomme les données en streaming découplées et qui les envoie au  microservice pour ingeston dans Elastisearch par une a requête POST via API REST / HTTP : "<i><b>kafka_consumer_to_service2.py</i></b>".</li>
</ul>


#### DataViz
Le but ultime étant de pouvoir observer des donées en mouvement,  la suite Elastisearch / Kibana nous a paru comme étant l'outil le plus adapté pour la visualisation. Celui-ci permet de définir des fenêtre dobservabilité dans une échelle temporelle. Nous avons utilisé une installation "on premisses" via Docker ainsi que la version cloud avec une préférence largement partagée par l'équipe de projet pour cette dernière.
<ul>
<li>Le script yml pour la configuration de Elastisearch et Kibada avec Docker : <i><b>"docker-compose.yml"</i></b>,</li>
<li>Le microservice d'ingestion dans Elastiseacrh des données découplées  en provenance des IOT : "<i><b>elastic_microservice2.py</i></b>",</li>
<li>La video montrant dans Kibana cloud un tableau de bord des données en mouvement issues du streaming de l'architechture mise en place : <i><b>"20220218_104145.mp4"</i></b>.</li>
</ul>




