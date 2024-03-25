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

### Database set up

```bash
flask shell
from app import db
db.create_all()
```

### Migration

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
