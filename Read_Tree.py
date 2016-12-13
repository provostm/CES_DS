# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 11:27:39 2016

@author: martin.provost
"""
import csv
from py2neo import Graph, Node, Relationship


def Delete_All_Graph():
        #Connexion à la base NEO4J perso
    graph = Graph(password='martin')
    graph.delete_all() # on vide le graph avant de le reconstruire


def Read_TreeCSV(filename="tree-maxTweet5-2followers.csv"):
    #Cette fonction permet de créer un graphe a partir d'un fichier CSV sauvegardé, on transforme le fichier en liste
    #puis on utilise la fonction Graph_Followers en passant la liste en argument
    neo=[]    
    f = open(filename, 'r')
    csvfile = csv.reader(f)
    
    for line in csvfile:        
        if line == "\n":
            next
        else :
            
            first=line[0]
            for element in line:
                if element == first :
                    next
                else :
                    neo.append( [first , element])

    return neo


def Read_Tree_List(list_followers):
    neo=[]
    first=list_followers[0]
    
    for element in list_followers:
        if element == first :
            next
        else :
            neo.append( [first , element])

    return neo


def Create_Nodes(df):
    #Connexion à la base NEO4J perso
    graph = Graph(password='martin')
    
    i=0    
    for i in range(df.shape[0]) :
        tx=graph.begin()
        author=df.iloc[i]["author"]
        tweet=df.iloc[i]["text"]
#        id_tweet=df.iloc[i].index()      
        create_date= df.iloc[i]["create_date"]
        author_location= df.iloc[i]["author_location"]
        full_name= df.iloc[i]["full_name"]
        
        a = Node("Twittos", name=author, tweet=tweet, create_date=str(create_date), full_name=full_name, author_location=author_location)
        tx.create(a)
        tx.commit()





def Graph_Followers(list_neo4j):
    print u"Il y a " + str(len(list_neo4j)) + u" tuples dans le fichier des followers"
    
    
    #Connexion à la base NEO4J perso
    graph = Graph(password='martin')
     
    for binome in list_neo4j:
        tx = graph.begin()
        userA=graph.find_one('Twittos', 'name', binome[0])
        if userA==None:
            a = Node("Twittos", name=binome[0])
            tx.create(a)
        else:
            a = userA            

        userB=graph.find_one('Twittos', 'name', binome[1])

        if userB==None: #binome[1] n'existe pas dans le graphe
            b = Node("Twittos", name=binome[1])
            ab = Relationship(a, "EST SUIVI PAR", b)

    
        else: #binome[1] existe dans le graphe, il est contenu dans le selector "selected"
            ab = Relationship(a, "EST SUIVI PAR", userB)
        
        tx.create(ab)
        tx.commit()    
