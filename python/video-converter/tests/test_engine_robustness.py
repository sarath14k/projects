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

if __name__ == "__main__":
    try:
        test_mpeg4_decoding()
        test_h264_decoding()
        print("\nAll engine robustness tests passed successfully!")
    except AssertionError as e:
        print(f"\nTest FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\nAn error occurred during testing: {e}")
        exit(1)
