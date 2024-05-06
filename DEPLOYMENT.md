# Configuration and Deployment

## Configuring secrets

#### For the application to run, you need to set up some secrets, for this, rename the
1. .env.example -> .env
2. .env.access_service.example -> .env.access_service
3. .env.notes.example -> .env.notes

#### Next, fill in your secrets instead of template secrets in these files.

## Preparing the environment

#### In order to run the project, you need to install the
1. docker engine
2. docker compose

## Launching an application

### All you need is

```shell
docker compose up --build
```

Or

```shell
docker-compose up --build
```