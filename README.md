# fast_api_monitor
Python FastApi website monitor


### Development environment

- Prepare a virtual Python 3.6+ environment
- Install requirements
```
$ pip install -r requirements.txt
```
- Run command `$ python main.py dev` to start the development server


### Testing

Testing for FastAPI is based on [pytest](https://docs.pytest.org/en/stable/)

See `./test/client.py` for script example, which took reference from fastapi docs:

- [testing](https://fastapi.tiangolo.com/tutorial/testing/)

Run `$ pytest ./test/client.py` to start a test


### Deployment

Run `$ ./script/pack.sh` to pack the project into `./build/fast_api_monitor.tar.gz`

Run `$ docker build -t python-api-monitor -f Dockerfile .` to make an docker image



### Project Structure Nutshell

- config
  - dev.cfg: app cfg of dev mode, using [python-dotenv](https://github.com/theskumar/python-dotenv)))
  - prod.cfg: app cfg of production mode
  - uvicorn: cfg for [uvicorn](https://www.uvicorn.org/settings/)
    - logger.json: [logging cfg](https://github.com/encode/uvicorn/blob/master/uvicorn/config.py) for uvicorn
    - dev.json: cfg for uvicorn launcher of dev mode
    - prod.json: cfg for uvicorn of prod mode
- build: deployment files
- controller: controller modules with router callbacks
- middleware: web app middlewares
- model: internal data models
- script: user defined scripts
  - pack.sh: pack the web-app project
- service: service libraries
- test: custom python scripts for testing modules
- utils: base apis for web app modules
- app.py: fastapi application entry
- main.py: uvicorn entry


### About coding

- run server in dev mode
  - `$ python main.py dev`
- add controller routes in `config/router.py` and add corresponding callbacks in `./controller`
- add services in `./service` for controllers
- add data models in `./model` for services and controllers
- add middlewares if necessary


### features later on for a SaaS application

- websocket server monitor
- persistence data store into DB
- notification with email
- business account for teams
