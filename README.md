# Create Python apps using SQL Server on macOS

## Preparation

### Docker

It's possible to install Docker using HomeBrew. You need _docker_ and _docker-machine_, and _VirtualBox_ to run docker.

```bash
brew cask install VirtualBox
brew install docker-machine
brew install docker
```

Then, you should create a VM and start `docker-machine`.
Configure at least 4GB of memory for your Docker environment, also consider adding multiple cores if you want to evaluate performance.
You may need to add the last line to your _~/.bash_profile_.
```bash
docker-machine create -d virtualbox --virtualbox-memory 4096  --cpus 2 default
docker-machine start
eval $(docker-machine env default)
```

You can use the following to run docker-machine daemon on start up:
```bash
brew services start docker-machine
```

It's possible to modify VM's characteristics while it's not running:
```bash
docker-machine stop
VBoxManage modifyvm default --cpus 2
docker-machine start
```

### Python

It's possible to install python using HomeBrew:
```bash
brew install python
```

### Appendix: Install HomeBrew

```bash
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

## Install and Run

### Get and Run Docker Image

```bash
docker pull microsoft/mssql-server-linux:2017-latest
docker run -e 'HOMEBREW_NO_ENV_FILTERING=1' -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=yourStrong(!)Password' -p 1433:1433 -d microsoft/mssql-server-linux
```

DB username will be `SA` (case-insensitive) and password will be what you pass as `SA_PASSWORD`. You can chose the edition by passing `MSSQL_PID`,too [[+](https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-configure-docker?view=sql-server-2017#production)]. By default, developer edition will be run.

You can ensure the success of installation by running `docker images`, after `docker pull`. 

The exposed port will be exposed to docker-machine, not host (your machine). You should use it's IP instead, where needed. You can find the IP by `docker-machine ip`. It's noticeable that the IP will be change whenever docker-machine starts.

You can check the docker using lightweight _hello-world_ web server:
```bash
docker pull crccheck/hello-world
docker run -d --name web-test -p 80:8000 crccheck/hello-world
curl $(docker-machine ip):80
```

### ODBC Driver and SQL Command Line Utility

It's possible to install these utilities by HomeBrew, too:
```bash
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
HOMEBREW_NO_ENV_FILTERING=1 ACCEPT_EULA=y brew install --no-sandbox msodbcsql17 mssql-tools
```

Now, you can use `sqlcmd` to communicate with DB server. Try:
```bash
sqlcmd -S $(docker-machine ip),1433 -U sa -P 'yourStrong(!)Password' -Q "SELECT @@VERSION"
```

You can use a CLI by:
```bash
sqlcmd -S $(docker-machine ip),1433 -U sa -P 'yourStrong(!)Password'
```

### Python

You can install python wrapper for ODBC by `pip`:
```bash
pip install pyodbc
```

You should add the following line to your code because of [a bug in MS SQL Server](https://github.com/Microsoft/homebrew-mssql-release/issues/18#issuecomment-397420786).
```python
locale.setlocale(locale.LC_CTYPE, "C")
```

## More Complicated Python Program

See [**Create Python apps using SQL Server on macOS** at Microsoft Get started with SQL Server](https://www.microsoft.com/en-us/sql-server/developer-get-started/python/mac/).
