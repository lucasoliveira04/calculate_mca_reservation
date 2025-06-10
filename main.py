import pandas as pd
from datetime import time, datetime
import csv


MARGEM_ERRO = 0.02

def read_excel_with_date_filter(path: str, start_date: str, end_date: str) -> dict:
    df = pd.read_excel(path)

    df['data'] = pd.to_datetime(df['data'], dayfirst=True).dt.date
    df['hora'] = pd.to_datetime(df['hora'], format='%H:%M', errors='coerce').dt.time

    start_date_dt = datetime.strptime(start_date, "%d/%m/%Y").date()
    end_date_dt = datetime.strptime(end_date, "%d/%m/%Y").date()

    hora_inicio = time(0, 0)
    hora_fim = time(6, 0)

    df_filtered = df[
        (df['data'] >= start_date_dt) & 
        (df['data'] <= end_date_dt) & 
        (df['hora'] >= hora_inicio) & 
        (df['hora'] <= hora_fim)
    ]

    return {
        "data": df_filtered["data"].astype(str).tolist(),
        "hora": df_filtered["hora"].astype(str).tolist(),
        "mca": df_filtered["mca"].tolist(),
    }

    

def calculate_max_res(largura: float, comprimento: float, altura: float) -> float:
    return largura * comprimento * altura * 1000

def calculate_mca(largura: float, comprimento: float, mca_values: dict) -> dict:
    return {
        hora: largura * comprimento * mca * 1000
        for hora, mca in zip(mca_values["hora"], mca_values["mca"])
    }

def calculate_consumo(mca_litros_dict: dict) -> dict:
    consumo = {}
    horas = list(mca_litros_dict.keys())

    for i in range(1, len(horas)):
        hora_anterior = horas[i - 1]
        hora_atual = horas[i]
        volume_anterior = mca_litros_dict[hora_anterior]
        volume_atual = mca_litros_dict[hora_atual]

        diff = volume_anterior - volume_atual
        consumo[hora_atual] = diff

    return consumo


def save_consumo_csv(consumo_dict: dict, filename: str):
    with open(filename, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Hora', 'Consumo (litros)'])
        for hora, litros in consumo_dict.items():
            writer.writerow([hora, round(litros, 2)])

def save_total_consumo_csv(consumo_total: float, filename: str):
    with open(filename, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Consumo Total (litros)'])
        writer.writerow([round(consumo_total, 2)])


def main():
    caminho_arquivo = "dados.xlsx"
    dados = read_excel_with_date_filter(caminho_arquivo, "07/06/2025", "14/06/2025")

    LARGURA = 1.5
    COMPRIMENTO = 2.0
    ALTURA = 3.0

    print("Volumes por célula:")
    volume_total = calculate_max_res(LARGURA, COMPRIMENTO, ALTURA)
    print(f"\nVolume total do reservatório: {volume_total:.2f} litros\n")

    print("MCA e porcentagem de uso:")
    mca_result = calculate_mca(LARGURA, COMPRIMENTO, dados)

    for hora, mca_litros in mca_result.items():
        percentual = (mca_litros / volume_total) * 100
        print(f"{hora}: {mca_litros:.2f} litros | Uso do reservatório: {percentual:.2f}%")

    print("\nConsumo por intervalo:")
    consumo_resultado = calculate_consumo(mca_result)

    consumo_total = 0.0
    consumo_ajustado = {}

    for hora, litros in consumo_resultado.items():
        litros_ajustados = litros * (1 - MARGEM_ERRO)
        status = "consumo" if litros_ajustados > 0 else "enchimento"
        print(f"{hora}: {abs(litros_ajustados):.2f} litros ({status})")
        consumo_ajustado[hora] = litros_ajustados
        if litros_ajustados > 0:
            consumo_total += litros_ajustados

    save_consumo_csv(consumo_ajustado, 'consumo_total_horas.csv')
    save_total_consumo_csv(consumo_total, 'consumo_total.csv')
    print(f"Arquivo 'consumo_total.csv' criado com o consumo total por hora.")
    print(f"Consumo total ajustado: {consumo_total:.2f} litros")


if __name__ == "__main__":
    main()
