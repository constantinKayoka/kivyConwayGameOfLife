#from random import random
import random
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock

class Tableau (App):

    def build(self):
        
        self.BigBox = BoxLayout(orientation='vertical') 

        self.buttonBox = BoxLayout(orientation = 'horizontal', size_hint = (1,0.1))
        self.start = Button(text = str("start"))
        self.randomized = Button(text = str("randomized"))
        self.Choose_sized = ToggleButton(text = "choisir taille",state = 'normal')

        self.buttonBox.add_widget(self.start)
        self.buttonBox.add_widget(self.randomized)
        self.buttonBox.add_widget(self.Choose_sized)
        self.BigBox.add_widget(self.buttonBox)


        self.input_wide = TextInput()
        self.buttonBox.add_widget(self.input_wide)
        self.intput_height = TextInput()
        self.buttonBox.add_widget(self.intput_height)

        self.grid = GridLayout(rows=10, cols=10,size_hint = (1,0.9))

        self.matrix = [] 
        
        self.addButton()
        #self.verifBouton()
        self.BigBox.add_widget(self.grid)
        
        self.Choose_sized.bind(on_press = self.changeSize)
        self.start.bind(on_press=self.start_game)
        self.randomized.bind(on_press=self.addButton_randomized)     
        
            
        
        return self.BigBox
    
    def start_game(self,source):
        if(self.Choose_sized.state == "down"):
            self.start.bind(on_press=self.randomized_update_button)
            Clock.schedule_interval(self.randomized_update_button,1)
        Clock.schedule_interval(self.updateBouton,1)

    
    def changeSize(self,source):
        """
        change la taille de grid
        """
        self.matrix = []
        self.BigBox.remove_widget(self.grid)
        
        self.grid = GridLayout(rows=int(self.input_wide.text), cols=int(self.intput_height.text),size_hint = (1,0.9))
        self.BigBox.add_widget(self.grid)
        
        if(self.Choose_sized.state == "down"):
            self.start.bind(on_press=self.randomized_update_button)
            self.randomized.bind(on_press=self.randomized_size_choose)

        for i in range(int(self.input_wide.text)):

            row = []

            for j in range(int(self.intput_height.text)):

                bouton = ToggleButton(state = 'normal')    # cre un bouton de state noram ou cellule morte
                                                           #le bouton down ==> vivante  
                self.grid.add_widget(bouton)

                row.append(bouton)
            
            self.matrix.append(row)
    
    def randomized_size_choose(self,source):
        """
        remplis les case aléatoirement pour 
        un set determiner manuelement
        """
        for i in range(int(self.input_wide.text)):

            for j in range(int(self.intput_height.text)):
                self.matrix[i][j].state = self.randomState()
    
    def randomized_update_button(self,source):
        """
        update les boutons aléatoirement
        pour un set determiner manuelement
        """
        for i in range(int(self.input_wide.text)):

            for j in range(int(self.intput_height.text)):
                n = self.checkNeighborhood(i, j)
                if self.matrix[i][j].state == 'down':  # si vivante
                    
                    if n != 2 and n != 3 : # si ni 2 ni 3 voisines vivantes
                        self.matrix[i][j].state = "normal"                         # meurt

                elif self.matrix[i][j].state == 'normal':                                   # sinon, si morte
                    if n == 3:     # si 3 voisines vivantes devient vivante
                        self.matrix[i][j].state = "down"
                        
    def addButton_randomized(self,source):
        """
        Ajouter les boutons alleatoirement vivants ou morts a grid
        et les ajouter à la matrix
        """
    
        for i in range(10):

            for j in range(10):
                self.matrix[i][j].state = self.randomState()


    def addButton(self): #not size_choose
        """
        Ajouter les boutons alleatoirement vivants ou morts a grid
        et les ajouter à la matrix
        """
        for i in range(10):

            row = []

            for j in range(10):

                bouton = ToggleButton(state = 'normal')    # cre un bouton de state noram ou cellule morte
                                                           #le bouton down ==> vivante  
                self.grid.add_widget(bouton)

                row.append(bouton)
            
            self.matrix.append(row)


    def updateBouton(self,source):  #not size_choose
        """
        Parcour la matrix en vérifiant l'etat des boutons
        et modifie leur etat en fonction des regles du jeu de la vie.
        """
        aliveMatrix = []
        for i in range(10):

            for j in range(10):
                n = self.checkNeighborhood(i, j)
                if self.matrix[i][j].state == 'down':  # si vivante
                    
                    if n != 2 and n != 3 : # si ni 2 ni 3 voisines vivantes
                        self.matrix[i][j].state = "normal"                         # meurt

                else:                                   # sinon, si morte
                    if n == 3:     # si 3 voisines vivantes devient vivante
                        self.matrix[i][j].state = "down"



    def checkNeighborhood(self, numLigneCellule, numColonneCellule):
        """
        Prend en argument les index de ligne et de colonne d'une cellule.
        Retourne le nombre de cellules vivantes parmi les 8
        cellule voisine de cette cellule.
        """
        
        nombreVivante = 0
        try:  #1
            if self.matrix[numLigneCellule - 1][numColonneCellule - 1].state == "down":
                nombreVivante += 1
        except IndexError:
            pass

        try: #2
            if self.matrix[numLigneCellule - 1][numColonneCellule + 1].state == "down":
                nombreVivante += 1
        except IndexError:
            pass

        try: #3
            if self.matrix[numLigneCellule - 1][numColonneCellule ].state == "down":
                nombreVivante += 1
        except IndexError:
            pass


######
        try: #4
            if self.matrix[numLigneCellule][numColonneCellule - 1].state == "down":
                nombreVivante += 1
        except IndexError:
            pass

        try: #5
            if self.matrix[numLigneCellule][numColonneCellule + 1].state == "down":
                nombreVivante += 1
        except IndexError:
            pass

#####

        try: #6
            if self.matrix[numLigneCellule + 1][numColonneCellule + 1].state == "down":
                nombreVivante += 1
        except IndexError:
            pass

        try: #7
            if self.matrix[numLigneCellule + 1][numColonneCellule - 1].state == "down":
                nombreVivante += 1
        except IndexError:
            pass
        try: #8
            if self.matrix[numLigneCellule + 1][numColonneCellule ].state == "down":
                nombreVivante += 1
        except IndexError:
            pass

        return nombreVivante
        
    def randomState(self):
        """
        retourne Aléatoirement "normal" ou "down" avec une proba de 1/2 
        """
        return random.choice(["normal", "down"])

    def randomState2(self):
        """
        #Retourne aleatoirement "normal" ou "down" (respectivement morte ou vivante)
        """
        nbre = int (proba * random())

        if nbre > 1:
            return ("normal")
        else:
            return ("down")
        




Tableau().run()