# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 10:47:37 2016

@author: martin.provost
"""

#import Connect_tweepy

from py2neo import Graph
import pandas as pd


def Delete_All_Graph():
        #Connexion à la base NEO4J perso
    graph = Graph(password='martin')
    graph.delete_all() # on vide le graph avant de le reconstruire

def Query_Graph():
    graph = Graph(password='martin')
    
    # la requête ci dessous compte toutes les relations de retweet tout tweet confondu, cad que si une personne a tweeté 2 fois à propos du 
    # mot clé, on somme les retweets pour ces tweets pour donner un nombre total de rewteets
    results_Twittos = graph.run("MATCH (n:Twittos)-[r]->(x) RETURN n.name as Screen_name, n.lang as Langue, n.tweet, COUNT(r) as Nb_Relations ORDER BY Nb_Relations DESC")
    
    # la requête ci dessous compte le nombre de retweets effectué par un Retweeter quelque soit le tweet, cad qu'on somme tous les retweets de 
    # cet utilisateur pour les tweets sélectionnés sur les mots clés.
    results_Retweeters = graph.run("MATCH (x)-[r]->(n:Retweeter) RETURN n.name as Screen_name, n.lang as Langue, COUNT(r) as Nb_Relations ORDER BY Nb_Relations DESC")
    

    
    df_twittos=pd.DataFrame.from_records(results_Twittos, columns=results_Twittos.keys())
    df_retweeters=pd.DataFrame.from_records(results_Retweeters, columns=results_Retweeters.keys())
        

    print ("---------Best Twittos----------------")
    print df_twittos[df_twittos.Nb_Relations > 1]
    print ("---------Best Retweeters-------------")
    print df_retweeters[df_retweeters.Nb_Relations > 1]

Query_Graph()