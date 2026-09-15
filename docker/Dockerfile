# Aula 07 -- imagem custom usada em DOIS lugares:
#   1) Bloco 1: "docker run" direto, empacotando treino_ml_rapido.py (Aula 05/06)
#   2) Bloco 4: base_image de TODOS os componentes da pipeline Kubeflow
#      (pipeline/pipeline_kfp_mlops.py) -- por isso ela ja vem com kfp
#      instalado (install_kfp_package=False no pipeline, ver LEIA-ME).
#
# Multi-stage: o estagio "builder" instala as dependencias; o estagio final
# só copia o resultado -- imagem final menor, sem compiladores/ferramentas
# de build sobrando.

# ---------------------------------------------------------------------
# Estagio 1: builder
# ---------------------------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .

# --user instala em /root/.local -- copiavel isoladamente pro estagio final
# (equivalente ao --break-system-packages usado no terminal: aqui dentro do
# container o Python NAO e "gerenciado pelo sistema" da mesma forma que no
# WSL2/Debian do seu host, mas --user evita qualquer ambiguidade mesmo assim)
RUN pip install --user --no-cache-dir -r requirements.txt

# ---------------------------------------------------------------------
# Estagio 2: imagem final
# ---------------------------------------------------------------------
FROM python:3.11-slim

# usuario nao-root (boa pratica -- Kubernetes/Kubeflow rodam melhor sem root)
RUN useradd --create-home --uid 1000 mlops
WORKDIR /app

COPY --from=builder /root/.local /home/mlops/.local
COPY data/bos_sinteticos.csv /app/data/bos_sinteticos.csv
COPY treino_ml_rapido.py /app/treino_ml_rapido.py

ENV PATH=/home/mlops/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

RUN chown -R mlops:mlops /app
USER mlops

# uso 1 (Bloco 1) -- roda o treino direto:
#   docker run --rm aula7-mlops-pcdf:local python treino_ml_rapido.py data/bos_sinteticos.csv
# uso 2 (Bloco 4) -- referenciada como base_image pelos componentes KFP,
#   nunca roda com este ENTRYPOINT (o KFP substitui o command/args).
ENTRYPOINT ["python", "treino_ml_rapido.py"]
CMD ["data/bos_sinteticos.csv"]
