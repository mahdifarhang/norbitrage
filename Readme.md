You need postgres running for it to work correctly, (use docker for it)
You need redis running. use docker compose for it. for:
1. cache (TODO)
2. celery message broker
3. celery-beat message broker (TODO)

You need celery to be running as a Consumer app. use command bellow:
```shell
python -m celery -A norbitrage worker -l info
```

