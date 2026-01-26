import time
import re
import subprocess

# Regex Patterns
RE_FRAME = re.compile(r"frame=\s*(\d+)")
RE_TIME = re.compile(r"time=(\d{2}):(\d{2}):(\d+\.\d+)")
RE_SIZE = re.compile(r"size=\s*(\d+)KiB")
RE_FPS_SPEED = re.compile(r"fps=\s*(\d+)")
RE_SPEED_TEXT = re.compile(r"speed=\s*([\d\.]+)x")
RE_BITRATE = re.compile(r"bitrate=\s*([\d\.]+)\s*kbits/s")

def build_ffmpeg_command(
    file, out, codec_conf, val, device_path, width, input_codec, target_bitrate, max_bitrate, limit_1080p
):
    is_cpu = codec_conf["type"] == "cpu"
    
    # ─── STABILITY FIX ───
    # Force CPU decoding to prevent GPU driver crashes (CS cancelled)
    force_cpu_decode = True 

    cmd = ["ffmpeg", "-y", "-progress", "pipe:2", "-hide_banner", "-loglevel", "error"]

    if not is_cpu:
        # Initialize VAAPI device, but DO NOT add -hwaccel vaapi (this disables hw decoding)
        cmd.extend(["-init_hw_device", f"vaapi=va:{device_path}", "-filter_hw_device", "va"])

    cmd.extend(["-i", file])

    vf_chain = []
    should_scale = limit_1080p and (width > 1920)

    if is_cpu:
        if should_scale:
            vf_chain.append("scale='min(1920,iw)':-2")
        vf_chain.append(f"format={codec_conf['fmt']}")
    else:
        # ─── UPLOAD TO GPU ───
        # Since decoding is on CPU, we upload frames to GPU memory here
        if codec_conf['fmt'] == 'p010': # 10-bit
            vf_chain.append("format=p010,hwupload")
        else: # 8-bit
            vf_chain.append("format=nv12,hwupload")

        if should_scale:
            vf_chain.append(f"scale_vaapi=w='min(1920,iw)':h=-2:format={codec_conf['fmt']}")
        else:
            vf_chain.append(f"scale_vaapi=format={codec_conf['fmt']}")

    if vf_chain:
        cmd.extend(["-vf", ",".join(vf_chain)])
    
    cmd.extend(["-c:v", codec_conf["name"]])

    if is_cpu:
        cmd.extend(["-crf", "26", "-preset", str(val)])
        if codec_conf["name"] == "libsvtav1":
            cmd.extend(["-svtav1-params", "lp=6:lookahead=32:scd=0"])
    else:
        # GPU Params - Using QP mode for stability with the upload pipeline
        # We ignore target_bitrate/max_bitrate in this mode to ensure stability
        # Mapping quality roughly: 18(Best) to 34(Tiny)
        cmd.extend(["-qp", str(val)])

    cmd.extend([
        "-c:a", "copy",
        "-c:s", "copy",
        "-map_metadata", "0",
        "-avoid_negative_ts", "1",
        out,
    ])
    return cmd

class ProgressParser:
    def __init__(self, duration, fps):
        self.duration_us = duration * 1_000_000
        self.total_frames = int(duration * fps) if fps > 0 else 0
        self.state = {}
        self.start_time = time.time()

    def parse(self, line):
        line = line.strip()
        if "=" not in line:
            return None

        try:
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip()
            self.state[key] = val

            if key == "progress" and val == "continue":
                raw_time = self.state.get("out_time_us", "0")
                if raw_time != "N/A":
                    out_time_us = int(raw_time)
                    pct = min(out_time_us / self.duration_us, 0.99) if self.duration_us > 0 else 0
                else:
                    frame = int(self.state.get("frame", 0))
                    pct = min(frame / self.total_frames, 0.99) if self.total_frames > 0 else 0

                fps = float(self.state.get("fps", 0))
                
                speed_str = self.state.get("speed", "0")
                if "x" in speed_str and "N/A" not in speed_str:
                    speed = float(speed_str.replace("x", ""))
                else:
                    speed = 0.0

                br_str = self.state.get("bitrate", "0")
                if "N/A" not in br_str:
                    bitrate = float(br_str.replace("kbits/s", ""))
                else:
                    bitrate = 0.0

                elapsed = time.time() - self.start_time
                rem = (elapsed / pct - elapsed) if pct > 0 else 0

                return pct, fps, speed, bitrate, rem
        except:
            return None
        return None