# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 20:42:26 2022

@author: norab

Utvidelsesideer: 
    
    - Sette i karantene
    - Bli smittet på nytt
    - Bli vaksinert
    - Sette i kohort
    - Vaksinasjonsgrad
    - R - tallet
        - Tell antall personer som smittes videre av en person. 
        Kan dermed regne R - tallet for de ulike parametrene!
    
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import random

from matplotlib.animation import FuncAnimation
# Enable interactive plot (jupyter)
#%matplotlib notebook

class Person:
    def __init__(self,i, posX, posY, fart, tid_syk):
        """
        
        Tid regnes i "frames" som betyr en "runde" i simulasjonen.
        Dette kan for eksempel tilsvare en time, en dag eller en uke, 
        avhengig av sykdommen. 
        
        """
        
        #ID and name
        self.indeks = i
        self.navn = "Person " + str(i)
        
        #Status: Mottakelig, infisert eller friskmeldt
        self.mottakelig = True   # S
        self.infisert = False    # I
        self.friskmeldt = False  # R
        self.tid_infisert = -1        # "tidspunkt" for infeksjon
        
        # Nåværende posisjon
        self.posX = posX 
        self.posY = posY
        
        # Målposisjon
        self.nyposX = np.random.random()*100
        self.nyposY = np.random.random()*100
        
        # Forflytningshastighet
        self.fart = fart
        
        self.karantene = False  # Karantene (forflyttes ikke)
        
        # Forflytning per iterasjon
        self.delta_posX = (self.nyposX - self.posX) / self.fart
        self.delta_posY = (self.nyposY - self.posY) / self.fart


        # infeksjonstid, tid det tar å bli frisk
        self.tid_syk = tid_syk

    def infiser(self,i):
        # Endre status til syk
        self.infisert = True
        self.mottakelig = False
        self.friskmeldt = False
        self.tid_infisert = i

    def helbred(self):
        # Endre status til frisk
        self.friskmeldt = True
        self.mottakelig = False
        self.infisert = False
        
    def oppdater_status(self,i):
        # Endre status til frisk dersom infeksjonstid er over
        if self.tid_infisert > -1:
            if (i - self.tid_infisert) > self.tid_syk:
                self.helbred()
                               
    def sett_målposisjon(self):
        # Sett ny målposisjon
        self.nyposX = np.random.random()*100
        self.nyposY = np.random.random()*100
        
        if self.karantene:
            self.delta_posX = 0
            self.delta_posY = 0
        else:
            self.delta_posX = (self.nyposX - self.posX) / self.fart
            self.delta_posY = (self.nyposY - self.posY) / self.fart
    
    def sett_karantene(self):
        self.karantene = True
        self.delta_posX = 0
        self.delta_posY = 0

    def oppdater_posisjon(self):
        # Animer forflytning fra posisjon til ny posisjon
        
        self.posX = self.posX + self.delta_posX
        self.posY = self.posY + self.delta_posY

        if abs(self.posX - self.nyposX) < 1 and abs(self.posY - self.nyposY) < 1:
            self.sett_målposisjon()

    def hent_farge(self):
        if self.infisert:
            return 'red'
        if self.mottakelig:
            return 'green'
        if self.friskmeldt:
            return 'lightblue'

    def hent_pos(self):
        return (self.posX, self.posY)

    def hent_dist(self,x,y):
        # kalkuler distanse mellom denne personen og en annen person
        return math.sqrt((self.posX - x)**2 + (self.posY - y)**2)
    
    
#%%

# Startverdier

tid = 200          # antll uker vi simulerer
N = 500                  # antall personer i populasjonen
p_start_smittede = 1         # prosentandel infiserte individer ved start (0-100%)
start_smittede = int(N * p_start_smittede / 100)

kontaktrate = 2         # smittsomhets radius. (i pixler, 0-100).
p_smittsomhet = 100       # smittsomhet. sannsynlighet for å overføre sykdom (0-100%)

p_karantene = 30        # prosentandel av populasjon i karantene (0-100%)
start_karantene = int(N * p_karantene / 100)

tid_syk = 10           # sykedager. Tid det tar å bli frisk igjen (0-uendelig)

S = [N-start_smittede]
I = [start_smittede]
R = [0]
t = [0]

# Opprett populasjon:
# sett alle populasjon på tilfeldige posisjoner. Infiser noen. 
populasjon = []
for i in range(N):
    posX = np.random.random()*100
    posY = np.random.random()*100
    fart = (np.random.random()+0.5)*100

    p = Person(i,posX, posY, fart, tid_syk)
    populasjon.append(p)
    
# Smitt tilfeldige personer (antall like mange som smittede) og infiser
for p in random.sample(populasjon, start_smittede): 
    p.infiser(0)
    
# Sett et visst antall folk i karantene
for p in random.sample(populasjon, start_karantene):
    p.sett_karantene()


# grafikk / animasjon
fig = plt.figure(figsize=(20,10))
plot1 = fig.add_subplot(1,2,1)
plot2 = fig.add_subplot(1,2,2)
plot1.axis('off')
plot2.axis([0,tid,0,N+10])

scatt = plot1.scatter([p.posX for p in populasjon],
                 [p.posY for p in populasjon],
                 c='green',
                 s=20)

fig2 = plt.Rectangle((0,0),100,100,fill=False)
plot1.add_patch(fig2)
plt_infiserte, = plot2.plot(start_smittede,color="red",label="Infiserte")
plt_friskmeldte, = plot2.plot(start_smittede,color="lightblue",label="Friskmeldte")
plt_mottakelige, = plot2.plot(N,color="green",label="Mottakelige")
plot2.legend(handles = [plt_friskmeldte,plt_infiserte, plt_mottakelige])
plot2.set_xlabel("Tid")
plot2.set_ylabel("Mennesker")


# animer - oppdater verdier for hele populasjon og oppdater plottene
def animer(frame,S, I, R,t, populasjon):
    smittede = 0
    friskmeldt = 0
    farger = []                             # grafikk
    størrelser = [20 for p in populasjon]   # grafikk
    
    for p in populasjon:
        # sjekk hvor lenge personen har vært syk
        p.oppdater_status(frame)
                       
        # animer forflytning for hver person
        p.oppdater_posisjon()
        if p.friskmeldt:
            friskmeldt += 1 # tell antall friskmeldte
        if p.infisert:
            smittede += 1 # tell antall infiserte
        
            
            # sjekk om det er personer i nærheten av en syk person og infiser alle
            # innen infeksjonsradiusen (gitt sannsynlighet for smitte)
            for person in populasjon:
                if person.indeks == p.indeks or person.infisert or person.friskmeldt: # Endre her om de skal kunne bli syke igjen
                    pass
                else:
                    d = p.hent_dist(person.posX,person.posY)
                    if d < kontaktrate:
                        if np.random.random() < p_smittsomhet / 100:
                            person.infiser(frame)
                            størrelser[person.indeks] = 80

        farger.append(p.hent_farge()) #change dot color according to the person's status

    #oppdater plottene
    I.append(smittede)
    R.append(friskmeldt)
    S.append(S[0]-I[-1])
    t.append(frame)


    # Overfør data to the matplotlib grafikk
    offsets=np.array([[p.posX for p in populasjon],
                     [p.posY for p in populasjon]])
    scatt.set_offsets(np.ndarray.transpose(offsets))
    scatt.set_color(farger)
    scatt.set_sizes(størrelser)
    plt_infiserte.set_data(t,I)
    plt_friskmeldte.set_data(t,R)
    plt_mottakelige.set_data(t,S)
    return scatt,plt_infiserte,plt_friskmeldte, plt_mottakelige

# run the animation indefinitely
animation = FuncAnimation(fig, 
                          animer,
                          frames = tid,
                          interval=200,
                          fargs=(S,I,R,t,populasjon),
                          blit=False,
                          repeat = False)
plt.show()
