# PyNewsScraper

Este projeto é um scraper (raspador de dados) para verificar as bibliotecas Python que tiveram atualização no último mês e listá-las, facilitando a identificação de bibliotecas com lançamentos de versão major.

Este Scraper utiliza IA para que não seja necessário a sua atualização constante

# Como utilizar

Para criar um ambiente virtual, execute
```
python -m venv .venv
```

Para ativar o ambiente virtual, execute
```
source .venv/bin/activate
```

Para instalar as dependências do projeto no ambiente virtual, execute
```
pip install -r requirements.txt
```

Para completar a instalação do Crawl4AI
```
# Install the package
pip install -U crawl4ai

# Run post-installation setup
crawl4ai-setup

# Verify your installation
crawl4ai-doctor
```
Crie uma chave junto a COHERE
- https://docs.cohere.com/
<p>

Atualize o valor em prompt.py
```
...
os.environ["COHERE_API_KEY"] = "<YOUR-API-KEY>"
...
```
Instale o Thinker
```cmd
sudo apt-get install python3-tk
```

Para procurar por releases, execute o comando abaixo e aguarde as instruções
```
python getNews.py releases
```

Para criar os resumos, execute
```
python getNews.py slides
```


Para desativar o ambiente virtual, execute `deactivate`.
