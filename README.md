# It happens bot

This telegram bot serves quotes from ithappens.me one by one to help you read them all.

## Dependencies

This service depends on [Quotes Service](https://github.com/elisey/quotes_service). Consider deploying it too.

### How to deploy

```shell
cp docker/prod.env.example docker/prod.env
vim docker/prod.env

docker-compose up --build -d app
```

### How to run locally

```shell
cp docker/prod.env.example app/.env
vim app/.env

docker-compose up --build -d app
```
