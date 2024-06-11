from celery import shared_task
from .models import Job, Task
from .coinmarketcap import CoinMarketCap

@shared_task
def scrape_coin_data(task_id):
    task = Task.objects.get(id=task_id)
    coinmarketcap = CoinMarketCap()
    data = coinmarketcap.fetch_coin_data(task.coin)
    coinmarketcap.close()
    
    task.output = data
    task.status = 'completed'
    task.save()
