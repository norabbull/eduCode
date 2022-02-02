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

import numpy as np
import matplotlib.pyplot as plt
import random
from sim_person import Person

from matplotlib.animation import FuncAnimation
import time
# Enable interactive plot (jupyter)
#%matplotlib notebook


    
    
#%%



##################################################################
##  Startverdier - ENDRE PARAMETRE HER
##################################################################


tid = 300                    # antall uker vi simulerer
N = 1000                     # antall personer i populasjonen
start_smittede = 1           # prosentandel infiserte individer ved start (0-100%)
kontaktrate = 60             # smittsomhets radius (0-100)
p_smittsomhet = 70           # smittsomhet - sannsynlighet for å overføre sykdom (0-100%)
karantene = 0                # prosentandel av populasjon i karantene (0-100%)
tid_infeksjon = 15           # Tid det tar å bli frisk igjen (0-uendelig)
sykehuskapasitet = 200       # Antall personer som kan legges inn på sykehus
fart = "tilfeldig"           # 1 - 300. Alternativ: "tilfeldig"
immunitet = 20               # Antall immunitetsdager
andel_vaksinerte = 20        # Prosentandel av befolkningen som er vaksinerte


##################################################################
##  TEST-SETT:
##################################################################

# tid = 300                   # antall uker vi simulerer
# N = 1000                    # antall personer i populasjonen
# start_smittede = 1          # prosentandel infiserte individer ved start (0-100%)
# kontaktrate = 60            # smittsomhets radius
# p_smittsomhet = 70          # smittsomhet. sannsynlighet for å overføre sykdom (0-100%)
# karantene = 70              # prosentandel av populasjon i karantene (0-100%)
# tid_infeksjon = 15          # Tid det tar å bli frisk igjen (0-uendelig)
# sykehuskapasitet = 200      # Antall personer som kan legges inn på sykehus
# fart = "tilfeldig"          # 1 - 300. Alternativ: "tilfeldig"
# immunitet = 20              # Antall immunitetsdager
# andel_vaksinerte = 20       # Prosentandel av befolkningen som er vaksinerte



##################################################################
##  IKKE ENDRE KODEN UNDER'
##################################################################

start_smittede = int(N * start_smittede / 100)
karantene = int(N * karantene / 100)
andel_vaksinerte = int(N * andel_vaksinerte / 100)

S = [N - start_smittede]
I = [start_smittede]
R = [0]
t = [0]
R_tallet = [0]

# Opprett populasjon:
# sett alle populasjon på tilfeldige posisjoner. Infiser noen. 
populasjon = []

for i in range(N):
    
    if fart == "tilfeldig": 
        fart = (np.random.random() + 0.5) * 100
    else: 
        fart = fart
    
    # Legge til person i populasjonen
    p = Person(i, 
               fart = fart, 
               tid_infeksjon = tid_infeksjon, 
               tid_immunitet = immunitet)
    populasjon.append(p)
    
# Smitt tilfeldige personer (antall like mange som smittede) og infiser
for p in random.sample(populasjon, start_smittede): 
    p.infiser(0)
    
# Sett et visst antall folk i karantene
for p in random.sample(populasjon, karantene):
    p.sett_karantene()


##################################################################
##  Grafikk / animasjon 
##################################################################

# Opprett grafikk

fig = plt.figure(figsize=(20,40))
plot1 = fig.add_axes([0.1,0.1,0.4,0.8])
plot2 = fig.add_axes([0.55,0.46,0.4,0.4])
plot3 = fig.add_axes([0.55,0.15,0.4,0.2])

plot1.axis('off')
plot2.axis([0,tid,0,N+10])
plot3.axis([0,tid,0,2])

scatt = plot1.scatter([p.posX for p in populasjon],
                 [p.posY for p in populasjon],
                 c='green',
                 s=20)

fig2 = plt.Rectangle((0,0),100,100,fill=False)
plot1.add_patch(fig2)

plt_infiserte, = plot2.plot(start_smittede,color="red",label="Infiserte")
plt_friskmeldte, = plot2.plot(start_smittede,color="lightblue",label="Friskmeldte")
plt_mottakelige, = plot2.plot(N,color="green",label="Mottakelige")
plt_R_tallet, = plot3.plot(R_tallet[0], color = "indigo", label = "R-tallet")
plot2.axhline(sykehuskapasitet, color = "orange", label = "sykehuskapasitet")
plot2.legend(handles = [plt_friskmeldte,plt_infiserte, plt_mottakelige, plt_R_tallet])
plot2.set_xlabel("Tid", fontsize = 15, fontweight = 'bold')
plot2.set_ylabel("Mennesker", fontsize = 15, fontweight = 'bold')
plot3.set_xlabel("Tid", fontsize = 15, fontweight = 'bold')
plot3.set_ylabel("R-tallet", fontsize = 15, fontweight = 'bold')


##################################################################
##  Simuler og animer verdier
##################################################################

# animer - oppdater verdier for hele populasjon og oppdater plottene
def animer(frame, S, I, R, t, populasjon, kontaktrate):

    smittede = 0
    friskmeldt = 0
    farger = []                             # grafikk
    størrelser = [20 for p in populasjon]   # grafikk
    kontaktrate = kontaktrate * 0.06
    
    for p in populasjon:
        
        # sjekk hvor lenge personen har vært syk
        p.oppdater_status(frame)
                       
        # animer forflytning for hver person
        p.oppdater_posisjon()
                
        # sjekk om det er personer i nærheten av en syk person og infiser alle
        # innen infeksjonsradiusen (gitt sannsynlighet for smitte)
        if p.infisert:
            for p2 in populasjon:
                if p2.indeks == p.indeks or p2.infisert or p2.friskmeldt: 
                    pass
                else:
                    d = p.hent_dist(p2.posX, p2.posY)
                    if d < kontaktrate:
                        if np.random.random() < p_smittsomhet / 100:
                            p2.infiser(frame)
                            størrelser[p2.indeks] = 80
                            
        if p.friskmeldt:
            friskmeldt += 1 # tell antall friskmeldte
        if p.infisert:
            smittede += 1 # tell antall infiserte
        
        farger.append(p.hent_farge())  # endre farge til person
        
    R_tall = (smittede - I[-1]) / I[-1]  # Gamle smittede / nye smittede  
    
    #oppdater plottene
    I.append(smittede)
    R.append(friskmeldt)
    S.append(S[0]-I[-1])
    t.append(frame)
    R_tallet.append(R_tall)


    # Overfør data to the matplotlib grafikk
    offsets=np.array([[p.posX for p in populasjon],
                     [p.posY for p in populasjon]])
    scatt.set_offsets(np.ndarray.transpose(offsets))
    scatt.set_color(farger)
    scatt.set_sizes(størrelser)
    plt_infiserte.set_data(t,I)
    plt_friskmeldte.set_data(t,R)
    plt_mottakelige.set_data(t,S)
    plt_R_tallet.set_data(t,R_tallet)
    #time.sleep(0.1)
    return scatt,plt_infiserte,plt_friskmeldte, plt_mottakelige, plt_R_tallet



##################################################################
##  Kjør simulasjonen
##################################################################

animation = FuncAnimation(fig, 
                          animer,
                          frames = tid,
                          interval = 200,
                          fargs = (S,I,R,t,populasjon,kontaktrate),
                          blit = False,
                          repeat = False)
plt.show()
