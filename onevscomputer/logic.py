# logic.py (Originalmente fornecido - Nenhuma alteração)

from random import randint

class Logic_calculator:
    def __init__(self):
        self.choose = None
        self.n1 = 0
        self.n2 = 0

    def randomNumber(self):
        """
        Escolhe dois números aleatórios iniciais, limitando o intervalo para 
        facilitar resultados de um único dígito (0 a 9).
        """
        # Limite os números iniciais para um intervalo menor (ex: 0 a 9)
        self.n1 = randint(0, 9)
        self.n2 = randint(0, 9)

    def choose_operator(self):
        """
        Escolhe o operador entre +, -, x, / garantindo que o resultado final
        esteja entre 0 e 9 (1 dígito).
        """
        while True:
            self.randomNumber()
            self.choose = randint(0, 3)

            # SOMA
            if self.choose == 0:
                result = self.n1 + self.n2
                # NOVO LIMITE: O resultado deve ser menor ou igual a 9
                if result <= 9: 
                    return "+"

            # SUBTRAÇÃO (resultado >= 0 AND <= 9)
            elif self.choose == 1:
                # Garante que n1 >= n2 para resultado não negativo
                if self.n1 < self.n2:
                    self.n1, self.n2 = self.n2, self.n1
                result = self.n1 - self.n2
                # NOVO LIMITE: O resultado deve estar entre 0 e 9
                if 0 <= result <= 9:
                    return "-"

            # MULTIPLICAÇÃO
            elif self.choose == 2:
                result = self.n1 * self.n2
                # NOVO LIMITE: O resultado deve ser menor ou igual a 9
                if result <= 9:
                    return "x"

            # DIVISÃO inteira exata
            else:
                # Evita divisão por zero
                if self.n2 == 0:
                    continue
                # Só aceita divisão com resultado inteiro
                if self.n1 % self.n2 == 0:
                    result = self.n1 // self.n2
                    # NOVO LIMITE: O resultado deve ser menor ou igual a 9
                    if result <= 9:
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
            return self.n1 // self.n2

    def is_correct(self, user_answer):
        """Retorna True/False se o usuário acertou."""
        return user_answer == self.get_correct_answer()

    def checknumber(self, answerUser):
        """Mantém compatibilidade com seu código antigo."""
        return "Parabéns!" if self.is_correct(answerUser) else "Errou! Tente de novo!"