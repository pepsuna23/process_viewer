import psutil
from tabulate import tabulate
import sys

def get_processes():
    """Retrieves a list of running processes."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'status', 'memory_info']):
        try:
            pinfo = proc.info
            # Convert memory to MB for better readability
            memory_mb = pinfo['memory_info'].rss / (1024 * 1024)
            pinfo['memory_mb'] = f"{memory_mb:.2f} MB"
            del pinfo['memory_info'] # Remove raw memory info
            processes.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

def display_processes(processes):
    """Displays processes in a tabular format."""
    if not processes:
        print("No processes found.")
        return

    headers = {
        'pid': 'PID',
        'name': 'Name',
        'username': 'User',
        'status': 'Status',
        'memory_mb': 'Memory (RSS)'
    }
    
    # Sort by memory usage (descending)
    processes.sort(key=lambda x: float(x['memory_mb'].split()[0]), reverse=True)

    print(tabulate(processes, headers=headers, tablefmt="grid"))

def main():
    try:
        print("Fetching process list...")
        processes = get_processes()
        display_processes(processes)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
