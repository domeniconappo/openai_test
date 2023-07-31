# openai microservice test


## Set up

Copy the .env.template to .env
Edit the variables and set your api key.

Apply first migration

```bash
make migrate
```

## Start the service

To start the service just run:

```bash
make up
```

Docs are at http://localhost:8000/swagger/

You can run tests with:

```bash
make test
```
