from django.shortcuts import render
import requests
from django.http import JsonResponse

def get_external_data(request):
    url = 'https://api.example.com/data/'  # Replace with your actual API URL
    headers = {
        'Authorization': 'Bearer YOUR_API_KEY_OR_TOKEN',
        'Accept': 'application/json',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Failed to fetch data'}, status=response.status_code)
