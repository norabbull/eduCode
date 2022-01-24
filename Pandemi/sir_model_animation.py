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
# Enable interactive plot (jupyter)
#%matplotlib notebook


    
    
#%%

# Startverdier

tid = 200                # antll uker vi simulerer
N = 500                  # antall personer i populasjonen
p_start_smittede = 1     # prosentandel infiserte individer ved start (0-100%)
start_smittede = int(N * p_start_smittede / 100)

kontaktrate = 2          # smittsomhets radius. (i pixler, 0-100).
p_smittsomhet = 100      # smittsomhet. sannsynlighet for å overføre sykdom (0-100%)

p_karantene = 30         # prosentandel av populasjon i karantene (0-100%)
start_karantene = int(N * p_karantene / 100)

tid_syk = 10             # Tid det tar å bli frisk igjen (0-uendelig)

S = [N-start_smittede]
I = [start_smittede]
R = [0]
t = [0]

fart = 200             # 1 - 300. Alternativ: "tilfeldig"



# Opprett populasjon:
# sett alle populasjon på tilfeldige posisjoner. Infiser noen. 
populasjon = []

for i in range(N):
    
    if fart == "tilfeldig": 
        (np.random.random()+0.5) * 100
    else: 
        fart = fart
    
    # Legge til person i populasjonen
    p = Person(i, fart, tid_syk)
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
