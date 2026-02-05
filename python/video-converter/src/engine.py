import time
import subprocess

def build_ffmpeg_command(
    file,
    out,
    codec_conf,
    val,
    device_path,
    width,
    input_codec,
    target_bitrate,
    max_bitrate,
    limit_1080p,
    compression_level=4,
    process_mode="Video + Audio",
    audio_codec_key="Copy",
):
    # Check if using CPU - either codec type is CPU OR device is "cpu"
    is_cpu = codec_conf["type"] == "cpu" or device_path == "cpu"

    # Force CPU decoding ONLY for codecs that often have poor/no VAAPI support
    problematic_vaapi_decoders = {
        "av1",
        "mpeg4",
        "msmpeg4v3",
        "msmpeg4v2",
        "msmpeg4v1",
        "flv1",
        "vp8",
    }
    force_cpu_decode = input_codec in problematic_vaapi_decoders and not is_cpu

    cmd = [
        "ffmpeg",
        "-y",
        "-threads",
        "0",
        "-progress",
        "pipe:2",
        "-hide_banner",
        "-loglevel",
        "warning",
    ]

    if not is_cpu:
        # Initialize VAAPI device with optimized thread queue
        cmd.extend(
            ["-init_hw_device", f"vaapi=va:{device_path}", "-filter_hw_device", "va"]
        )
        if not force_cpu_decode:
            # Restore hardware accelerated decoding for maximum performance
            cmd.extend(
                [
                    "-hwaccel",
                    "vaapi",
                    "-hwaccel_output_format",
                    "vaapi",
                    "-extra_hw_frames",
                    "32",
                ]
            )

    cmd.extend(["-i", file])

    if process_mode == "Audio Only":
        cmd.append("-vn")
    else:
        vf_chain = []
        should_scale = limit_1080p and (width > 1920)

        if is_cpu:
            if should_scale:
                vf_chain.append("scale='min(1920,iw)':-2")
            vf_chain.append(f"format={codec_conf['fmt']}")
        else:
            if force_cpu_decode:
                # Decoded on CPU, upload to GPU for filtering/encoding
                if codec_conf["fmt"] == "p010":  # 10-bit
                    vf_chain.append("format=p010,hwupload")
                else:  # 8-bit
                    vf_chain.append("format=nv12,hwupload")

            if should_scale:
                vf_chain.append(
                    f"scale_vaapi=w='min(1920,iw)':h=-2:format={codec_conf['fmt']}"
                )
            else:
                vf_chain.append(f"scale_vaapi=format={codec_conf['fmt']}")

        if vf_chain:
            cmd.extend(["-vf", ",".join(vf_chain)])

        cmd.extend(
            [
                "-c:v",
                codec_conf["name"]
                if not (device_path == "cpu" and codec_conf["type"] != "cpu")
                else "libx265",
            ]
        )

        if is_cpu:
            if codec_conf["name"] == "libsvtav1":
                cmd.extend(["-preset", str(val)])
                cmd.extend(["-svtav1-params", "lp=8:lookahead=20:scd=1:tune=0"])
            else:
                x265_presets = {
                    4: "slower",
                    5: "slow",
                    6: "medium",
                    7: "faster",
                    8: "fast",
                    9: "veryfast",
                    10: "ultrafast",
                }
                preset = x265_presets.get(val, "medium")
                cmd.extend(["-crf", "26", "-preset", preset])
        else:
            cmd.extend(["-compression_level", str(compression_level)])
            depth = (
                4 if compression_level <= 2 else (3 if compression_level <= 4 else 2)
            )
            cmd.extend(["-async_depth", str(depth)])

            buf_size = max_bitrate * 2
            cmd.extend(
                [
                    "-rc_mode",
                    "QVBR",
                    "-global_quality",
                    str(val),
                    "-b:v",
                    str(target_bitrate),
                    "-maxrate",
                    str(max_bitrate),
                    "-bufsize",
                    str(buf_size),
                ]
            )

    # Audio encoding logic
    from .config import AUDIO_CODECS

    audio_codec_name = AUDIO_CODECS.get(audio_codec_key, "copy")
    cmd.extend(["-c:a", audio_codec_name])

    cmd.extend(
        [
            "-c:s",
            "copy",
            "-map_metadata",
            "0",
            "-avoid_negative_ts",
            "1",
            out,
        ]
    )
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
                if raw_time and raw_time != "N/A":
                    out_time_us = int(raw_time)
                    pct = min(out_time_us / self.duration_us, 0.99) if self.duration_us > 0 else 0
                else:
                    frame_str = self.state.get("frame", "0")
                    frame = int(frame_str) if str(frame_str).isdigit() else 0
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