# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 14:59:41 2016

@author: martin.provost
"""
#Mes fonctions
import Connect_tweepy
#import Read_Tree
import Query_Graph

#Les librairies de Python
import time
import sys
import csv
import tweepy
from py2neo import Graph, Node, Relationship


KEYWORDS= ['"informatica"']
RESULT_TYPE="mixed recent popular" # valeurs possibles : mixed, recent, popular
#GEOCODE = "48.860710, 2.336775"
#RADIUS = "20km"
MAXTWEETS=1
RETWEET_ONLY=True # True pour le graphe sur les retweets, False pour le graphe sur les followers
LANGUES=['fr', 'en'] # vérifier qu'il est possible de spécifier 2 langues

#Paramètres pour le graphe sur les followers
ENTRY_FOLLOWER=5
FOLLOWERS_of_FOLLOWER=5

#Paramètres pour le graphe sur les retweets
MAX_RETWEETS=100 #maximum 100
LIMIT_RETWEETS=1 #limite à partir de laquelle on collecte les tweets qui ont au moins xx retweets. (minimum 0). cette option fonctionne si RETWEET_ONLY == True

def main():
    if __name__ == '__main__':
        print time.ctime()
        api=Connect_tweepy.TweepyConnect()
        
        Check_Limit_API(api)
        search_dico=Connect_tweepy.keyWordsSearch(api, keyWords=KEYWORDS, langues=LANGUES, maxTweets=MAXTWEETS, result_type=RESULT_TYPE, \
                                                    retweet=RETWEET_ONLY, limit_retweets=LIMIT_RETWEETS)           
        
        if search_dico.empty:
            print(u"Pas de tweets pour ces mots clés\n")
            sys.exit(0)
        search_dico.set_index("id_tweet", inplace=True)
        
        print u"Le DataFrame des tweets contient " + str(search_dico.shape[0]) + " lignes et "+ str(search_dico.shape[1]) + " colonnes"
        
        Query_Graph.Delete_All_Graph()
        
        search_dico = Create_Nodes(api, search_dico)
        
        print u"Le DataFrame d'origine contient maintenant " + str(search_dico.shape[0]) + " lignes et "+ str(search_dico.shape[1]) + " colonnes" 
        
        search_dico.to_csv('collect_tweets.csv', sep='|', encoding='utf-8')
        search_dico.set_index("id_tweet", inplace=True)
        
        Query_Graph.Query_Graph()
        
#        if(remaining == 0):
#            print (u"il n'y a plus de requêtes disponible, il faut attendre jusqu'à " + reset_time)
##            sys.exit(0) #permet de quitter le programme
#            time.sleep(int(attente+1)) # permet d'attendre le temps qu'il faut pour récupérer le droit de requêter.
        
        
        
        #On initialise un fichier CSV qui va contenir les informations récoltées
#        csvfile = open('tree.csv', 'wb')
#        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        
#        for entry_user in search_dico["author"]:    
#                # on vérifie s'il reste des requêtes dispo pour l'API (si non, on attend automatiquement)
#                Check_Limit_API(api) 
#                # on affiche l'heure pour pouvoir visualiser que le programme travaille lorsqu'il est long        
#                print time.ctime()
##                tree={} # on initialise un dictionnaire qui va contenir les données        
#                
#                #On crée une ligne dans le dico pour l'utilisateur d'entrée avec ses followers
##                tree = Screen_NametoDic(api, entry_user, tree, ENTRY_FOLLOWER )
#                
#                followers, location = Screen_NametoList(api, entry_user, ENTRY_FOLLOWER)
#                print followers
#                print location
#                if followers == []:
#                    #Si la personne qui a tweeté a bloqué l'accès à ses followers, on passe au suivant
#                    next
#                #On liste les followers dans un fichier csv, avec en 1er le parent, et ensuite ses followers
#                writer.writerow(list([entry_user]) + followers)
#                
#                #Ecriture des followers dans le graphe NEO4J
#                list_Neo4j=Read_Tree.Read_Tree_List(list([entry_user]) + followers)
#                Read_Tree.Graph_Followers(list_Neo4j)
#                
                #Fonction pour requêter et récupérer les followers des followers
#                Followers_of_Followers(api, writer, followers, entry_user, maxFollower=FOLLOWERS_of_FOLLOWER)
                
#        csvfile.close()
        #        WriteTree(tree)
        
#        list_neo4j = Read_Tree.Read_TreeCSV()
#        Read_Tree.Graph_Followers(list_neo4j)


    
def Create_Nodes(api, df):
    #Connexion à la base NEO4J perso
    graph = Graph(password='martin')
    
    i=0
    for i in range(df.shape[0]) :
            Check_Limit_API(api) #Fonction qui vérifie s'il reste des requêtes dispo sur l'API
#            print time.ctime()
            
            tx=graph.begin()
            author=df.iloc[i]["author"]
            tweet=df.iloc[i]["text"]
            create_date= df.iloc[i]["create_date"]
            author_location= df.iloc[i]["author_location"]
            full_name= df.iloc[i]["full_name"]
            lang= df.iloc[i]["lang"]
            iso_lang= df.iloc[i]["iso_lang"]
                     
            a = Node("Twittos", name=author, tweet=tweet, create_date=str(create_date), full_name=full_name, author_location=author_location, lang=lang, iso_lang=iso_lang)
            tx.create(a)
            tx.commit()
          
            if RETWEET_ONLY:
                tweets_id=df.index[i]
                df = Create_Retweet_Link(api, tweets_id, a, author, df)
            else:
                followers = getFollowers(api, author, ENTRY_FOLLOWER)
                Create_Relationship(api, followers, a, author)
    return df

def Create_Retweet_Link(api, id_tweet, userA, entry_user, main_Df ):         
#    print u"Il y a " + str( len(tweets_id)) + u" tweets dans la liste des tweets"
    #Connexion à la base NEO4J perso    
    graph = Graph(password='martin')    

    Check_Limit_API(api)
    print time.ctime() # On affiche l'heure à chaque tweet qu'on traite pour voir l'avancement
    results = api.retweets( id_tweet, count=MAX_RETWEETS )
    print u"Il y a " + str( len(results)) + u" retweets dans la liste des retweets" 
    
    for r in results:
        dic = Create_Unique_Retweet_link(graph, r, userA, main_Df)
        main_Df=main_Df.append(Connect_tweepy.dict_to_df(dic))
    return main_Df   
def Create_Relationship(api, df_Followers, userA, entry_user):
    print u"Il y a " + str( len(df_Followers)) + u" tuples dans la liste des followers"
    #Connexion à la base NEO4J perso
    graph = Graph(password='martin')
    
    for f in df_Followers :   
        userB = Create_Unique_Relationship(graph, f, userA)        
        Followers_of_Followers(api, f, userB)

def Create_Unique_Relationship(graph, f, entry_Node):
        author=f.screen_name
        create_date= f.created_at
        author_location= f.location
        full_name= f.name
        friends_count=f.friends_count
        followers_count=f.followers_count
        statuses_count=f.statuses_count
        tx = graph.begin()
        userB=graph.find_one('Twittos', 'name', author)
        followB=graph.find_one('follower', 'name', author)
        
        if userB==None and followB==None: #author n'existe pas dans le graphe, on le crée
            b = Node('follower', name=author, create_date=str(create_date), full_name=full_name, author_location=author_location, \
            friends_count=friends_count, followers_count=followers_count, statuses_count=statuses_count)
            ab = Relationship(entry_Node, "EST SUIVI PAR", b)

        else: #author existe dans le graphe, il est contenu dans le selector "selected"
            if userB==None:
                b=followB
                ab = Relationship(entry_Node, "EST SUIVI PAR", b)
            else :
                b=userB
                ab = Relationship(entry_Node, "EST SUIVI PAR", b)
        
        tx.create(ab)
        tx.commit()
        return b

def Create_Unique_Retweet_link(graph, tweet, entry_Node, main_Df):
        
        author=tweet.author.screen_name
        create_date= tweet.created_at
        author_location= tweet.user.location
        lang=tweet.user.lang
#        iso_lang=tweet.metadata["iso_language_code"]
        full_name= tweet.user.name
#        friends_count=tweet.friends_count
#        followers_count=tweet.followers_count
#        statuses_count=tweet.statuses_count
        tx = graph.begin()
        userB=graph.find_one('Twittos', 'name', author)
        followB=graph.find_one('Retweeter', 'name', author)
        
        dic={}
        dic["author"]=author
        dic["create_date"]= create_date
        dic["author_location"]= author_location
        dic["full_name"]= full_name
        text=tweet.text.encode('utf-8')
        dic["text"]=text
        dic["id_tweet"]=tweet.id
        dic["lang"]=lang
#        dic["iso_lang"]=iso_lang
        dic["retweet_count"]=1
        
        
        
        
        if userB==None and followB==None: #author n'existe pas dans le graphe, on le crée
            b = Node('Retweeter', name=author, create_date=str(create_date), full_name=full_name, author_location=author_location, lang=lang)
            ab = Relationship(entry_Node, "A ETE RETWEET PAR", b)
           
        else: #author existe dans le graphe, il est contenu dans le selector "selected"
            if userB==None:
                b=followB
                ab = Relationship(entry_Node, "A ETE RETWEET PAR", b)
            else :
                b=userB
                ab = Relationship(entry_Node, "A ETE RETWEET PAR", b)
        
        tx.create(ab)
        tx.commit()
        return dic


   
def getFollowers(api, nickname, count=20):
    #Récupérer les followers d'un utilisateur donné (id ou screen_name)   
    try:
        followers = api.followers(nickname , count=count)
    except tweepy.TweepError:
        print(u"L'utilisateur "+ nickname + u" semble avoir protégé son compte, Skipping...")    
        return []
    return followers
         
def Check_Limit_API(api):
    data = api.rate_limit_status()

    remain_follow=data['resources']['followers']['/followers/list']
    remaining=remain_follow['remaining']
    
    remain_retweet=data['resources']['statuses']['/statuses/retweets/:id']
    remaining_retweet=remain_retweet['remaining']  
    
    if(remaining == 0 and not (RETWEET_ONLY) ): #Nous n'avons plus de requêtes pour les followers
        reset_time= time.ctime(int(remain_follow['reset']) )
        attente= remain_follow['reset'] - time.time()
        print (u"il n'y a plus de requêtes disponible pour les followers, il faut attendre jusqu'à " + reset_time)
        time.sleep(int(attente+1))
    
    if(remaining_retweet == 0 and RETWEET_ONLY): #Nous n'avons plus de requêtes pour la récupération des retweets
        reset_time= time.ctime(int(remain_retweet['reset']) )
        attente= remain_retweet['reset'] - time.time()
        print (u"il n'y a plus de requêtes disponible pour les retweets, il faut attendre jusqu'à " + reset_time)
        time.sleep(int(attente+1))
    
    return 0
    
def FollowersScreeNametoList(followers):
    #Renvoie les followers en liste
    l=[]    
    for f in followers:
        l.append(f.screen_name)
    return l

def FollowersLocationtoList(followers):
    #Renvoie les followers en liste
    l=[]    
    for f in followers:
        l.append(f.location)
    return l

def Followers_of_Followers(api, tree, node):
    # cette fonction va récupérer les followers des followers des gens qui ont cité le(s) mot(s) clé(s)
#    i=0
        Check_Limit_API(api)
        followers = getFollowers(api, tree.screen_name, FOLLOWERS_of_FOLLOWER)
        
        print u"Il y a " + str( len(followers)) + u" tuples dans le fichier des followers"

        #Connexion à la base NEO4J perso
        graph = Graph(password='martin')
        
        for f in followers :
            Create_Unique_Relationship(graph, f, node)

def Screen_NametoList(api,nickname, count=20):
    #Renvoie les followers en liste à partir du nickname
    name=[]
    location=[]    
    followers = getFollowers(api, nickname, count)
    if followers==[]:
        return []
    for f in followers:
        name.append(f.screen_name)
        location.append(f.location)
    return name, location

def Screen_NametoDic(api, nickname, dic, count=20):
    #Ajoute les followers au dictionnaire passé en argument à partir du nickname
    if not (nickname in dic.keys()):
        followers = getFollowers(api, nickname, count)
        dic[nickname]=FollowersScreeNametoList(followers)
        
    return dic

def WriteTree(tree):
    #Ecrit le contenu de l'arbre des relations dans un fichier CSV
    with open('tree.csv', 'wb') as csvfile:
#    fieldnames = ['first_name', 'last_name']
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)    
        for key, list_follow in tree.items():    
            writer.writerow(list_follow)
            
#On éxécute le main
main()