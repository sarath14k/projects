import time

from .config import CODECS


def build_ffmpeg_command(
    file,
    out,
    codec_conf,
    val,
    device_path,
    do_scale,
    input_codec,
    target_bitrate,
    max_bitrate,
):
    is_cpu = codec_conf["type"] == "cpu"
    force_cpu_decode = input_codec == "av1" and not is_cpu

    cmd = ["ffmpeg", "-y", "-progress", "pipe:2", "-hide_banner"]

    if not is_cpu:
        cmd.extend(
            ["-init_hw_device", f"vaapi=va:{device_path}", "-filter_hw_device", "va"]
        )
        if not force_cpu_decode:
            cmd.extend(
                [
                    "-hwaccel",
                    "vaapi",
                    "-hwaccel_output_format",
                    "vaapi",
                    "-extra_hw_frames",
                    "256",
                ]
            )

    cmd.extend(["-i", file])

    vf_chain = []
    if is_cpu:
        if do_scale:
            vf_chain.append("scale='min(1920,iw)':-2")
        vf_chain.append(f"format={codec_conf['fmt']}")
    else:
        if force_cpu_decode:
            vf_chain.append("format=nv12|p010,hwupload")
        if do_scale:
            vf_chain.append(
                f"scale_vaapi=w='min(1920,iw)':h=-2:format={codec_conf['fmt']}"
            )
        else:
            vf_chain.append(f"scale_vaapi=format={codec_conf['fmt']}")

    if vf_chain:
        cmd.extend(["-vf", ",".join(vf_chain)])
    cmd.extend(["-c:v", codec_conf["name"]])

    if is_cpu:
        cmd.extend(["-crf", "26", "-preset", str(val)])
    else:
        cmd.extend(["-compression_level", "1"])
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

    cmd.extend(
        [
            "-c:a",
            "copy",
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
    def __init__(self, duration):
        self.duration_us = duration * 1_000_000
        self.state = {}
        self.start_time = time.time()

    def parse(self, line):
        line = line.strip()
        if "=" not in line:
            return None
        key, val = line.split("=", 1)
        self.state[key.strip()] = val.strip()

        if key.strip() == "progress" and val.strip() == "continue":
            try:
                out_time_us = int(self.state.get("out_time_us", 0))
                pct = (
                    min(out_time_us / self.duration_us, 0.99)
                    if self.duration_us > 0
                    else 0
                )
                fps = float(self.state.get("fps", 0))
                speed_str = self.state.get("speed", "0")
                speed = (
                    float(speed_str.replace("x", ""))
                    if "x" in speed_str
                    else float(speed_str)
                )
                br_str = self.state.get("bitrate", "0")
                bitrate = (
                    float(br_str.replace("kbits/s", "")) if "N/A" not in br_str else 0
                )
                elapsed = time.time() - self.start_time
                rem = (elapsed / pct - elapsed) if pct > 0 else 0
                return pct, fps, speed, bitrate, rem
            except:
                return None
        return None
