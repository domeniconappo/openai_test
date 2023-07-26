# openai microservice test

Copy the .env.template to .env
Edit the variables and set your api key.

Apply first migration

```bash
make migrate
```

Then to start the service:

```bash
make up
```

Docs are at http://localhost:8000/swagger/
