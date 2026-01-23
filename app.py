import logging
import os
import subprocess
import sys
import threading
import time

import psutil
import webview
from flask import Flask, render_template, jsonify, request

logging.basicConfig(
    filename='process_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder=os.path.join(base_dir, 'templates'))

def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'status', 'memory_info', 'cpu_percent']):
        try:
            info = proc.info
            memory_mb = info['memory_info'].rss / (1024 * 1024)
            info['memory_mb'] = f"{memory_mb:.2f}"
            info['memory_val'] = memory_mb
            
            info['cpu_percent'] = info['cpu_percent'] or 0.0

            del info['memory_info']
            processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    processes.sort(key=lambda x: float(x['memory_val']), reverse=True)
    return processes

current_stats = {
    'cpu_percent': 0.0,
    'memory_percent': 0.0,
    'total_threads': 0
}

previous_processes = {} 
first_run = True

def update_stats_loop():
    global previous_processes, first_run
    
    while True:
        try:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            try:
                 threads = sum(p.num_threads() for p in psutil.process_iter() if p.pid != 0)
            except:
                 threads = 0
            
            current_stats['cpu_percent'] = cpu
            current_stats['memory_percent'] = mem
            current_stats['total_threads'] = threads

            current_chunk = {}
            for p in psutil.process_iter(['pid', 'name']):
                try:
                    current_chunk[p.pid] = p.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            if first_run:
                previous_processes = current_chunk
                first_run = False
            else:
                current_pids = set(current_chunk.keys())
                previous_pids = set(previous_processes.keys())

                new_pids = current_pids - previous_pids
                for pid in new_pids:
                    name = current_chunk.get(pid, "Unknown")
                    logging.info(f"Process STARTED: {name} (PID: {pid})")
                
                gone_pids = previous_pids - current_pids
                for pid in gone_pids:
                    name = previous_processes.get(pid, "Unknown")
                    logging.info(f"Process STOPPED: {name} (PID: {pid})")
                
                previous_processes = current_chunk

        except Exception as e:
            logging.error(f"Error in stats/logging loop: {e}")
            time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/processes')
def api_processes():
    return jsonify(get_processes())

@app.route('/api/stats')
def api_stats():
    return jsonify(current_stats)

@app.route('/api/run', methods=['POST'])
def api_run_program():
    data = request.json
    command = data.get('command')
    if not command:
         return jsonify({'success': False, 'message': 'No command provided'}), 400
    
    try:
        subprocess.Popen(command, shell=True)
        logging.info(f"User launched command: {command}")
        return jsonify({'success': True, 'message': f'Command started: {command}'})
    except Exception as e:
        logging.error(f"Failed to launch command '{command}': {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/kill/<int:pid>', methods=['DELETE'])
def api_kill_process(pid):
    try:
        proc = psutil.Process(pid)
        name = proc.name()
        proc.terminate()
        logging.info(f"Process terminated by USER: PID={pid}, Name={name}")
        return jsonify({'success': True, 'message': f'Process {name} (PID {pid}) terminated.'})
    except psutil.NoSuchProcess:
        return jsonify({'success': False, 'message': 'Process not found.'}), 404
    except psutil.AccessDenied:
        return jsonify({'success': False, 'message': 'Permission denied.'}), 403
    except Exception as e:
        logging.error(f"Error terminating process {pid}: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

def start_flask():
    app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
    stats_thread = threading.Thread(target=update_stats_loop, daemon=True)
    stats_thread.start()

    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    webview.create_window("System Monitor Pro", "http://127.0.0.1:5000", width=1200, height=800)
    webview.start()
