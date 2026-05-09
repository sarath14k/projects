#!/usr/bin/env python3
import os

import sys
import json

def get_status(temp, device_type):
    # Adjust thresholds based on device type if necessary
    if device_type == "GPU" and "Hotspot" in device_type:
        # GPU hotspot can be higher normally
        optimal, normal, warm = 50, 85, 95
    elif device_type == "GPU" or device_type == "CPU":
        optimal, normal, warm = 45, 75, 85
    else:
        # NVMe, Motherboard, etc
        optimal, normal, warm = 40, 60, 70

    if temp <= optimal:
        return "❄️ Optimal"
    elif temp <= normal:
        return "✔️ Normal"
    elif temp <= warm:
        return "⚠️ Warm"
    else:
        return "🔥 Hot/Bad"

def main():
    hwmon_dir = "/sys/class/hwmon/"
    try:
        hwmons = os.listdir(hwmon_dir)
    except FileNotFoundError:
        if "--json" in sys.argv: print("{}")
        else: print("Hardware monitoring not available.")
        return

    results = {}
    
    for hwmon in hwmons:
        path = os.path.join(hwmon_dir, hwmon)
        try:
            with open(os.path.join(path, "name"), "r") as f:
                name = f.read().strip()
        except (IOError, OSError):
            continue

        device_type = "Other"
        display_name = name
        if name == "acpitz":
            display_name = "ACPI (Ambient)"
        elif name == "nvme":
            display_name = "NVMe Storage"
            device_type = "Storage"
        elif name == "k10temp":
            display_name = "AMD CPU"
            device_type = "CPU"
        elif name == "gigabyte_wmi":
            display_name = "Motherboard (Gigabyte)"
            device_type = "Motherboard"
        elif "r8169" in name:
            display_name = "Network Card"
        elif name == "amdgpu":
            display_name = "AMD GPU"
            device_type = "GPU"

        temps = []
        try:
            files = os.listdir(path)
        except OSError:
            continue

        for file in files:
            if file.startswith("temp") and file.endswith("_input"):
                try:
                    with open(os.path.join(path, file), "r") as f:
                        val = int(f.read().strip()) / 1000.0
                    
                    # Try to read label, fallback to generic
                    label = "temp"
                    try:
                        with open(os.path.join(path, file.replace("_input", "_label")), "r") as f:
                            label = f.read().strip()
                    except (IOError, OSError):
                        if name == "gigabyte_wmi":
                            label = f"Sensor {file[4:-6]}"
                except (IOError, ValueError):
                    continue

                # Improve labels
                if name == "acpitz" and label == "temp":
                    label = "Ambient"
                elif name == "k10temp":
                    if label == "Tctl": label = "Package (Tctl)"
                    elif label == "Tccd1": label = "Die 1"
                elif name == "amdgpu":
                    if label == "edge": label = "Edge"
                    elif label == "junction": label = "Hotspot"
                    elif label == "mem": label = "VRAM"
                elif "r8169" in name:
                    label = "Chip"

                current_type = device_type
                if label == "Hotspot":
                    current_type = "GPU Hotspot"

                status = get_status(val, current_type)
                temps.append({
                    "label": label,
                    "value": val,
                    "status": status
                })

        if temps:
            results[display_name] = sorted(temps, key=lambda x: x["label"])

    if "--json" in sys.argv:
        sys.stdout.write(json.dumps(results) + "\n")
    else:
        output = []
        for device, readings in results.items():
            output.append(f"[{device}]")
            for r in readings:
                output.append(f"  {r['label']}: {r['value']:.1f}°C  {r['status']}")
            output.append("")
        sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    main()
