def calculate_max_res(largura: float, comprimento: float, altura: float, celulas: bool, qntdCelulas: int) -> float:
    """Calcula o volume total do reservatório em litros."""
    if celulas:
        largura_por_celula = largura / qntdCelulas
        volume_total = 0
        for i in range(qntdCelulas):
            volume_celula = largura_por_celula * comprimento * altura * 1000  
            print(f"Reservatório {i + 1}: {volume_celula:.2f} litros")
            volume_total += volume_celula
        return volume_total
    else:
        volume_total = largura * comprimento * altura * 1000
        print(f"Reservatório único: {volume_total:.2f} litros")
        return volume_total


def calculate_mca(largura: float, comprimento: float, mca_values: dict) -> dict:
    """Calcula o volume em litros para cada valor de MCA dado."""
    return {
        hora: largura * comprimento * mca * 1000
        for hora, mca in mca_values.items()
    }


def main():
    LARGURA = 1.5
    COMPRIMENTO = 2.0
    ALTURA = 3.0

    CELULAS = True
    QNTD_CELULAS = 5

    MCA_AND_HOURS = {
        "00:00": 2.0,
        "00:20": 1.5,
        "00:22": 1.8,
        "01:00": 2.5,
        "02:00": 3.0,
        "03:00": 3.5,
    }

    print("Volumes por célula:")
    volume_total = calculate_max_res(LARGURA, COMPRIMENTO, ALTURA, CELULAS, QNTD_CELULAS)
    print(f"\nVolume total do reservatório: {volume_total:.2f} litros\n")

    print("MCA e porcentagem de uso:")
    mca_result = calculate_mca(LARGURA, COMPRIMENTO, MCA_AND_HOURS)

    for hora, mca_litros in mca_result.items():
        percentual = (mca_litros / volume_total) * 100
        print(f"{hora}: {mca_litros:.2f} litros | Uso do reservatório: {percentual:.2f}%")


if __name__ == "__main__":
    main()
