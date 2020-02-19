# Running

```bash
$ celery worker -A src.task
```

```Python
>>> from src.task import add_random_cows, inseminate
>>> add_random_cows.delay(1)
<AsyncResult: f079a420-6021-474e-b797-49b042602d5c>
>>> inseminate.delay(1)
<AsyncResult: 6aa05919-65f7-4a06-ab23-1b9a94977076>
```

```
[2020-02-19 16:48:52,467: WARNING/ForkPoolWorker-2] Estera added to the farm.
[2020-02-19 16:49:02,945: WARNING/ForkPoolWorker-2] Estera is now inseminated.
```
