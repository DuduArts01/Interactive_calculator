from random import randint, choice

class Logic_calculator:
    def __init__(self):
        self.last_denominators = []  # saves the last used numbers
        # create list of possible denominators, excluding the last ones
        self.candidates = [i for i in range(1, 11) if i not in self.last_denominators[-3:]]
    
    def randomNumber(self):
        self.n1 = 1
        self.n2 = 2 

    def choose_operator(self):
        self.choose = randint(0,3)
        
        # Easy calculate numbers to user
        if self.choose == 3: # 3 
            while self.n1 % self.n2 != 0: # Answer is interger and n1 >= n2 
                self.n1 = randint(0,100) 
                self.n2 = randint(1,10) # Can never have denominator 0 
            return "/"
            
        
        
        elif self.choose == 2: # 2
            while self.n1 < self.n2: # Answer is interger and n1 >= n2
                self.n1 = randint(0,10)
                self.n2 = randint(0,9)

            return "x" 
        
        elif self.choose: # 1
            while self.n1 < self.n2: # Answer is interger and n1 >= n2
                self.n1 = randint(0,50)
                self.n2 = randint(0,49)
            
            return "-"
        
        else: # 0
            while self.n1 < self.n2: # Answer is interger and n1 >= n2
                self.n1 = randint(0,50)
                self.n2 = randint(0,49)
            
            return "+"         

    def checknumber(self, answerUser):
        if self.choose == 3 and answerUser == (self.n1 / self.n2): # Correct Sum
            return "Parabéns!"
        elif self.choose == 3 and answerUser != (self.n1 / self.n2): # Wrong Sum
            return "Errou! Tente de novo!" 
        elif self.choose == 2 and answerUser == (self.n1 * self.n2): # Correct Subtration
            return "Parabéns!"
        elif self.choose == 2 and answerUser != (self.n1 * self.n2): # Wrong Subtration
            return "Errou! Tente de novo!"
        elif self.choose and answerUser == (self.n1 - self.n2): # Correct multiply
            return "Parabéns!"
        elif self.choose and answerUser != (self.n1 - self.n2): # Wrong multiply
            return "Errou! Tente de novo!"
        elif not self.choose and answerUser == (self.n1 + self.n2): # Correct Division
            return "Parabéns!"
        elif not self.choose and answerUser != (self.n1 + self.n2): # Wrong Division
            return "Errou! Tente de novo!"