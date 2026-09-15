#!/usr/bin/env python3
"""
Aula 07 -- Bloco 4, demo de retreino/governanca (variante EXTRA): gera uma
versao ruidosa do dataset embaralhando o rotulo houve_violencia. Serve pra
ILUSTRAR o conceito de "dado ruim derruba a acuracia" -- mas com só 40
linhas no dataset ficticio, o resultado NÃO é garantido cair abaixo do
limiar de 60% (testado: varia entre 58% e 67% dependendo da seed). Para a
demonstração AO VIVO do gate bloqueando de verdade, use a variante
confiável do Passo B4-5 (limiar_minimo alto via parâmetro da pipeline, ver
LEIA-ME) -- este script aqui é só material de estudo/discussão sobre
qualidade de dados, não a demo principal de bloqueio.

Uso:
    python3 gerar_dado_ruidoso.py <entrada.csv> <saida.csv> [fracao_ruido]
"""
import random
import sys

import pandas as pd


def main():
    entrada = sys.argv[1] if len(sys.argv) > 1 else "bos_sinteticos.csv"
    saida = sys.argv[2] if len(sys.argv) > 2 else "bos_sinteticos_ruido.csv"
    fracao = float(sys.argv[3]) if len(sys.argv) > 3 else 0.7

    random.seed(7)
    df = pd.read_csv(entrada)

    n_embaralhar = int(len(df) * fracao)
    indices = random.sample(list(df.index), n_embaralhar)

    # embaralha o rotulo SÓ nessas linhas -- quebra a relação entre as
    # features (natureza/bairro/turno) e o alvo, sem mudar o formato do CSV
    valores_originais = df.loc[indices, "houve_violencia"].tolist()
    random.shuffle(valores_originais)
    df.loc[indices, "houve_violencia"] = valores_originais

    df.to_csv(saida, index=False)
    print(f"ok: {n_embaralhar}/{len(df)} linhas com rotulo embaralhado -> {saida}")


if __name__ == "__main__":
    main()
