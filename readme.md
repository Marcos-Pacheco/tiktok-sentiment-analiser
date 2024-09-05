Projeto de TCC

# Instruções de Execução

## Iniciar projeto
Para iniciar o projeto, dê permissões de execução para o arquivo `init.sh` e o execute:

    chmod +x init.sh
    ./init.sh

## Ativar Ambiente
    source env/bin/activate

## PiP Version
    py -m pip --version

## Criar arquivo de dependências
    py -m pip freeze > requirements.txt

## Instalar dependências
    python -m pip install -r requirements.txt

## Criar arquivo de versionamento das dependências
    py -m pip install -c constraints.txt

## Executar Scrapper
    py App.py
