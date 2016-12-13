# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 14:59:41 2016

@author: martin.provost
"""

import Connect_tweepy
import Read_Tree
import time
import sys
import csv
import tweepy

global KEYWORDS 
global GEOCODE 
global RADIUS
KEYWORDS= ['data science']
GEOCODE = "48.860710, 2.336775"
RADIUS = "20km"

def main():
    if __name__ == '__main__':
        print time.ctime()
        api=Connect_tweepy.TweepyConnect()
        data = api.rate_limit_status()

        remain_follow=data['resources']['followers']['/followers/list']
        remaining= remain_follow['remaining']
        reset_time= time.ctime(int( remain_follow['reset']) )                
        attente= remain_follow['reset'] - time.time()
        
        search_dico=Connect_tweepy.keyWordsSearch(api, keyWords='data science', maxTweets=20)           
        search_dico.set_index("id_tweet", inplace=True)
        
        print u"Le DataFrame des tweets contient " + str(search_dico.shape[0]) + " lignes et "+ str(search_dico.shape[1]) + " colonnes"
        
        Read_Tree.Delete_All_Graph()
        Read_Tree.Create_Nodes(search_dico)
        
        
        if(remaining == 0):
            print (u"il n'y a plus de requêtes disponible, il faut attendre jusqu'à " + reset_time)
#            sys.exit(0) #permet de quitter le programme
            time.sleep(int(attente+1)) # permet d'attendre le temps qu'il faut pour récupérer le droit de requêter.
        
        
        
        #On initialise un fichier CSV qui va contenir les informations récoltées
        csvfile = open('tree.csv', 'wb')
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        
        for entry_user in search_dico["author"]:    
                #entry_user est le point d'entrée du "graphe", pour le moment on le spécifie à la main, mais il faut pouvoir le 
                # récupérer via un search par mots clés par la suite                
                
                tree={} # on initialise un dictionnaire qui va contenir les données        
                
                #On crée une ligne dans le dico pour l'utilisateur d'entrée avec ses followers
                tree = Screen_NametoDic(api, entry_user, tree )
                
                followers = Screen_NametoList(api,entry_user)
                if followers == []:
                    #Si la personne qui a tweeté a bloqué l'accès à ses followers, on passe au suivant
                    next
                #On liste les followers dans un fichier csv, avec en 1er le parent, et ensuite ses followers
                writer.writerow(list([entry_user]) + followers)
                
                #Ecriture des infos dans le graphe NEO4J
                list_Neo=Read_Tree.Read_Tree_List(list([entry_user]) + followers)
                Read_Tree.Graph_Followers(list_Neo)
                
                #Fonction pour requêter et récupérer les followers des followers
                Followers_of_Followers(api, writer, tree, entry_user, maxFollower=10)

        csvfile.close()
        #        WriteTree(tree)
        
#        list_neo4j = Read_Tree.Read_TreeCSV()
#        Read_Tree.Graph_Followers(list_neo4j)
        
def getFollowers(api, nickname):
    #Récupérer les followers d'un utilisateur donné (id ou screen_name)   
    try:
        followers = api.followers(nickname)
    except tweepy.TweepError:
        print(u"L'utilisateur "+ nickname + u" semble avoir protégé son compte, Skipping...")    
        return []
    return followers
    
def FollowerstoList(followers):
    #Renvoie les followers en liste
    l=[]    
    for f in followers:
        l.append(f.screen_name)
    return l

def Screen_NametoList(api,nickname):
    #Renvoie les followers en liste à partir du nickname
    l=[]
    followers = getFollowers(api, nickname)
    if followers==[]:
        return []
    for f in followers:
        l.append(f.screen_name)
    return l

def Screen_NametoDic(api,nickname, dic):
    #Ajoute les followers au dictionnaire passé en argument à partir du nickname
    if not (nickname in dic.keys()):
        followers = getFollowers(api, nickname)
        dic[nickname]=FollowerstoList(followers)
        # on affiche l'heure pour pouvoir visualiser que le programme travaille lorsqu'il est long        
        print time.ctime()
    return dic

def WriteTree(tree):
    #Ecrit le contenu de l'arbre des relations dans un fichier CSV
    with open('tree.csv', 'wb') as csvfile:
#    fieldnames = ['first_name', 'last_name']
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)    
        for key, list_follow in tree.items():    
            writer.writerow(list_follow)

def Followers_of_Followers(api, writer, tree, entry_user, maxFollower=10):
    # cette fonction va récupérer les followers des followers des gens qui ont cité le(s) mot(s) clé(s)
    i=0
    for nickname in tree[entry_user]:
        if i < maxFollower:                    
            data = api.rate_limit_status()

            remain_follow=data['resources']['followers']['/followers/list']
            remaining=remain_follow['remaining']               
            
            if(remaining == 0): #Nous n'avons plus de requêtes pour les followers à dispo
                reset_time= time.ctime(int(remain_follow['reset']) )
                attente= remain_follow['reset'] - time.time()
                print (u"il n'y a plus de requêtes disponible, il faut attendre jusqu'à " + reset_time)
                time.sleep(int(attente+1)) # permet d'attendre le temps qu'il faut pour récupérer le droit de requêter.
#                            sys.exit(0) #permet de quitter le programme
            else:                    
                tree=Screen_NametoDic(api,nickname,tree)
                followers = Screen_NametoList(api,nickname)
                if followers == []:
                    next
                    
                #On liste les followers dans un fichier csv, avec en 1er le parent, et ensuite ses followers
                writer.writerow(list([nickname]) + followers)
                
                #Ecriture des infos dans le graphe NEO4J
                list_Neo=Read_Tree.Read_Tree_List(list([nickname]) + followers)
                Read_Tree.Graph_Followers(list_Neo)                
                
                i+=1
    
    
#On éxécute le main
main()