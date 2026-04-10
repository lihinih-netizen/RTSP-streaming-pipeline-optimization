# survey_runner.py
import subprocess
import yaml
import time

config_path = "/home/aiot/Documents/Containers/networking/homeassistant/go2rtc/config/go2rtc.yml"

SURVEY_CONFIGS = {
    '1': {'codec': 'h264', 'width': '1920', 'height': '1080', 'bitrate': '2000k', 'framerate': '30'},
    '2': {'codec': 'h264', 'width': '1280', 'height': '720',  'bitrate': '2000k', 'framerate': '30'},
    '3': {'codec': 'h264', 'width': '854',  'height': '480',  'bitrate': '2000k', 'framerate': '30'},
    '4': {'codec': 'h264', 'width': '1920', 'height': '1080', 'bitrate': '500k',  'framerate': '30'},
    '5': {'codec': 'h264', 'width': '1920', 'height': '1080', 'bitrate': '2000k', 'framerate': '10'},
    '6': {'codec': 'h265', 'width': '1920', 'height': '1080', 'bitrate': '2000k', 'framerate': '30'},
}

def set_config(config_num):
    params = SURVEY_CONFIGS[config_num]
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f) or {}
    
    config['streams']['Camera_3'] = [
        f"ffmpeg:rtsp://admin:aiot2024@192.168.50.13:554/h264Preview_01_main"
        f"#video={params['codec']}"
        f"#width={params['width']}"
        f"#height={params['height']}"
        f"#bitrate={params['bitrate']}"
        f"#framerate={params['framerate']}"
    ]
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    # Restart container
    subprocess.run(['podman', 'restart', 'go2rtc-ha'])
    print(f"\n✓ Configuration {config_num} active!")
    print(f"  Settings: {params['codec']}, {params['width']}x{params['height']}, {params['bitrate']}, {params['framerate']}fps")
    print(f"  Waiting 60 seconds for stream to stabilize...")
    
    for i in range(60, 0, -1):
        print(f"\r  Stabilizing... {i} seconds remaining", end='', flush=True)
        time.sleep(1)
    
    print(f"\n✓ Stream ready! Ask participants to rate Configuration {config_num}")
    input("\nPress Enter when ready for next configuration...")

def main():
    print("="*60)
    print("SURVEY RUNNER")
    print("="*60)
    print("\nThis will run each survey configuration one by one.")
    print("Press Enter after participants finish rating each config.")
    input("\nPress Enter to start with Configuration 1...")
    
    for num in ['1', '2', '3', '4', '5', '6']:
        set_config(num)
    
    print("\n✓ All configurations shown!")
    print("Survey complete — collect all forms from participants.")

if __name__ == "__main__":
    main()