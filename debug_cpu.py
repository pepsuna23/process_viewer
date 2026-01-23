import psutil
import time

print("Testing psutil.cpu_percent(interval=None) loop...")
# First call to initialize
print(f"First call (should be 0): {psutil.cpu_percent(interval=None)}")

for i in range(5):
    time.sleep(3)
    val = psutil.cpu_percent(interval=None)
    print(f"Call {i+1} after 3s: {val}%")
