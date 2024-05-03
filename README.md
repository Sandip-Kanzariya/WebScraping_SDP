# MedMinear Backend [RESTfull APIs using FLASK]

> [Frontend](https://github.com/DigitalGit2003/WebScraping_Frontend)

# Run Project

## Setting up a Python Virtual Environment and Installing Packages (py = python)

### Create Virtual Environment

```bash
py -m venv .venv
```

### Activate Virtual Environment

```bash
.venv\Scripts\activate
```

### Install Packages From requirements.txt

```bash
pip install -r requirements.txt
```

### Environment Variable Setup (env.env file make changes as per your need)
```py
FLASK_APP=app
FLASK_DEBUG=True
FLASK_RUN_PORT=5050
FLASK_RUN_HOST=0.0.0.0

# For Remote PostgreSQL Database : postgresql://username:password@hostname:port/database_name
SQLALCHEMY_DATABASE_URI=POSTGRESQL_REMOTE_URL

JWT_SECRET_KEY = SELECTED_SECRET_KEY
IMAGE_UPLOAD_FOLDER= PATH
TESSERACT_CMD = PATH
FLASK_SECRET_KEY = SELECTED_FLASK_SECRET_KEY

# For Different Databases

# For local SQLite Database
# SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite3 

# For local MySQL Database
# SQLALCHEMY_DATABASE_URI=mysql://root:@localhost/flask 
# For Remote MySQL Database
# SQLALCHEMY_DATABASE_URI=MYSQL_FREEDATABASE_URL

# For local PostgreSQL Database
# SQLALCHEMY_DATABASE_URI=POSTGRESQL_LOCAL_URL
```

### Install as per your database 
|Database|Pip|
|---|---|
|PostgreSQL|pip install psycopg2 or pip install psycopg2-binary|
|MySQL|pip install mysqlclient|


### Database set up (**If required then only**)
```bash
flask shell
from app import db
db.create_all()
```

### Migration (**If required then only**)

```shell
flask db init
flask db migrate -m "message"
flask db upgrade
```

### Run Flask App (script_file_name = app.py)
```bash
flask --app script_file_name run
or
py script_file_name.py
```

## Team Members

<table>
  <tr>
    <td align="center">
        <a href="https://github.com/DigitalGit2003">
            <img src="https://github.com/DigitalGit2003.png" width="100px;" alt=""/>
            <br />
            <sub><b>Gautam Lathiya</b></sub>
        </a>
        <br />
        <a href="https://github.com/Sandip-Kanzariya/WebScraping_SDP/commits?author=DigitalGit2003" title="Code">💻</a>
    </td>
    <td align="center">
        <a href="https://github.com/Sandip-Kanzariya">
            <img src="https://github.com/Sandip-Kanzariya.png" width="100px;" alt=""/>
            <br />
            <sub><b>Sandip Kanzariya</b></sub>
        </a>
        <br />
        <a href="https://github.com/Sandip-Kanzariya/WebScraping_SDP/commits?author=Sandip-Kanzariya" title="Documentation">💻</a>
    </td>
    <td align="center">
        <a href="https://github.com/Prit-mmonpara">
            <img src="https://github.com/Prit-mmonpara.png" width="100px;" alt=""/>
            <br />
            <sub><b>Prit Monpara</b></sub>
        </a>
        <br />
        <a href="https://github.com/Sandip-Kanzariya/WebScraping_SDP/commits?author=Prit-mmonpara" title="Documentation">💻</a>
    </td>
    </tr>
</table>
