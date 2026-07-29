"""
Classes responsáveis por:
  - Contrato: valor fixo de R$ 2.000,00 parcelável em até 5x
  - OrcamentoAluguel: junta um Imovel + um Contrato e gera o orçamento final, incluindo a exportação do arquivo .csv com 12 parcelas

Complementando a HERANÇA já usada em models.py.
"""

import csv
from datetime import date
from scripts.models import Imovel


class Contrato:
    """Representa o contrato de locação, valor fixo parcelável em até 5x."""

    VALOR_TOTAL = 2000.00
    MAX_PARCELAS = 5

    def __init__(self, num_parcelas: int = 1):
        if not 1 <= num_parcelas <= self.MAX_PARCELAS:
            raise ValueError(
                f"O contrato só pode ser parcelado em até {self.MAX_PARCELAS}x."
            )
        self.num_parcelas = num_parcelas

    def valor_parcela(self) -> float:
        return round(self.VALOR_TOTAL / self.num_parcelas, 2)


class OrcamentoAluguel:
    """Gera o orçamento final: aluguel mensal + parcelas do contrato."""

    MESES_CSV = 12

    def __init__(self, imovel: Imovel, contrato: Contrato, cliente: str = "Cliente"):
        self.imovel = imovel
        self.contrato = contrato
        self.cliente = cliente

    def valor_aluguel_mensal(self) -> float:
        return self.imovel.calcular_aluguel()

    def resumo(self) -> str:
        linhas = [
            "=" * 46,
            "        ORÇAMENTO DE ALUGUEL - IMOBILIÁRIA R.M",
            "=" * 46,
            f"Cliente: {self.cliente}",
            f"Imóvel: {self.imovel.descricao()}",
            f"Valor do aluguel mensal: R$ {self.valor_aluguel_mensal():.2f}",
            f"Valor do contrato: R$ {Contrato.VALOR_TOTAL:.2f} "
            f"em {self.contrato.num_parcelas}x de "
            f"R$ {self.contrato.valor_parcela():.2f}",
            "=" * 46,
        ]
        return "\n".join(linhas)

    def exportar_csv(self, caminho: str = "orcamento_aluguel.csv") -> str:
        """
        Gera um .csv com as 12 parcelas mensais do orçamento.
        """
        aluguel_mensal = self.valor_aluguel_mensal()
        parcela_contrato = self.contrato.valor_parcela()

        with open(caminho, mode="w", newline="", encoding="utf-8-sig") as arquivo:
            writer = csv.writer(arquivo, delimiter=";")
            writer.writerow(
                ["Mes", "Aluguel (R$)", "Parcela Contrato (R$)", "Total do Mes (R$)"]
            )
            for mes in range(1, self.MESES_CSV + 1):
                parcela_do_mes = (
                    parcela_contrato if mes <= self.contrato.num_parcelas else 0.0
                )
                total_mes = round(aluguel_mensal + parcela_do_mes, 2)
                writer.writerow(
                    [
                        mes,
                        f"{aluguel_mensal:.2f}",
                        f"{parcela_do_mes:.2f}",
                        f"{total_mes:.2f}",
                    ]
                )
        return caminho
