# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 13:54:07 2022

@author: norab
"""

import math
import numpy as np


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