from django.http import JsonResponse

from .client import generate_answer


def test_ollama(request):
    """Test endpoint for Ollama integration"""
    test_prompt = "Hello, please respond with just 'Docker Ollama working!'"

    try:
        response = generate_answer(test_prompt)
        return JsonResponse({"success": True, "response": response})
    except Exception as e:  # pragma: no cover
        return JsonResponse({"success": False, "error": str(e)}, status=500)
