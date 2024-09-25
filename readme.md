## Instalação
⚠️ ***Este projeto necessita ter docker instalado em sua máquina.***

Clone o projeto em uma pasta na sua máquina:
```bash
git clone https://github.com/Marcos-Pacheco/tiktok-sentiment-analiser.git analiser
```

Inicie os containeres de acordo com o webdriver(navegador) de sua preferência:
```bash
# firefox
docker compose --profile firefox up -d
# chrome
docker compose --profile chrome up -d
```

Em seguida instale as depedências do container python:
```bash
docker compose exec app pip install -r requirements.txt
```

## Scraping
Um dos recursos desse projeto é o scraping de comentário de vídeos do TikTok. Para fazer o scraping de comentários, siga os seguintes passos:
1. Executando o código inicial:
    - Preencha o arquivo `app/urls.txt` com urls dos vídeos que deseja fazer o scraping, separados por linha;
    - Execute o comando
        ```bash
        docker compose exec app py app.py
    ```
2. Na execução do código você deve seguir os seguintes passos:
    - Selecionar webdriver (Firefox|Chrome);
    - Selecionar o tipo de input de urls;
    - Após isso o código irá esperar por um input humano;
    - Você poderá encontrar o painel de execução do scraping no endereço `localhost:4444`
    - Procura pela aba sessions e clique no ícone que tem uma câmera;
    - Ele irá solicitar uma senha, digite `secret`;
    - Após isso você terá de resolver a ***verificação de humanos*** do TikTok;
    - Ao terminar, volte ao terminal e tecle enter, para sinalizar o final da verificação.

## Desativando
Para remover os containeres, execute o seguinte código:
```bash
docker compose --profile "*" down
```