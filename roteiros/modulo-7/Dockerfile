FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git jq bash && rm -rf /var/lib/apt/lists/*
RUN useradd -m aluno
USER aluno
RUN git config --global --add safe.directory /origem
WORKDIR /home/aluno
CMD ["bash"]
