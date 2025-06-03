import math 
import pandas as pd

#---------- Utile en Beton Armée ---------#
class beton:
    def __init__(self,fck:int=25,coefficent_De_Majoration:int=1.5):
        self.fck = fck
        self.fcm = self.fck+8
        self.fcd = self.fck/coefficent_De_Majoration
        if self.fck<=50:
            self.fctm = 0.3*self.fck**(2/3)
        else:
            self.fctm = 2.12*math.log(1+self.fcm/10)
        self.Ecm = 22_000*(self.fcm/10)**0.3 
        
    def calcul_epsilon_cu(self):
        """Calcule la déformation ultime du béton en compression"""
        if self.fck <= 50:
            return 0.0035
        else:
            return 0.0026 + 0.035*((90-self.fck)/100)**4
            
    def calcul_epsilon_c2(self):
        """Calcule la déformation à la résistance maximale en compression"""
        if self.fck <= 50:
            return 0.002
        else:
            return 0.002 + 0.085*((self.fck-50)/100)**0.53
            
    def calcul_epsilon_c3(self):
        """Calcule la déformation à la résistance maximale en compression pour les sections rectangulaires"""
        if self.fck <= 50:
            return 0.00175
        else:
            return 0.00175 + 0.00055*((self.fck-50)/40)
            
    def calcul_lambda(self):
        """Calcule le coefficient lambda pour le calcul de la résistance en compression"""
        if self.fck <= 50:
            return 0.8
        else:
            return 0.8 - (self.fck-50)/400
            
    def calcul_eta(self):
        """Calcule le coefficient eta pour le calcul de la résistance en compression"""
        if self.fck <= 50:
            return 1.0
        else:
            return 1.0 - (self.fck-50)/200

class acier:
    def __init__(self,fyk:int=500,coefficent_De_Majoration:int=1.15):
        self.fyk = fyk 
        self.fyd = self.fyk/coefficent_De_Majoration
        self.E = 210_000
        
    def calcul_epsilon_yd(self):
        """Calcule la déformation de l'acier à la limite élastique"""
        return self.fyd/self.E
        
    def calcul_epsilon_uk(self):
        """Calcule la déformation ultime de l'acier"""
        if self.fyk <= 400:
            return 0.025
        elif self.fyk <= 600:
            return 0.02
        else:
            return 0.015
            
    def calcul_k(self):
        """Calcule le coefficient k pour le calcul de la résistance en traction"""
        if self.fyk <= 400:
            return 1.05
        elif self.fyk <= 600:
            return 1.08
        else:
            return 1.15
            
    def calcul_epsilon_ud(self):
        """Calcule la déformation de calcul de l'acier"""
        return min(0.9*self.calcul_epsilon_uk(), 0.02)
        
    def calcul_fctd(self):
        """Calcule la résistance de calcul en traction de l'acier"""
        return self.fyd/self.calcul_k()

class coefficient_de_majoration:
    def __init__(self,accidentelle:bool):
        if not accidentelle:
            self.beton = 1.5
            self.acier = 1.15
        else:
            self.beton = 1.2
            self.acier = 1 
            
class inertie:
    def __init__(self,forme:str,suivant_Y:bool=True):
        self.forme = forme 
        self.Y = suivant_Y
    def r(self,b,h):
        if self.Y:
            return (b*h**3)/12
        else:
            return (h*b**3)/12
    def c(self,d,angle):
        pass
    def T(self,bw,h,angle):
        pass
    def I(self,B,b,H,h):
        pass  
        

def proposition_de_barre(section:float=12.0):
    barre = [5,6,8,10,12,14,16,18,20,25,32,40] # Diammetre de la barre en mm
    nombre = []
    barre_possible = []
    for i in barre:
        n = 4*section/(math.pi*(i*0.1)**2)
        if 1<=n<=10 and type(n)==float:
            nombre.append(int(n)+1)
            barre_possible.append(i)
        elif 1<=n<=10 and type(n)==int:
            nombre.append(int(n)+1)
            barre_possible.append(i)
    return {key:value for key,value in zip(nombre,barre_possible)} 

def combinaison_de_barre(section:float=12.0,filtre:float=0.50): #Mbola misy erreur
    A = [1,2,3,4]
    B = [8,10,12,14,16,18,20,25,32,40]
    valeur_possible = []
    combinaison_possible = []
    for a in A:
        for b in B:
            for c in A:
                for d in B:
                    if (b==8 and d-b<=6)or(b==10 and -2<=d-b<=6)or(b==12 and -4<=d-b<=8)or(b==14 and -4<=d-b<=11)or(b==18 and -6<=d-b<=14)or(b==20 and -8<=d-b<=12)or(b==25 and -11<=d-b<=7)or(b==32 and -16<=d-b):
                        e = (a*(math.pi*b**2/4)+c*(math.pi*d**2/4))*0.01
                        combinaison_possible.append(f"{a}_HA_{b} + {c}_HA_{d}")
                        valeur_possible.append(e) 
    dictionnaire = {key:value for key,value in zip(valeur_possible,combinaison_possible)}
    Section_possible = []
    Combinaison_possible = []
    for i in valeur_possible:
        if section/i<=1 and i-section<filtre:
            Section_possible.append(i)
    Section_possible = list(set(Section_possible)) 
    for keys,value in dictionnaire.items():
        for i in Section_possible:
            if keys == i:
                Combinaison_possible.append(value)
    return {"Variantes":Combinaison_possible,"S (cm²)":Section_possible} 
#-----------------------------------------------------------------------------#

def flection_simple(fck:int,
                    fyk:int,
                    Mu:float,
                    h:float,
                    bw:float,
                    class_exposition:str,
                    d:float,
                    d_prime:float = None,
                    situation:str="normale"):
    if situation == "accidentelle": 
        gamma_c = 1.2
        gamma_s = 1
    else:
        gamma_c = 1.5
        gamma_s = 1.15
    if d_prime==None: 
        d_prime = 0.9*d 
    Beton = beton(fck,gamma_c)
    Acier = acier(fyk,gamma_s) 
    fyd =  Acier.fyd
    fcd =  Beton.fcd
    mu =  Mu/(bw*d**2*fcd) 
    alpha_ulim = 1.25*(1-math.sqrt(1-2*0.372))
    z_ulim = d*(1-0.4*alpha_ulim)
    A_s_min = max(0.26*bw*d*Beton.fctm/fyk,0.0013*bw*d) 
    A_s_max = 0.04*bw*h 
    if mu <= 0.372: 
        alpha_u = 1.25*(1-math.sqrt(1-2*mu))
        z_u = d*(1-0.4*alpha_u)
        A_s = Mu/(z_u*fyd)
        return {"A_s":A_s*10000, "As_min": A_s_min*10000, "A_s_max":A_s_max} 
    else:
        M_ulim = 0.372*bw*d**2*fcd 
        Delta_M = Mu - M_ulim
        A_s = M_ulim/(z_ulim*fyd)+Delta_M/((d-d_prime)*fyd) 
        A_sc = Delta_M/((d-d_prime)*fyd)
        return {"A_s":A_s*10000, "A_sc":A_sc*10000, "As_min": A_s_min*10000, "A_s_max":A_s_max}

