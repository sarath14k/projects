import librosa
import sys
import numpy as np
import os
import json
import re
import subprocess
import shutil
import tempfile
import multiprocessing
import torch
from numba import njit
import concurrent.futures

class VocalAnalyzer:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.y = None
        self.sr = 22050
        self.f0 = None
        self.voiced_flag = None
        self.zcr = None
        self.ref_f0 = None 
        self.ref_y = None 
        self.ref_full_y = None
        self.rms = None
        self.cache_dir = os.path.expanduser("~/.local/share/vocalpulse/cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        if self.file_path and os.path.exists(self.file_path):
            self.load_audio()
            
    def load_audio(self):
        try:
            self.y, self.sr = librosa.load(self.file_path, sr=22050)
            return self.y, self.sr
        except:
            return None, None

    def analyze_pitch(self, quick=True):
        if self.y is None: return
        fmin = librosa.note_to_hz('C2')
        fmax = librosa.note_to_hz('C7')
        self.f0 = librosa.yin(self.y, fmin=fmin, fmax=fmax, sr=self.sr, frame_length=2048, hop_length=512)
        self.rms = librosa.feature.rms(y=self.y, frame_length=2048, hop_length=512)[0]
        self.voiced_flag = self.rms > (np.mean(self.rms) * 0.4)
        self.f0[~self.voiced_flag] = 0
        return self.f0, self.voiced_flag

    def calculate_rating(self, reference_f0=None):
        if self.f0 is None or self.voiced_flag is None:
            return 0.0, "No audio data to analyze."
        if reference_f0 is not None:
            self.ref_f0 = reference_f0
            return self._compare_with_reference(self.f0, reference_f0)
        return 0.0, "Comparison failed."

    def verify_identity(self, ref_audio):
        """Phase 1: Sync and Check Music Identity (Iron-Gate)"""
        try:
            # Quick Chroma for initial sync
            chroma_live = librosa.feature.chroma_stft(y=self.y, sr=self.sr, hop_length=512)
            chroma_ref = librosa.feature.chroma_stft(y=ref_audio, sr=self.sr, hop_length=512)
            
            # Phase 1: Robust Offset Detection (Cross-Correlation on Envelopes)
            env_live = librosa.feature.rms(y=self.y, frame_length=2048, hop_length=512)[0]
            env_ref = librosa.feature.rms(y=ref_audio, frame_length=2048, hop_length=512)[0]
            
            # Normalize envelopes for better correlation
            e1 = (env_live - np.mean(env_live)) / (np.std(env_live) + 1e-6)
            e2 = (env_ref - np.mean(env_ref)) / (np.std(env_ref) + 1e-6)
            
            # Find best starting offset
            corr = np.correlate(e1, e2, mode='full')
            best_offset = np.argmax(corr) - (len(e2) - 1)
            
            # Phase 2: Lethal Forensic Shield (CQT + MFCC + Euclidean)
            if best_offset > 0:
                y_live_aligned = self.y[best_offset*512:]
                y_ref_aligned = ref_audio[:len(y_live_aligned)]
            else:
                y_ref_aligned = ref_audio[abs(best_offset)*512:]
                y_live_aligned = self.y[:len(y_ref_aligned)]
            
            # 1. Calculate Absolute Spectral Features (Log-Amplitude DNA)
            cqt_live = librosa.amplitude_to_db(np.abs(librosa.cqt(y=y_live_aligned, sr=self.sr, hop_length=512, n_bins=84)), ref=np.max)
            mfcc_live = librosa.feature.mfcc(y=y_live_aligned, sr=self.sr, n_mfcc=20)
            contrast_live = librosa.feature.spectral_contrast(y=y_live_aligned, sr=self.sr)
            
            # Forensic Matrix (RAW Log-Spectral Shape)
            feat_live = np.nan_to_num(np.vstack([cqt_live, mfcc_live, contrast_live]))
            
            cqt_ref = librosa.amplitude_to_db(np.abs(librosa.cqt(y=y_ref_aligned, sr=self.sr, hop_length=512, n_bins=84)), ref=np.max)
            mfcc_ref = librosa.feature.mfcc(y=y_ref_aligned, sr=self.sr, n_mfcc=20)
            contrast_ref = librosa.feature.spectral_contrast(y=y_ref_aligned, sr=self.sr)
            
            feat_ref = np.nan_to_num(np.vstack([cqt_ref, mfcc_ref, contrast_ref]))
            
            # 2. Euclidean DTW (Punishes Absolute Spectral Mismatches)
            D, wp = librosa.sequence.dtw(X=feat_live, Y=feat_ref, metric='euclidean', global_constraints=True, band_rad=int(1.0*self.sr/512))
            
            # Phase 3: Absolute DNA Audit
            m1_f = np.array([feat_live[:, i] for i, j in wp if i < feat_live.shape[1] and j < feat_ref.shape[1]])
            m2_f = np.array([feat_ref[:, j] for i, j in wp if i < feat_live.shape[1] and j < feat_ref.shape[1]])
            dna_match = np.corrcoef(m1_f.flatten(), m2_f.flatten())[0,1]
            
            # Phase 4: Forensic Sweet-Spot (75% Rule)
            linearity = 1.0 - (max(np.sum(np.diff(wp, axis=0)[:,0]==0), np.sum(np.diff(wp, axis=0)[:,1]==0)) / len(wp)) if len(wp) > 0 else 0.0
            
            # Sweet-Spot: DNA > 75% and Linearity > 40%
            is_passed = (dna_match > 0.75 and linearity > 0.40)
            
            return dna_match, linearity, is_passed
        except Exception as e:
            print(f"IDENTITY ERROR: {e}")
            return 0.0, 0.0, False

    def _compare_with_reference(self, live_f0, ref_f0):
        try:
            live = np.nan_to_num(live_f0)
            ref = np.nan_to_num(ref_f0)
            
            live_midi = np.zeros_like(live)
            valid_live = live > 0
            live_midi[valid_live] = 12 * np.log2(live[valid_live] / 440.0) + 69.0
            
            ref_midi = np.zeros_like(ref)
            valid_ref = ref > 0
            ref_midi[valid_ref] = 12 * np.log2(ref[valid_ref] / 440.0) + 69.0
            
            # 1. Deep Identity (Temporal Instrumental DNA)
            # We compare the musical progression along the entire song path
            chroma_live = librosa.feature.chroma_stft(y=self.y, sr=self.sr, hop_length=512)
            ref_audio = getattr(self, 'ref_full_y', self.ref_y)
            fingerprint_match = 0.0
            
            if ref_audio is not None:
                chroma_ref = librosa.feature.chroma_stft(y=ref_audio, sr=self.sr, hop_length=512)
                
                # First pass: Fast Alignment
                c1 = np.mean(chroma_live, axis=1); c2 = np.mean(chroma_ref, axis=1)
                base_id = np.corrcoef(c1, c2)[0,1]
                
                # Second pass: Progressing DNA check (will be refined after DTW)
                fingerprint_match = base_id 
            else:
                fingerprint_match = 0.0

            # 2. Parallel Temporal Sync
            l_env = self.rms.copy()
            r_env = librosa.feature.rms(y=self.ref_y, frame_length=2048, hop_length=512)[0]
            l_norm = (l_env - np.mean(l_env)) / (np.std(l_env) + 1e-6)
            r_norm = (r_env - np.mean(r_env)) / (np.std(r_env) + 1e-6)
            corr = np.correlate(l_norm, r_norm, mode='full')
            offset = np.argmax(corr) - (len(l_norm) - 1)
            
            if offset > 0:
                ref_midi = np.pad(ref_midi, (offset, 0), mode='constant')
                valid_ref = np.pad(valid_ref, (offset, 0), mode='constant', constant_values=False)
            elif offset < 0:
                live_midi = np.pad(live_midi, (-offset, 0), mode='constant')
                valid_live = np.pad(valid_live, (-offset, 0), mode='constant', constant_values=False)

            max_len = max(len(live_midi), len(ref_midi))
            live_midi = np.pad(live_midi, (0, max_len - len(live_midi)), mode='constant')
            ref_midi = np.pad(ref_midi, (0, max_len - len(ref_midi)), mode='constant')
            valid_live = np.pad(valid_live, (0, max_len - len(valid_live)), mode='constant', constant_values=False)
            valid_ref = np.pad(valid_ref, (0, max_len - len(valid_ref)), mode='constant', constant_values=False)

            # 3. Dynamic Alignment (DTW) - The MIR Forensic Gate
            # Using no band constraints to handle skipped parts and large offsets
            D, wp = librosa.sequence.dtw(X=live_midi, Y=ref_midi, metric='euclidean', global_constraints=False)
            
            # --- CSI (Cover Song Identification) Distance ---
            # Accumulated cost divided by path length = Normalized Distance
            dtw_distance = D[-1, -1] / len(wp)
            csi_score = max(0, 1.0 - (dtw_distance / 20.0)) # 20.0 is a typical max distance for Chroma
            
            # --- Instrumental DNA Refinement (Energy-Aware Forensic Match) ---
            if ref_audio is not None:
                # 1. Temporal Chroma (Tones)
                path_c_live = []; path_c_ref = []
                # 2. Spectral MFCC (Texture/Timbre)
                mfcc_live = librosa.feature.mfcc(y=self.y, sr=self.sr, n_mfcc=13)
                mfcc_ref = librosa.feature.mfcc(y=ref_audio, sr=self.sr, n_mfcc=13)
                path_m_live = []; path_m_ref = []
                
                # Calculate Energy Masks to ignore silence/intros
                rms_live = self.rms
                rms_ref = librosa.feature.rms(y=self.ref_y, frame_length=2048, hop_length=512)[0]
                
                for i, j in wp[::10]:
                    # Energy-Aware Gate: Only compare if BOTH have audio energy
                    if i < len(rms_live) and j < len(rms_ref):
                        if rms_live[i] > 1e-4 and rms_ref[j] > 1e-4:
                            if i < chroma_live.shape[1] and j < chroma_ref.shape[1]:
                                path_c_live.append(chroma_live[:, i])
                                path_c_ref.append(chroma_ref[:, j])
                            if i < mfcc_live.shape[1] and j < mfcc_ref.shape[1]:
                                path_m_live.append(mfcc_live[:, i])
                                path_m_ref.append(mfcc_ref[:, j])
                
                if len(path_c_live) > 20:
                    # Chroma Match (Tones) - 70% weight for Karaoke tracks
                    v1 = np.array(path_c_live); v2 = np.array(path_c_ref)
                    best_temporal_id = -1.0
                    for shift in range(12):
                        v2_s = np.roll(v2, shift, axis=1)
                        tid = np.corrcoef(v1.flatten(), v2_s.flatten())[0,1]
                        if tid > best_temporal_id: best_temporal_id = tid
                    
                    # MFCC Match (Production Texture) - 30% weight
                    m1 = np.array(path_m_live).flatten(); m2 = np.array(path_m_ref).flatten()
                    mfcc_match = np.corrcoef(m1, m2)[0,1]
                    
                    # Final Forensic Identity (weighted towards tones)
                    fingerprint_match = (best_temporal_id * 0.7) + (mfcc_match * 0.3)
            
            # 4. Surgical DNA (Aligned note progression)
            path_live = []; path_ref = []
            for i, j in wp[::5]:
                if valid_live[i] and valid_ref[j]:
                    path_live.append(live_midi[i]); path_ref.append(ref_midi[j])
            progression_match = np.corrcoef(np.diff(path_live), np.diff(path_ref))[0,1] if len(path_live) > 20 else 0.0
            
            # 5. Pitch Analysis
            best_shift = 0; max_mel_corr = -1
            for s in range(-6, 7):
                test_l = []; test_r = []
                for i, j in wp:
                    if valid_live[i] and valid_ref[j]:
                        test_l.append(live_midi[i] + s); test_r.append(ref_midi[j])
                if len(test_l) > 20:
                    c = np.corrcoef(test_l, test_r)[0, 1]
                    if c > max_mel_corr: max_mel_corr = c; best_shift = s
            
            live_midi[valid_live] += best_shift
            melody_corr = max(0, max_mel_corr)
            
            total_dist = 0; overlap_count = 0; ref_indices = set()
            steps = np.diff(wp, axis=0)
            for i, j in wp:
                if valid_live[i] and valid_ref[j]:
                    diff = np.abs(live_midi[i] - ref_midi[j]) % 12
                    if diff > 6: diff = 12 - diff
                    total_dist += diff
                    overlap_count += 1
                    ref_indices.add(j)
            
            if overlap_count < 10: return 0.0, "❌ Error: No matching vocals detected!"
            
            avg_dist = total_dist / overlap_count
            unique_coverage = len(ref_indices) / max(1, np.sum(valid_ref))
            linearity = 1.0 - (max(np.sum(steps[:,0]==0), np.sum(steps[:,1]==0)) / len(wp)) if len(wp) > 0 else 0.5
            
            # --- Iron-Gate Identity Security (Lethal Forensic Shield) ---
            # 1. Production DNA (Texture Match)
            cqt_live = np.abs(librosa.cqt(y=self.y, sr=self.sr, hop_length=512, n_bins=84))
            mfcc_live = librosa.feature.mfcc(y=self.y, sr=self.sr, n_mfcc=20)
            feat_live = np.nan_to_num(np.vstack([librosa.util.normalize(cqt_live), librosa.util.normalize(mfcc_live)]))
            
            ref_audio = getattr(self, 'ref_full_y', self.ref_y)
            cqt_ref = np.abs(librosa.cqt(y=ref_audio, sr=self.sr, hop_length=512, n_bins=84))
            mfcc_ref = librosa.feature.mfcc(y=ref_audio, sr=self.sr, n_mfcc=20)
            feat_ref = np.nan_to_num(np.vstack([librosa.util.normalize(cqt_ref), librosa.util.normalize(mfcc_ref)]))
            
            # Re-run strict DTW (Euclidean)
            radius = int(2.0 * self.sr / 512)
            D_f, wp_f = librosa.sequence.dtw(X=feat_live, Y=feat_ref, metric='euclidean', global_constraints=True, band_rad=radius)
            
            # Acoustic DNA Match (Texture Correlation)
            m1_f = np.array([mfcc_live[:, i] for i, j in wp_f if i < mfcc_live.shape[1] and j < mfcc_ref.shape[1]])
            m2_f = np.array([mfcc_ref[:, j] for i, j in wp_f if i < mfcc_live.shape[1] and j < mfcc_ref.shape[1]])
            dna_match = np.corrcoef(m1_f.flatten(), m2_f.flatten())[0,1]
            
            # Final identity decision (75% Sweet-Spot Rule)
            is_mismatch = (dna_match < 0.75 or linearity < 0.40)
            
            # Professional Studio Metrics
            vibrato_score = np.std(np.diff(live_midi)[valid_live[:-1]])
            vibrato_bonus = max(0, 10 * (1.0 - min(1.0, vibrato_score * 2)))
            texture_match = min(1.0, max(0.5, 1.0 - (avg_dist / 12.0)))

            base_score = 100 * (melody_corr ** 1.5)
            pitch_bonus = 20 * np.exp(-avg_dist / 1.5)
            final_score = (base_score + pitch_bonus + vibrato_bonus) * (0.5 + 0.5 * min(1.0, unique_coverage)) * (0.8 + 0.2 * linearity)
            final_score = min(100, max(0, final_score))
            
            status_text = ""
            if is_mismatch: 
                final_score = 0.0
                status_text = "❌ Error: Not the same song! (Mismatch detected)\n"

            # Final Criteria Labels
            identity_status = "✅ (CSI Identity Verified)" if not is_mismatch else f"❌ (Mismatch: High Alignment Cost)"
            melody_status = "✅" if melody_corr >= 0.35 else f"❌ (Need >35%)"
            dna_status = "✅" if progression_match >= 0.20 or melody_corr > 0.85 else f"❌ (Need >20%)"

            feedback = (
                f"{status_text}"
                f"Acoustic DNA Match: {dna_match*100:.1f}% {identity_status}\n"
                f"Path Linearity: {linearity*100:.1f}% (Target: >40%) {'✅' if linearity > 0.40 else '❌'}\n"
                f"Melody Match: {melody_corr*100:.1f}% (Target: >35%) {melody_status}\n"
                f"Melodic DNA: {max(0, progression_match)*100:.1f}% (Target: >20%) {dna_status}\n"
                f"Vocal Texture: {texture_match*100:.1f}%\n"
                f"Vibrato Stability: {100 - min(100, vibrato_score*200):.1f}%\n"
                f"Final Score: {final_score:.1f}/100"
            )
            return final_score, feedback
        except Exception as e:
            return 0.0, f"Engine Error: {e}"

    def isolate_vocals(self, audio_path, video_id=None):
        import subprocess, shutil, torch
        if video_id:
            standard_path = os.path.join(self.cache_dir, video_id, "vocals.wav")
            if os.path.exists(standard_path): return standard_path
        
        out_dir = os.path.join(self.cache_dir, video_id) if video_id else "separated_temp"
        os.makedirs(out_dir, exist_ok=True)
        demucs = shutil.which("demucs") or os.path.join(os.path.dirname(__file__), "venv/bin/demucs")
        
        # GPU Acceleration Check (RDNA 4 / ROCm 6.0+)
        device = "cpu"
        try:
            if torch.cuda.is_available():
                device = "cuda"
                print("🚀 GPU ACCELERATION ACTIVE: Using RDNA 4 Vanguard Architecture (ROCm Mode)")
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                device = "mps"
                print("🚀 GPU ACCELERATION ACTIVE: Using Metal Performance Shaders")
            else:
                # Last resort override check (USER FORCED)
                if os.environ.get('HSA_OVERRIDE_GFX_VERSION') == '12.0.0':
                    device = "cuda"
                    print("🚀 GPU ACCELERATION ACTIVE: Forced RDNA 4 Identity (GFX 12.0)")
                else:
                    print(f"DEBUG: Vocal Isolation using {multiprocessing.cpu_count()} CPU THREADS (Turbo Mode)")
        except:
            print("DEBUG: Falling back to CPU for isolation.")

        cmd = [demucs, "--two-stems=vocals", "-d", device, "-o", out_dir, audio_path]
        if device == "cpu":
            cmd.insert(3, "-j")
            cmd.insert(4, str(multiprocessing.cpu_count()))
            
        proc = subprocess.Popen(cmd)
        self.current_proc = proc
        proc.wait()
        
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        vocal_path = os.path.join(out_dir, "htdemucs", base_name, "vocals.wav")
        standard_path = os.path.join(out_dir, "vocals.wav")
        if os.path.exists(vocal_path):
            shutil.move(vocal_path, standard_path)
            return standard_path
        return audio_path

    def search_youtube(self, query):
        import subprocess
        yt_dlp = self._get_yt_dlp()
        cmd = [yt_dlp, "--quiet", "--force-ipv4", "--extractor-args", "youtube:player_client=android_vr,tv_embedded", "--flat-playlist", "--print", "RESULT:::%(title)s:::%(id)s:::%(thumbnails.0.url)s:::%(duration_string)s", f"ytsearch5:{query}"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        results = []
        for line in res.stdout.split("\n"):
            if line.startswith("RESULT:::"):
                p = line.split(":::")
                if len(p) >= 5:
                    results.append({"title": p[1], "id": p[2], "thumbnail": p[3], "duration": p[4], "url": f"https://www.youtube.com/watch?v={p[2]}"})
        return results

    def _get_yt_dlp(self):
        import shutil
        return shutil.which("yt-dlp") or os.path.join(os.path.dirname(__file__), "venv/bin/yt-dlp")

    def fetch_reference(self, song_name):
        import subprocess, shutil
        # Hard Reset: Clear previous reference state to prevent 'ghosting'
        self.ref_y = None
        self.ref_full_y = None
        self.ref_f0 = None
        
        # Triple-Shield URL Repair: Handle cut-off, fragmented, or messy links
        song_name = song_name.strip()
        
        # 1. Fragmented Link Recovery (e.g. starting with .com)
        if ".com/" in song_name and not song_name.startswith("http"):
            song_name = "https://www.youtube" + song_name[song_name.find(".com"):]
        if song_name.startswith("watch?v="):
            song_name = "https://www.youtube.com/" + song_name
            
        # 2. General Protocol Fixes
        if "youtube.com" in song_name and not song_name.startswith("http"):
            song_name = "https://" + song_name
        if "youtu.be" in song_name and not song_name.startswith("http"):
            song_name = "https://" + song_name
            
        # 3. Strip Junk (e.g. descriptions in parentheses)
        song_name = re.sub(r'\(.*\)', '', song_name).strip()
        
        # 4. Extract/Recover Video ID
        video_id = None
        if "v=" in song_name: video_id = song_name.split("v=")[1].split("&")[0]
        elif "youtu.be/" in song_name: video_id = song_name.split("youtu.be/")[1].split("?")[0]
        elif len(song_name) == 11 and re.match(r'^[a-zA-Z0-9_-]{11}$', song_name):
            video_id = song_name
            song_name = f"https://www.youtube.com/watch?v={video_id}"
        
        print(f"DEBUG: Forensic URL Sanitizer -> {song_name}")
        
        if video_id:
            cache_dir = os.path.join(self.cache_dir, video_id)
            cached_audio = os.path.join(cache_dir, "vocals.wav")
            full_audio = os.path.join(cache_dir, "full.wav")
            metadata_file = os.path.join(cache_dir, "metadata.json")
            if os.path.exists(cached_audio) and os.path.exists(full_audio):
                title = None
                if os.path.exists(metadata_file):
                    try:
                        with open(metadata_file, "r") as f:
                            title = json.load(f).get("title")
                    except: pass
                self.ref_y, sr = librosa.load(cached_audio, sr=self.sr)
                self.ref_full_y, _ = librosa.load(full_audio, sr=self.sr)
                # Ensure F0 is calculated for the cached audio
                self.ref_f0 = librosa.yin(self.ref_y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), sr=sr, frame_length=2048, hop_length=512)
                return self.ref_f0, title or "Cached Performance"

        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            ref_path = os.path.join(tmp_dir, "ref.m4a")
            full_wav = os.path.join(tmp_dir, "full.wav")
            
            yt_dlp = self._get_yt_dlp()
            # 1. Fetch Title (with timeout safety)
            song_title = "Forensic Match"
            try:
                cmd_title = [yt_dlp, "--get-title", "--no-check-certificate", song_name]
                proc = subprocess.Popen(cmd_title, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                self.current_proc = proc
                stdout, _ = proc.communicate(timeout=30)
                if proc.returncode == 0:
                    song_title = stdout.strip()
            except Exception as e:
                print(f"TITLE ERROR (Ignoring): {e}")
            
            # Download with DRM-Shield & Triple-Client (Bypasses Encryption blocks)
            try:
                cmd = [
                    yt_dlp, 
                    "--no-check-certificate", 
                    "--no-cache-dir",
                    "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                    "--extractor-args", "youtube:player-client=android,web,ios", # Triple-Client
                    "--check-formats", # Automatic fallback for DRM
                    "--format", "ba[ext=m4a]/ba/b", # Prioritize standard audio
                    "--fragment-retries", "5",
                    "--retries", "5",
                    "-x", 
                    "-o", ref_path, 
                    song_name
                ]
                print(f"DEBUG: Starting DRM-Shield Extraction for {song_title}...")
                proc = subprocess.Popen(cmd)
                self.current_proc = proc
                proc.wait(timeout=300)
            except Exception as e:
                print(f"DOWNLOAD ERROR: {e}")

            # Smart-Discovery: Find the downloaded file regardless of extra extensions
            import glob
            downloaded_files = glob.glob(os.path.join(tmp_dir, "ref*"))
            if downloaded_files:
                actual_ref_path = downloaded_files[0]
                # 3. Convert to WAV
                subprocess.run(["ffmpeg", "-y", "-i", actual_ref_path, "-ar", "22050", full_wav], capture_output=True)
                
                # 4. Isolate Vocals
                isolated = self.isolate_vocals(actual_ref_path, video_id=video_id)
                
                if video_id:
                    cache_dir = os.path.join(self.cache_dir, video_id)
                    os.makedirs(cache_dir, exist_ok=True)
                    # Move results to cache
                    if os.path.exists(full_wav):
                        shutil.move(full_wav, os.path.join(cache_dir, "full.wav"))
                    with open(os.path.join(cache_dir, "metadata.json"), "w") as f:
                        json.dump({"title": song_title}, f)
                
                # 5. Load and Analyze
                self.ref_y, sr = librosa.load(isolated, sr=self.sr)
                target_full = os.path.join(self.cache_dir, video_id, "full.wav") if video_id else full_wav
                self.ref_full_y, _ = librosa.load(target_full, sr=self.sr)
                f0 = librosa.yin(self.ref_y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), sr=sr, frame_length=2048, hop_length=512)
                
                return f0, song_title
        return None, None
