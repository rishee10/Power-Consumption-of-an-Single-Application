import psutil
import time

def measure_power_consumption(process_name, duration=10, sampling_interval=1):

    # Find all processes matching the given name
    processes = [proc for proc in psutil.process_iter(['name', 'pid']) if process_name.lower() in proc.info['name'].lower()]

    if not processes: # If No Such Process found 
        print(f"No process with name '{process_name}' found.")
        return

    print(f"Monitoring {len(processes)} '{process_name}' processes...")
    
    # Assumptions for power estimation
    cpu_power_per_core = 15  # Watts per core at 100% usage
    memory_power_per_gb = 3  # Watts per GB of memory usage

    total_cpu_usage = 0
    total_memory_usage_gb = 0

    # Monitor processes over the specified duration
    start_time = time.time()
    while time.time() - start_time < duration:
        for proc in processes:
            try:
                # Get CPU and memory usage for the process
                cpu_usage = proc.cpu_percent(interval=None)  # CPU usage as a percentage
                memory_info = proc.memory_info()
                memory_usage_gb = memory_info.rss / (1024 ** 3)  # Convert memory usage to GB
                
                # Accumulate the usage
                total_cpu_usage += cpu_usage
                total_memory_usage_gb += memory_usage_gb
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # Wait for the next sample
        time.sleep(sampling_interval)

    # Calculate average power consumption
    num_cores = psutil.cpu_count(logical=True)
    avg_cpu_power = (total_cpu_usage / duration / 100) * cpu_power_per_core * num_cores
    avg_memory_power = (total_memory_usage_gb / duration) * memory_power_per_gb

    # Display results
    print(f"\nEstimated power consumption of '{process_name}':")
    print(f"CPU Power: {avg_cpu_power:.2f} W")
    print(f"Memory Power: {avg_memory_power:.2f} W")
    print(f"Total Power: {avg_cpu_power + avg_memory_power:.2f} W")

# Example usage
if __name__ == "__main__":
    process_name = "chrome.exe"  # Application Name for which we required power consumption
    measure_power_consumption(process_name)


