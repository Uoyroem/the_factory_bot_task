from django.http import JsonResponse, HttpRequest


def handler404(request: HttpRequest, exception: Exception) -> JsonResponse:
    return JsonResponse({"detail": "Not found"}, status=404)
