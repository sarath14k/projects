from src.engine import build_ffmpeg_command

def test_mpeg4_decoding():
    print("Testing MPEG4 decoding (Should force CPU decode + hwupload)...")
    codec_conf = {"name": "hevc_vaapi", "type": "gpu", "fmt": "p010"}
    cmd = build_ffmpeg_command(
        file="input.avi",
        out="output.mkv",
        codec_conf=codec_conf,
        val=17,
        device_path="/dev/dri/renderD128",
        width=1280,
        input_codec="mpeg4",
        target_bitrate=2000000,
        max_bitrate=3000000,
        limit_1080p=True,
        compression_level=1
    )
    
    cmd_str = " ".join(cmd)
    print(f"Generated command: {cmd_str}")
    
    # Check that -hwaccel vaapi is NOT present (because of force_cpu_decode)
    assert "-hwaccel vaapi" not in cmd_str, "MPEG4 should NOT use -hwaccel vaapi"
    # Check that hwupload is present in filters
    assert "hwupload" in cmd_str, "MPEG4 should use hwupload filter"
    print("MPEG4 test passed!")

def test_h264_decoding():
    print("\nTesting H264 decoding (Should use full hardware acceleration)...")
    codec_conf = {"name": "hevc_vaapi", "type": "gpu", "fmt": "p010"}
    cmd = build_ffmpeg_command(
        file="input.mp4",
        out="output.mkv",
        codec_conf=codec_conf,
        val=17,
        device_path="/dev/dri/renderD128",
        width=1280,
        input_codec="h264",
        target_bitrate=2000000,
        max_bitrate=3000000,
        limit_1080p=True,
        compression_level=1
    )
    
    cmd_str = " ".join(cmd)
    print(f"Generated command: {cmd_str}")
    
    # Check that -hwaccel vaapi IS present
    assert "-hwaccel vaapi" in cmd_str, "H264 SHOULD use -hwaccel vaapi"
    # Check that hwupload is NOT present in filters (it's internal to vaapi hwaccel)
    assert "hwupload" not in cmd_str, "H264 should NOT use hwupload filter explicitly"
    print("H264 test passed!")

def test_cropping():
    print("\nTesting Cropping (Should force CPU decode + crop filter)...")
    codec_conf = {"name": "hevc_vaapi", "type": "gpu", "fmt": "p010"}
    cmd = build_ffmpeg_command(
        file="input.mp4",
        out="output.mkv",
        codec_conf=codec_conf,
        val=17,
        device_path="/dev/dri/renderD128",
        width=1280,
        input_codec="h264",
        target_bitrate=2000000,
        max_bitrate=3000000,
        limit_1080p=True,
        compression_level=1,
        crop="640:480:10:20"
    )
    
    cmd_str = " ".join(cmd)
    print(f"Generated command: {cmd_str}")
    
    # Check that -hwaccel vaapi is NOT present (because cropping forces CPU decode)
    assert "-hwaccel vaapi" not in cmd_str, "Cropping should NOT use -hwaccel vaapi"
    # Check that crop filter is present
    assert "crop=640:480:10:20" in cmd_str, "Cropping should include the crop filter"
    # Check that hwupload is present in filters
    assert "hwupload" in cmd_str, "Cropping should use hwupload filter"
    print("Cropping test passed!")

def test_trimming():
    print("\nTesting Trimming (Should include -ss and -t arguments)...")
    codec_conf = {"name": "hevc_vaapi", "type": "gpu", "fmt": "p010"}
    cmd = build_ffmpeg_command(
        file="input.mp4",
        out="output.mkv",
        codec_conf=codec_conf,
        val=17,
        device_path="/dev/dri/renderD128",
        width=1280,
        input_codec="h264",
        target_bitrate=2000000,
        max_bitrate=3000000,
        limit_1080p=True,
        compression_level=1,
        trim_enabled=True,
        start_time="00:01:30",
        end_time="00:02:15"
    )
    
    cmd_str = " ".join(cmd)
    print(f"Generated command: {cmd_str}")
    
    assert "-ss" in cmd, "Trimming should include seek argument"
    assert "90.000" in cmd, "Trimming should convert start time to seconds"
    assert "-t" in cmd, "Trimming should include duration argument"
    assert "45.000" in cmd, "Trimming should calculate correct duration in seconds"
    
    idx_ss = cmd.index("-ss")
    idx_t = cmd.index("-t")
    idx_i = cmd.index("-i")
    assert idx_ss < idx_i, "-ss must be before -i"
    assert idx_t > idx_i, "-t must be after -i"
    print("Trimming test passed!")

if __name__ == "__main__":
    try:
        test_mpeg4_decoding()
        test_h264_decoding()
        test_cropping()
        test_trimming()
        print("\nAll engine robustness tests passed successfully!")
    except AssertionError as e:
        print(f"\nTest FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\nAn error occurred during testing: {e}")
        exit(1)
