from django.shortcuts import render

def test_ws(request):
    return render(request, 'test_ws.html', {})