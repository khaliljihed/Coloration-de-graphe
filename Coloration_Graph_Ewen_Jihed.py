
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 20:53:14 2021

@author: jihed
"""
#Les import nécessaire au projet

#tknter est la bibliothèque graphique qui nous permet d'afficher les graphes
from tkinter import *
import numpy as np
#graphviz est la bibliothèque qui permet le traçage des graphes
from graphviz import Graph
import pylab
#Pour enrgistrer les graphs
from PIL import ImageTk, Image
import random
#Pour colorer les graphes
import webcolors 

#Déclaration des variables globales
global photo
global photo1
g = Graph('G', filename='process.png',format='png')
listNoeud=[]
maxi=1
l2,l1,c1,c2=0,0,0,0


#************************ Fonctions  *****************************
#cette fonction permet de récupérer l'opération choisie (insertion manuelle de graphe, graphe aléatoire)
def getOperation():
    return variable.get()

def maximum(x,y) :
    if x>y :
        return(x)
    else :
        return(y)

#Cette fonction génère un graph aléatoire, connexe et sans cycle 
#Ce graphe n'est pas forcément planaire
def arbitaryGraph(nodes, numberEdges):
    l=list(range(1,nodes+1))
    #S est l'ensemble des noeuds non connéctés 
    #T est l'ensemble des noeuds connectés 
    S, T = set(l), set()
    # Choisir arbitrairement un noeud et le conncter au reste du graphe
    current_node = random.sample(S, 1).pop()
    S.remove(current_node)
    T.add(current_node)
    # Creer le graph. liste est la liste des arêtes
    liste=[]
    while S:
        neighbor_node = random.randint(1, nodes)
        while(neighbor_node==current_node):
            neighbor_node = random.randint(1, nodes)
        if neighbor_node not in T:
            edge = str(current_node)+' '+ str(neighbor_node)
            liste.append(edge)
            S.remove(neighbor_node)
            T.add(neighbor_node)
            # le nouveau sommet est le nouveau sommet voisin.
            current_node = neighbor_node
            numberEdges-=1
    # jusqu'ici le graph est connexe, sans cycle (une succession de noeuds => donc planaire) 
    #S'il nous reste des arêtes à rajouter, la boucle suivante le fera. 
    for i in range(numberEdges):
                
        n1=random.randint(1, nodes)
        n2=random.randint(1, nodes)
        while((n1==n2) or (str(n1)+ ' '+ str(n2) in liste) or (str(n2)+ ' '+ str(n1) in liste)):
            n1=random.randint(1, nodes)
            n2=random.randint(1, nodes)
        line = str(n1)+ ' '+ str(n2)
        liste.append(line)
    return liste

#Cette fonction permet d'inserer une arete à l'aide de l'interface graphique
def edgeInsert():
        global listNoeud
        global maxi
        value=getOperation()
        if ((value=='Manuel')):
            try:
                l1=int(entry1.get("1.0",'end-1c'))
                c1=int(entry2.get("1.0",'end-1c'))
                assert l1>0 and c1>0
                L =str(l1)+' '+str(c1)
                L2=str(c1)+' '+str(l1)
                assert(L not in listNoeud) and (L2 not in listNoeud)# and((l1<=maxi+1 and c1<=maxi) or(l1<=maxi and c1<=maxi+1))
            except:
                if (l1==c1):
                    insertError('Il ne faut pas avoir de cycle')
                elif not((l1<=maxi+1 and c1<=maxi) or(l1<=maxi and c1<=maxi+1)):
                    insertError('Les noeuds doivent etre ordonnée et les indices successifs')
                else :
                    insertError('arete existe déjà')
                entry1.delete('1.0')
                entry2.delete('1.0')
                return
        if maxi<maximum(l1,c1):
            maxi=maximum(l1,c1)
        
        listNoeud.append(L)
        entry1.delete('1.0')
        entry2.delete('1.0')
        insertHint(' | '.join(listNoeud))
        
#Cette fonction permet d'afficher le premier graph non coloré        
def afficherGraph():
    global listNoeud
    global l2
    global photo
    for line in listNoeud :
        x=line.split()
        g.edge(x[0],x[1])
    filename = g.render(filename='img/g1')
    pylab.savefig('graph.png')
    image = Image.open('img/g1.png')
    if (image.size[0]>image.size[1]):
        au=image.size[0]
        au1=image.size[1]
        v=int((400/au)*au1)
        image=image.resize((400,v))
    else :
        au=image.size[0]
        au1=image.size[1]
        v=int((400/au1)*au)
        image=image.resize((v,400))
    canvas = Canvas(frame31, width =500, height = 500)      
    canvas.pack()  
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0,0, anchor=NW, image=photo)
    graphColorFinal()      

def calculnodesnumber(l):
    ls=[]
    for line in l:
        x=int(line.split()[0])-1
        y=int(line.split()[1])-1
        if x not in ls:
            ls.append(x)
        if y not in ls:
            ls.append(y)
    ls=sorted(ls)
    return(len(ls))

def liste_voisin(noeud):
    global listNoeud
    L=[]
    for i in range(len(listNoeud)):
        x=listNoeud[i].split()
        if (int(x[0])==noeud):
            L.append(int(x[1]))
        elif (int(x[1])==noeud):
            L.append(int(x[0]))
    return L


#Avec r=0.5, nous avons repris la même fonction f
def f(v,rand):
    S=1/(1+np.exp(-v))
    if ( rand>0.5 and rand<S):
        return 0
    if ( rand<0.5 and rand<S):
        return 1
    if ( rand<=0.5 and rand>=S):
        return 2
    if ( rand>=0.5 and rand>=S):
        return 3


#Algorithme de coloration de graph, version modifié pour tout les graphes
def graphColorAlgorithm():
    global l2
    global listNoeud
    global photo1
    global maxi
    #pour le cas manuel
    
    nodes=l2
    if (getOperation()=='Manuel'):
        nodes=maxi
    color=[]
    mat=np.zeros((nodes,nodes), dtype=int)
    color=[nodes] * nodes
    #Créer la matrice du graphe remplie de 1 s'il y'a une connexion entre i et j , 0 sinon
    for line in listNoeud:
        x=int(line.split()[0])-1
        y=int(line.split()[1])-1
        mat[x][y]=1 
        mat[y][x]=1
    #print(mat)
    #la fitness d'un noeud est le nombre de noeuds voisin ayant la même couleur que lui
    #ainsi la fitness d'un noeud est donée par "color_neighbors[i].count(color[i])"
    #la fitness du graphe est le maximum des ftness de tout ses noeuds
    done=False
    color_neighbors=[] 
    for i in range(nodes):
        color_neighbors.append([])
    while(not done):
        for i in range(nodes):
            color_neighbors[i]=[]
            for j in range(nodes):
                if mat[i][j]==1:
                    color_neighbors[i].append(color[j]) 
        max=0
        indexMax=-1
        for i in range(nodes):
            if max<color_neighbors[i].count(color[i]):
                max=color_neighbors[i].count(color[i])
                indexMax=i
        if indexMax==-1:
            done=True # if no node have same color as its neighbors than done!
        else:
            color[indexMax]=color[indexMax]-1 # else node change its color
    print(color)
    print(color_neighbors)
    return color


#algorithme de coloration de graphes planaire - MPSO
def graphColorAlgorithmMPSO():
    global l2
    global listNoeud
    global photo1
    global maxi
    #pour le cas manuel
    
    nodes=l2
    if (getOperation()=='Manuel'):
        nodes=maxi
    if getOperation()=="MPSO":
        nodes=calculnodesnumber(listNoeud)
        print(nodes)
    mat=np.zeros((nodes,nodes), dtype=int)
    color=[random.randint(0,3 ) for i in range(nodes)]
    #Créer la matrice du graphe remplie de 1 s'il y'a une connexion entre i et j , 0 sinon
    for line in listNoeud:
        x=int(line.split()[0])-1
        y=int(line.split()[1])-1
        mat[x][y]=1 
        mat[y][x]=1
    #print(mat)
    #la fitness d'un noeud est le nombre de noeuds voisin ayant la même couleur que lui
    #ainsi la fitness d'un noeud est donée par "color_neighbors[i].count(color[i])"
    #la fitness du graphe est le maximum des ftness de tout ses noeuds
    done=False
    color_neighbors=[] 
    for i in range(nodes):
        color_neighbors.append([])
    V=[0 for i in range(nodes)]
    w=0.7  #le coefficient dâ€™inertie qui contrÃ´le la contribution de la vÃ©locitÃ©
    c1=0.3 #coefficient en rapport avec pbest
    c2=0.4 #coefficient en rapport avec gbest
    while(not done):
        for i in range(nodes):
            color_neighbors[i]=[]
            for j in range(nodes):
                if mat[i][j]==1:
                    color_neighbors[i].append(color[j]) 
        for i in range(len(color)):
            L=liste_voisin(i+1)
            g=random.choice(L)-1
            rand=random.random()
            V[i]=w*V[i]+c1*rand*(color_neighbors[i].count(color[i])-color[i])+c2*rand*(color[g]-color[i])
            color[i]= (color[i]+f(V[i],rand))%4
        for i in range(nodes):
            color_neighbors[i]=[]
            for j in range(nodes):
                if mat[i][j]==1:
                    color_neighbors[i].append(color[j]) 
        max=0
        for i in range(nodes):
            if max<color_neighbors[i].count(color[i]):
                max=color_neighbors[i].count(color[i])
        print("**********************************")
        print(color)
        print(color_neighbors)
        if (max==0):
            done=True

        '''
        max=0
        indexMax=-1
        for i in range(nodes):
            if max<color_neighbors[i].count(color[i]):
                max=color_neighbors[i].count(color[i])
                indexMax=i
        if indexMax==-1:
            done=True # if no node have same color as its neighbors than done!
        else:
            color[indexMax]=color[indexMax]-1 # else node change its color'''
    for i in range(len(color)):
        color[i]+=1
    print(color)
    return color

def graphColorFinal():
    global l2
    global listNoeud
    global photo1
    nodes=l2
    global maxi
    value=getOperation()
    if (getOperation()=='Manuel'):
        nodes=maxi
    if value=="MPSO":
        color=graphColorAlgorithmMPSO()
    else :
        color=graphColorAlgorithm()
    g1 = Graph('G', filename='process2.png',format='png')
    if (getOperation()!='MPSO'):
        for i in range(len(color)):
            color[i]=nodes-color[i]
    listcolor={}
    s=max(color)
    for i in range(s+1):
        x=webcolors.rgb_to_hex((random.randint(1,255), random.randint(1,255), random.randint(1,255)))
        listcolor[i]=x
    for line in listNoeud :
        x=line.split()
        g1.edge(x[0],x[1])
    for j in range(len(color)):
        g1.node(str(j+1), style='filled', fillcolor=listcolor[color[j]])
    g1.attr(fill="#d9d9d9", style="filled")
    filename = g1.render(filename='img/graph2')
    pylab.savefig('graph2.png')
    image1 = Image.open('img/graph2.png')
    if (image1.size[0]>image1.size[1]):
        au=image1.size[0]
        au1=image1.size[1]
        v=int((400/au)*au1)
        image1=image1.resize((400,v))
    else :
        au=image1.size[0]
        au1=image1.size[1]
        v=int((400/au1)*au)
        image1=image1.resize((v,400))
    #image = image.resize((750, 700))
    canvas = Canvas(frame32, width =500, height = 500)      
    canvas.pack()  
    photo1 = ImageTk.PhotoImage(image1)
    canvas.create_image(0,0, anchor=NW, image=photo1)
    insertHint("Nombre chromatique = "+str( max(color)+1))
            
#this function prints and returns the operation choice
def genererGraphAleatoire():
    global listNoeud
    global l2
    global c2
    value=getOperation()
    if value=="MPSO":
        insertHint("lecture du graphe à partir de graphe.txt")
        file1 = open('graphe.txt', 'r')
        listNoeud = file1.readlines() 
        for i in range(len(listNoeud)):
            listNoeud[i]=listNoeud[i][:-1]
        print(listNoeud)
               
    else:
        try:
            l2=int(entry3.get("1.0",'end-1c'))
            c2=int(entry4.get("1.0",'end-1c'))
            assert l2>0 and l2-2<c2<((l2*(l2-1)/2)+1)
        except:
            insertError("Nombre d'arcs maximal est {nm}:".format(nm= l2*(l2-1)/2))
            reset()
            return
        listNoeud=arbitaryGraph(l2,c2)
    afficherGraph()

def onOperationSelection(value):
    if ((value=='Manuel')):
        frame22Bis.forget()
        frame22Bis1.forget()
        frame22.pack(fill="x" ,pady=(0,6))
        frame21.forget()
        insertHint('Insérer les arêtes ligne par ligne, les aretes doivent etre ordonnées el graphe connexe ')

    elif (value=='Générer un graphe aléatoire' ):
        frame22.forget()
        frame22Bis1.forget()
        frame22Bis.pack(fill="x" ,pady=(0,6))
        frame21.forget()
        insertHint('Lecture du graphe à partir du fichier graphe.txt ')
    elif ( value=="MPSO"):
        frame22.forget()

        frame22Bis1.pack(fill="x" ,pady=(0,6))
        frame21.forget()
        frame22Bis.forget()

#this function takes the Error text (String) and display in it's section
def insertError(ErrorString):
    ErrorStringV.set(ErrorString)
    try:
        frame33.grid_forget()
    except:
        pass
    

#this function takes the Error text (String) and display in it's section
def insertHint(HintString):
    hintStringV.set(HintString)
    try:
        frame33.grid_forget()
    except:
        pass

#****************************** the interface *********************************
root = Tk()

root.title('Coloration de graphe')
root.configure(background="#686868")
frame=Frame(root, width="1280",height="720",bg="#686868")  #frame=Frame(root,width="550",height="500")
frame.pack_propagate(0)
frame.pack(padx=25,pady=(25,0),fill="both")  #frame.pack(padx=25,pady=25,fill="both")


frame2=Frame(frame ,bg="#686868")
frame2.pack(fill="x",pady=(0,0))
label2=Label(frame2,text="choisir le mode d'insertion de graphe",bg="#686868",fg="black",pady=5, padx=5)
label2.config(font=("Arial 14", 12,"bold"))
label2.pack(side=LEFT)
options = ('Manuel', 'Générer un graphe aléatoire', 'MPSO')
variable = StringVar(root)
variable.set("operation") # default value
w = OptionMenu(frame2, variable, *options,command=onOperationSelection)
w.config(width=13)
w.pack(side=LEFT)


#multiplication frame
frameSize=Frame(frame,bg="#686868" )
frameSize.pack()
frame21=Frame(frameSize,bg="#686868" )
#frame21.pack()
entry1=Text(frame21,width=4,height=2,bg="white")
entry2=Text(frame21,width=4,height=2,bg="white")
entry1.grid(row=0,column=1)
entry2.grid(row=0,column=3)


frame22=Frame(frameSize,bg="#686868" )
frame22.config(width=800, height=200)
frame22Bis=Frame(frameSize,bg="#686868" )
frame22Bis.config(width=800, height=200)
frame22Bis1=Frame(frameSize,bg="#686868" )
frame22Bis1.config(width=800, height=200)
labell1=Label(frame22,text="Le premier noeud:",bg="#686868",fg="white")
labell1.grid(row=0,column=0)
labelc1=Label(frame22,text="le deuxieme noeud:",bg="#686868",fg="white")
labelc1.grid(row=0,column=2)
#frame22.pack(fill="x" ,pady=(0,6))
labell1Bis=Label(frame22Bis,text="Nombre de noeuds:",bg="#686868",fg="white")
labell1Bis.grid(row=0,column=0)
labelc1Bis=Label(frame22Bis,text="Nombre d'arcs':",bg="#686868",fg="white")
labelc1Bis.grid(row=0,column=2)
entry2=Text(frame22,width=4,height=2,bg="white")
entry1=Text(frame22,width=4,height=2,bg="white")
entry2.grid(row=0,column=1)
entry1.grid(row=0,column=3)
entry3=Text(frame22Bis,width=4,height=2,bg="white")
entry4=Text(frame22Bis,width=4,height=2,bg="white")
entry3.grid(row=0,column=1)
entry4.grid(row=0,column=3)
InsertButton=Button(frame22, text="Insérer", bg="khaki", fg="black", command=edgeInsert)
#resButton.pack(pady=(12,12))
InsertButton.config( height = 1, width = 8 )
InsertButton.config(font=("Arial 14", 10))
InsertButton.grid(row=0,column=7, padx=10, pady=10)
endButton=Button(frame22, text="Fin", bg="red", fg="black", command=afficherGraph)
endButtonBis=Button(frame22Bis, text="Fin", bg="IndianRed3", fg="black", command=genererGraphAleatoire)
endButtonBis1=Button(frame22Bis1, text="Calcul graphe", bg="IndianRed3", fg="black", command=genererGraphAleatoire)

#resButton.pack(pady=(12,12))
endButton.config( height = 1, width = 8 )
endButton.config(font=("Arial 14", 10))
endButton.grid(row=0,column=8, padx=10, pady=10)
endButtonBis.config( height = 1, width = 8 )
endButtonBis.config(font=("Arial 14", 10))
endButtonBis.grid(row=0,column=8, padx=10, pady=10)
endButtonBis1.config( height = 1, width = 12 )
endButtonBis1.config(font=("Arial 14", 10))
endButtonBis1.grid(row=0,column=8, padx=10, pady=10)
#****** matrices ******
frame3=Frame(frame)
frame3.pack()
#***matrix1***
#*section1*(the first matrix)
frame31=Frame(frame3,bg="#d9d9d9",width=683,height=500)
frame31.pack_propagate(False)
frame31.grid(row=0,column=0,padx=(0,7))    #frame31.pack(side=LEFT,padx=(0,7))
label311=Label(frame31,text="Graphe d'origine",fg="#686868",bg="#d9d9d9")
label311.config(font=("Arial 14",13,"bold"))
label311.pack(pady=(16,16))


#*section2*
frame314=Frame(frame31)
frame314.pack()

#***matrix2***
#*section1*
frame32=Frame(frame3,bg="#d9d9d9",width=683,height=500)
frame32.pack_propagate(False)
#frame32.pack(side=LEFT)
frame32.grid(row=0,column=1)
label321=Label(frame32,text="Graphe coloré",fg="#686868",bg="#d9d9d9")
label321.config(font=("Arial 14",13,"bold"))
label321.pack(pady=(16,16))
frame324=Frame(frame32)
frame324.pack()

#****** Erros ******
frame4=Frame(frame ,bg="IndianRed3")
frame4.pack(fill="x",pady=(6,12))

label40=Label(frame4, text="Errors:",bg="IndianRed3",fg="white",pady=5,anchor=W)
label40.config(font=("Arial 14", 14,"bold"))
label40.pack(side=LEFT,padx=(15,0))

ErrorStringV = StringVar()
label4=Label(frame4, textvariable=ErrorStringV,bg="IndianRed3",fg="white",pady=5,anchor=W,padx=2)
label4.config(font=("Arial 14", 12,"bold"))
label4.pack(side=LEFT)

#****** Hints or small results ******
frame5=Frame(frame ,bg="DarkSeaGreen")
frame5.pack(fill="x",pady=(0,0))

label50=Label(frame5,text="Hints:",bg="DarkSeaGreen",fg="white",pady=5,anchor=W)
label50.config(font=("Arial 14", 14,"bold"))
label50.pack(side=LEFT,padx=(15,0))

hintStringV= StringVar()
label5=Label(frame5,textvariable=hintStringV,bg="DarkSeaGreen",fg="white",pady=5,anchor=W,padx=2)
label5.config(font=("Arial 14", 12,"bold"))
label5.pack(side=LEFT)

root.mainloop()

 
