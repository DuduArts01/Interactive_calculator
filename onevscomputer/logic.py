from random import randint

class Logic_calculator:
    def __init__(self):
        self.choose = None
        self.n1 = 0
        self.n2 = 0

    def randomNumber(self):
        """Escolhe dois números aleatórios iniciais."""
        self.n1 = randint(0, 50)
        self.n2 = randint(0, 50)

    def choose_operator(self):
        """Escolhe o operador entre +, -, x, / garantindo resultados inteiros quando necessário."""
        self.choose = randint(0, 3)

        if self.choose == 0:
            # Soma
            return "+"

        elif self.choose == 1:
            # Subtração (garante n1 >= n2)
            while self.n1 < self.n2:
                self.n1 = randint(0, 50)
                self.n2 = randint(0, 50)
            return "-"

        elif self.choose == 2:
            # Multiplicação
            return "x"

        else:
            # Divisão inteira
            while True:
                self.n1 = randint(1, 100)
                self.n2 = randint(1, 10)
                if self.n1 % self.n2 == 0:  # garante resultado inteiro
                    break
            return "/"

    def get_correct_answer(self):
        """Retorna o resultado correto com base no operador."""
        if self.choose == 0:
            return self.n1 + self.n2
        elif self.choose == 1:
            return self.n1 - self.n2
        elif self.choose == 2:
            return self.n1 * self.n2
        elif self.choose == 3:
            return self.n1 / self.n2

    def is_correct(self, user_answer):
        """Retorna True/False se o usuário acertou."""
        return user_answer == self.get_correct_answer()

    def checknumber(self, answerUser):
        """Mantém compatibilidade com seu código antigo."""
        if self.is_correct(answerUser):
            return "Parabéns!"
        else:
            return "Errou! Tente de novo!"
