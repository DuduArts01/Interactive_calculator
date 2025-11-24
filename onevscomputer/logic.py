from random import randint

class Logic_calculator:
    def __init__(self):
        self.choose = None
        self.n1 = 0
        self.n2 = 0

    def randomNumber(self):
        """Escolhe dois números aleatórios iniciais (não define operador ainda)."""
        self.n1 = randint(0, 50)
        self.n2 = randint(0, 50)

    def choose_operator(self):
        """
        Escolhe o operador entre +, -, x, / garantindo que o resultado final
        esteja entre 0 e 99 (2 dígitos).
        """
        while True:
            self.randomNumber()
            self.choose = randint(0, 3)

            # SOMA
            if self.choose == 0:
                result = self.n1 + self.n2
                if result <= 99:
                    return "+"

            # SUBTRAÇÃO (resultado >= 0 AND < 100)
            elif self.choose == 1:
                if self.n1 < self.n2:
                    self.n1, self.n2 = self.n2, self.n1
                result = self.n1 - self.n2
                if 0 <= result <= 99:
                    return "-"

            # MULTIPLICAÇÃO
            elif self.choose == 2:
                result = self.n1 * self.n2
                if result <= 99:
                    return "x"

            # DIVISÃO inteira exata
            else:
                # Só aceita divisão com resultado inteiro
                if self.n2 == 0:
                    continue
                if self.n1 % self.n2 == 0:
                    result = self.n1 // self.n2
                    if result <= 99:
                        return "/"

            # Se não deu certo, repete o loop até gerar valores válidos

    def get_correct_answer(self):
        """Retorna o resultado correto com base no operador."""
        if self.choose == 0:
            return self.n1 + self.n2
        elif self.choose == 1:
            return self.n1 - self.n2
        elif self.choose == 2:
            return self.n1 * self.n2
        elif self.choose == 3:
            return self.n1 // self.n2  # divisão inteira

    def is_correct(self, user_answer):
        """Retorna True/False se o usuário acertou."""
        return user_answer == self.get_correct_answer()

    def checknumber(self, answerUser):
        """Mantém compatibilidade com seu código antigo."""
        return "Parabéns!" if self.is_correct(answerUser) else "Errou! Tente de novo!"
