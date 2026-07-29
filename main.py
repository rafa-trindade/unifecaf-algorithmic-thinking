"""
Aplicação de linha de comando (CLI) da Imobiliária R.M.

Como executar:
    python main.py
"""

from scripts.models import Apartamento, Casa, Estudio
from scripts.orcamento import Contrato, OrcamentoAluguel


def ler_inteiro(mensagem: str, opcoes=None) -> int:
    while True:
        valor = input(mensagem).strip()
        if valor.isdigit() and (opcoes is None or int(valor) in opcoes):
            return int(valor)
        print("  -> Valor inválido, tente novamente.")


def ler_sim_nao(mensagem: str) -> bool:
    while True:
        valor = input(mensagem + " (s/n): ").strip().lower()
        if valor in ("s", "n"):
            return valor == "s"
        print("  -> Responda apenas 's' ou 'n'.")


def montar_imovel():
    print("\nTipo de imóvel:")
    print("  1 - Apartamento")
    print("  2 - Casa")
    print("  3 - Estúdio")
    tipo = ler_inteiro("Escolha (1-3): ", opcoes=(1, 2, 3))

    if tipo == 1:
        quartos = ler_inteiro("Quantos quartos (1 ou 2): ", opcoes=(1, 2))
        garagem = ler_sim_nao("Deseja incluir vaga de garagem?")
        sem_criancas = ler_sim_nao("O cliente possui filhos? (responda 'n' para SEM filhos)")

        return Apartamento(quartos=quartos, garagem=garagem, sem_criancas=not sem_criancas)

    if tipo == 2:
        quartos = ler_inteiro("Quantos quartos (1 ou 2): ", opcoes=(1, 2))
        garagem = ler_sim_nao("Deseja incluir vaga de garagem?")
        return Casa(quartos=quartos, garagem=garagem)

    # Estúdio
    quer_vagas = ler_sim_nao("Deseja incluir vagas de estacionamento?")
    vagas = 0
    if quer_vagas:
        vagas = ler_inteiro("Quantas vagas (mínimo 2): ", opcoes=range(2, 21))
    return Estudio(vagas=vagas)


def montar_contrato():
    print("\nO contrato de locação é de R$ 2.000,00, parcelável em até 5x.")
    num_parcelas = ler_inteiro("Em quantas vezes deseja parcelar (1 a 5): ", opcoes=(1, 2, 3, 4, 5))
    return Contrato(num_parcelas=num_parcelas)


def main():
    print("Bem-vindo ao sistema de Orçamento de Aluguel - Imobiliária R.M")
    cliente = input("Nome do cliente: ").strip() or "Cliente"

    imovel = montar_imovel()
    contrato = montar_contrato()

    orcamento = OrcamentoAluguel(imovel=imovel, contrato=contrato, cliente=cliente)

    print("\n" + orcamento.resumo())

    gerar_csv = ler_sim_nao("\nDeseja gerar o arquivo .csv com as 12 parcelas do orçamento?")
    if gerar_csv:
        caminho = orcamento.exportar_csv("orcamento_aluguel.csv")
        print(f"Arquivo gerado com sucesso: {caminho}")

    print("\nObrigado por usar o sistema da Imobiliária R.M!")


if __name__ == "__main__":
    main()
