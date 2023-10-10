# tester/views.py
from django.shortcuts import get_object_or_404, render, redirect
from .models import Server
from .forms import ServerForm
import socket
import subprocess

def server_list(request):
    servers = Server.objects.all()
    return render(request, 'tester/server_list.html', {'servers': servers})

def add_server(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('server_list')
    else:
        form = ServerForm()
    return render(request, 'tester/add_server.html', {'form': form})

def modify_server(request, server_id):
    server = get_object_or_404(Server, pk=server_id)

    if request.method == 'POST':
        form = ServerForm(request.POST, instance=server)
        if form.is_valid():
            form.save()
            return redirect('server_list')
    else:
        form = ServerForm(instance=server)

    return render(request, 'tester/modify_server.html', {'form': form, 'server': server})

def delete_server(request, server_id):
    server = get_object_or_404(Server, pk=server_id)
    
    if request.method == 'POST':
        server.delete()
        return redirect('server_list')
    
    return render(request, 'tester/delete_server.html', {'server': server})


def test_server(request, server_id):
    try:
        server = Server.objects.get(pk=server_id)
        ip_address = socket.gethostbyname(server.address)
        
        # Perform a ping test
        try:
            ping_result = subprocess.run(
                ["ping", ip_address],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10,
            )
            if ping_result.returncode == 0:
                result = f"Server is reachable. Ping Response: {ping_result.stdout}"
            else:
                result = f"Server is unreachable. Ping Error: {ping_result.stderr}"
        except subprocess.TimeoutExpired:
            result = "Ping test timeout. Server may be unreachable."
        
        # Perform a DNS resolution test
        try:
            socket.gethostbyname(server.address)
            dns_result = "DNS resolution successful."
        except socket.gaierror:
            dns_result = "DNS resolution failed. Could not resolve host."

    except Server.DoesNotExist:
        result = "Server not found"
        dns_result = ""
    
    return render(
        request,
        'tester/test_server.html',
        {'server': server, 'ping_result': result, 'dns_result': dns_result}
    )
