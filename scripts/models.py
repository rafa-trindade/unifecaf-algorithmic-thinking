"""
Classe abstrata:
    Imovel

Subclasses concretas:
    Apartamento, Casa, Estudio
"""

from abc import ABC, abstractmethod


class Imovel(ABC):
    """Classe base abstrata para qualquer tipo de imóvel locável."""

    VALOR_GARAGEM = 300.00

    def __init__(self, quartos: int = 1, garagem: bool = False):
        self.quartos = quartos
        self.garagem = garagem

    @abstractmethod
    def calcular_valor_base(self) -> float:
        """Cada subclasse define sua própria regra de valor base."""
        raise NotImplementedError

    def calcular_valor_garagem(self) -> float:
        """Regra padrão de garagem (sobrescrita pelo Estúdio)."""
        return self.VALOR_GARAGEM if self.garagem else 0.0

    def calcular_aluguel(self) -> float:
        """Valor final do aluguel mensal (polimorfismo em ação)."""
        return round(self.calcular_valor_base() + self.calcular_valor_garagem(), 2)

    def descricao(self) -> str:
        return f"{self.__class__.__name__} - {self.quartos} quarto(s)"


class Apartamento(Imovel):

    VALOR_1_QUARTO = 700.00
    ACRESCIMO_2_QUARTOS = 200.00
    DESCONTO_SEM_CRIANCAS = 0.05  # 5%

    def __init__(self, quartos: int = 1, garagem: bool = False, sem_criancas: bool = False):
        super().__init__(quartos, garagem)
        self.sem_criancas = sem_criancas

    def calcular_valor_base(self) -> float:
        valor = self.VALOR_1_QUARTO
        if self.quartos == 2:
            valor += self.ACRESCIMO_2_QUARTOS
        return valor

    def calcular_aluguel(self) -> float:
        valor = super().calcular_aluguel()
        if self.sem_criancas:
            valor = valor * (1 - self.DESCONTO_SEM_CRIANCAS)
        return round(valor, 2)


class Casa(Imovel):

    VALOR_1_QUARTO = 900.00
    ACRESCIMO_2_QUARTOS = 250.00

    def calcular_valor_base(self) -> float:
        valor = self.VALOR_1_QUARTO
        if self.quartos == 2:
            valor += self.ACRESCIMO_2_QUARTOS
        return valor


class Estudio(Imovel):

    VALOR_BASE = 1200.00
    VALOR_2_VAGAS = 250.00
    VALOR_VAGA_ADICIONAL = 60.00

    def __init__(self, vagas: int = 0):
        super().__init__(quartos=1, garagem=False)
        self.vagas = vagas

    def calcular_valor_base(self) -> float:
        return self.VALOR_BASE

    def calcular_valor_garagem(self) -> float:
        if self.vagas <= 0:
            return 0.0
        if self.vagas <= 2:
            return self.VALOR_2_VAGAS
        vagas_extras = self.vagas - 2
        return self.VALOR_2_VAGAS + (vagas_extras * self.VALOR_VAGA_ADICIONAL)
