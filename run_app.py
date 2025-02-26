

import os
import sys
import subprocess
import time
import signal
import threading
import socket

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

def is_port_in_use(port, host='localhost'):
    """Check if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def kill_process_on_port(port, host='localhost'):
    """Kill the process using the specified port."""
    if not is_port_in_use(port, host):
        return False
    
    try:
        # Find the process ID using the port
        if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
            cmd = f"lsof -i :{port} -t"
            pid = subprocess.check_output(cmd, shell=True).decode().strip()
            if pid:
                # Kill the process
                os.system(f"kill -9 {pid}")
                print(f"Killed process {pid} using port {port}")
                time.sleep(1)  
                return True
    except Exception as e:
        print(f"Error killing process on port {port}: {e}")
    
    return False

def run_backend():
    """Run the backend server."""
    # Check if the port is already in use
    if is_port_in_use(settings.API_PORT, settings.API_HOST):
        print(f"Port {settings.API_PORT} is already in use. Attempting to kill the process...")
        if not kill_process_on_port(settings.API_PORT, settings.API_HOST):
            print(f"Could not free port {settings.API_PORT}. Please close the application using this port and try again.")
            return None
    
    print(f"Starting backend server on http://{settings.API_HOST}:{settings.API_PORT}")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", settings.API_HOST, "--port", str(settings.API_PORT), "--reload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=dict(os.environ, PYTHONPATH=os.path.dirname(os.path.abspath(__file__)))
    )
    return backend_process

def run_frontend():
    """Run the frontend server."""
    # Check if the port is already in use
    if is_port_in_use(settings.FRONTEND_PORT, 'localhost'):
        print(f"Port {settings.FRONTEND_PORT} is already in use. Attempting to kill the process...")
        if not kill_process_on_port(settings.FRONTEND_PORT, 'localhost'):
            print(f"Could not free port {settings.FRONTEND_PORT}. Please close the application using this port and try again.")
            return None
    
    print(f"Starting frontend server on http://localhost:{settings.FRONTEND_PORT}")
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port", str(settings.FRONTEND_PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=dict(os.environ, PYTHONPATH=os.path.dirname(os.path.abspath(__file__)))
    )
    return frontend_process

def stream_output(process, prefix):
    """Stream the output of a process to the console."""
    if process is None:
        return
        
    for line in iter(process.stdout.readline, ""):
        if line:
            print(f"{prefix}: {line.strip()}")

def main():
    """Run the application."""
    # Create data directories if they don't exist
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    os.makedirs(settings.VISUALIZATIONS_DIR, exist_ok=True)
    
    # Start the backend server
    backend_process = run_backend()
    if backend_process is None:
        print("Failed to start backend server. Exiting...")
        return
        
    backend_thread = threading.Thread(
        target=stream_output,
        args=(backend_process, "Backend"),
        daemon=True
    )
    backend_thread.start()
    
    # Wait for the backend to start
    print("Waiting for backend to start...")
    time.sleep(5)
    
    # Start the frontend server
    frontend_process = run_frontend()
    if frontend_process is None:
        print("Failed to start frontend server. Shutting down backend...")
        backend_process.terminate()
        return
        
    frontend_thread = threading.Thread(
        target=stream_output,
        args=(frontend_process, "Frontend"),
        daemon=True
    )
    frontend_thread.start()
    
    # Handle graceful shutdown
    def signal_handler(sig, frame):
        print("Shutting down...")
        if frontend_process:
            frontend_process.terminate()
        if backend_process:
            backend_process.terminate()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process and backend_process.poll() is not None:
                print("Backend server stopped. Shutting down...")
                if frontend_process:
                    frontend_process.terminate()
                break
            
            if frontend_process and frontend_process.poll() is not None:
                print("Frontend server stopped. Shutting down...")
                if backend_process:
                    backend_process.terminate()
                break
    except KeyboardInterrupt:
        print("Shutting down...")
        if frontend_process:
            frontend_process.terminate()
        if backend_process:
            backend_process.terminate()

if __name__ == "__main__":
    main() 
