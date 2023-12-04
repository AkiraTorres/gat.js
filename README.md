# gat.js

## como rodar

```bash
$ git clone https://github.com/akiratorres/gat.js
$ cd gat.js
```

### criar e ativar um venv na pasta da aplicação

```bash
$ python -m venv venv
$ ./venv/Scripts/activate
```

### instalar as dependencias do projeto

```bash
$ pip install -r requirements.txt
```

### configurar o arquivo .env

### se não existente, criar a base de dados e rodar as migrations

```bash
$ flask --app ./src/app.py migrate upgrade
```

### e após executar o script de inserção de dados na base


### finalmente executar a aplicação

```bash
$ flask --app ./src/app.py run
```