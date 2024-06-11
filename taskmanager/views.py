from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, Task
from .tasks import scrape_coin_data
import uuid

class StartScrapingView(APIView):
    def post(self, request):
        coin_list = request.data.get('coins', [])
        
        if not all(isinstance(coin, str) for coin in coin_list):
            return Response({"error": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)
        
        job = Job.objects.create()
        
        for coin in coin_list:
            task = Task.objects.create(job=job, coin=coin)
            scrape_coin_data.delay(task.id)
        
        return Response({"job_id": job.job_id}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        try:
            job_uuid = uuid.UUID(job_id)
            job = Job.objects.get(job_id=job_uuid)
        except (ValueError, Job.DoesNotExist):
            return Response({"error": "Invalid job ID"}, status=status.HTTP_404_NOT_FOUND)
        
        tasks = job.tasks.all()
        response_data = {
            "job_id": str(job.job_id),
            "tasks": [
                {
                    "coin": task.coin,
                    "output": task.output
                } for task in tasks
            ]
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
