## Instalação
⚠️ ***Este projeto necessita ter docker instalado em sua máquina.***

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
- Preencha o arquivo `app/urls.txt` com urls dos vídeos que deseja fazer o scraping, separados por linha;
- Execute o comando
    ```bash
    docker compose exec app py app.py
    ```
Você poderá encontrar o painel de execução do scraping no endereço `localhost:4444`

## Desativando
Para remover os containeres, execute o seguinte código:
```bash
docker compose --profile "*" down
```