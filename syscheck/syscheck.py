import argparse
import sys
import json
import time
from datetime import datetime
import platform

# Check for psutil
try:
    import psutil
except ImportError:
    print("Error: 'psutil' module not found.")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def check_cpu(args):
    """Monitor CPU usage"""
    print(f"[*] Checking CPU Usage... (Interval: {args.interval}s)")
    # First call to cpu_percent with interval returns the usage
    usage = psutil.cpu_percent(interval=args.interval, percpu=True)
    total_usage = psutil.cpu_percent(interval=None)
    
    data = {
        "cpu_total_percent": total_usage,
        "cpu_per_core_percent": usage,
        "cpu_count_logical": psutil.cpu_count(),
        "cpu_count_physical": psutil.cpu_count(logical=False)
    }
    
    if args.json:
        return data
        
    print(f"Total CPU Usage: {total_usage}%")
    print(f"Per Core: {usage}")
    print(f"Cores: {data['cpu_count_physical']} Physical, {data['cpu_count_logical']} Logical")
    
    if total_usage > args.threshold:
        print(f"[WARNING] High CPU Usage detected: {total_usage}% > {args.threshold}%")
        
    return data

def check_memory(args):
    """Monitor Memory usage"""
    print("[*] Checking Memory Usage...")
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    data = {
        "total": get_size(svmem.total),
        "available": get_size(svmem.available),
        "used": get_size(svmem.used),
        "percent": svmem.percent,
        "swap_total": get_size(swap.total),
        "swap_used": get_size(swap.used),
        "swap_percent": swap.percent
    }
    
    if args.json:
        return data

    print(f"Total: {data['total']}")
    print(f"Available: {data['available']}")
    print(f"Used: {data['used']} ({data['percent']}%)")
    print(f"Swap Used: {data['swap_used']} ({data['swap_percent']}%)")
    
    if svmem.percent > args.threshold:
        print(f"[WARNING] High Memory Usage detected: {svmem.percent}% > {args.threshold}%")
        
    return data

def check_disk(args):
    """Monitor Disk usage"""
    print("[*] Checking Disk Usage...")
    partitions = psutil.disk_partitions()
    disk_data = []
    
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
            
        p_data = {
            "device": partition.device,
            "mountpoint": partition.mountpoint,
            "fstype": partition.fstype,
            "total": get_size(partition_usage.total),
            "used": get_size(partition_usage.used),
            "free": get_size(partition_usage.free),
            "percent": partition_usage.percent
        }
        disk_data.append(p_data)
        
        if not args.json:
            print(f"Device: {p_data['device']}")
            print(f"  Mount: {p_data['mountpoint']}")
            print(f"  Type: {p_data['fstype']}")
            print(f"  Usage: {p_data['percent']}% ({p_data['used']} / {p_data['total']})")
            
            if partition_usage.percent > args.threshold:
                print(f"  [WARNING] High Disk Usage on {partition.mountpoint}: {partition_usage.percent}% > {args.threshold}%")

    return disk_data

def check_processes(args):
    """List top consuming processes"""
    print(f"[*] Listing Top {args.top} Processes by Memory...")
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent']):
        try:
            pinfo = proc.info
            processes.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    # Sort by memory percent
    processes = sorted(processes, key=lambda p: p['memory_percent'] or 0, reverse=True)[:args.top]
    
    data = []
    if not args.json:
        print(f"{'PID':<10} {'User':<15} {'CPU%':<10} {'MEM%':<10} {'Name'}")
        print("-" * 60)
        
    for p in processes:
        if args.json:
            data.append(p)
        else:
            print(f"{p['pid']:<10} {str(p['username'])[:15]:<15} {p['cpu_percent']:<10} {round(p['memory_percent'], 2):<10} {p['name']}")
    
    return data

def main():
    parser = argparse.ArgumentParser(description="SysCheck: Simple System Resource Monitor")
    
    parser.add_argument("--cpu", action="store_true", help="Check CPU usage")
    parser.add_argument("--memory", action="store_true", help="Check Memory usage")
    parser.add_argument("--disk", action="store_true", help="Check Disk usage")
    parser.add_argument("--proc", action="store_true", help="Check Processes")
    parser.add_argument("--all", action="store_true", help="Check All Resources")
    
    parser.add_argument("--threshold", type=float, default=80.0, help="Warning threshold percent (default: 80.0)")
    parser.add_argument("--interval", type=float, default=1.0, help="CPU check interval (seconds, default: 1.0)")
    parser.add_argument("--top", type=int, default=5, help="Number of processes to list (default: 5)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    results = {
        "timestamp": datetime.now().isoformat(),
        "system": platform.system(),
        "node": platform.node(),
    }
    
    if args.all:
        args.cpu = args.memory = args.disk = args.proc = True

    if args.cpu:
        results["cpu"] = check_cpu(args)
    if args.memory:
        results["memory"] = check_memory(args)
    if args.disk:
        results["disk"] = check_disk(args)
    if args.proc:
        results["processes"] = check_processes(args)
        
    if args.json:
        print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()
