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

### copiar o arquivo .env.example como .env e setar suas variáveis de conexão com o db

```python
DB_NAME=""     # nome da database que o projeto vai acessar
DB_USER=""     # nome do usuário que acessa o db
DB_PASS=       # senha do usuário que acessa o db
DB_PORT=5432   # porta da aplicação do postgresql, a porta padrão é 5432
```

### rodar as migrations se as tabelas ainda não existem no banco de dados e após isso executar o script de inserção de dados na base

```bash
$ flask --app ./src/app.py migrate upgrade
```

### finalmente executar a aplicação

```bash
$ flask --app ./src/app.py run
```

### para rodar os testes devemos ir no diretório que está os arquivos de teste e colocar o seguinte comando
```bash
$ pytest .\historic_tests.py .\professor_tests.py .\student_tests.py .\subject_tests.py
```
