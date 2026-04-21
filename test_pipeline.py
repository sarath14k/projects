import sys; sys.path.append('/home/sarath/.local/share/vocalpulse')
from vocal_analyzer import VocalAnalyzer
import librosa
analyzer = VocalAnalyzer('/home/sarath/Downloads/Music/8725724364465589_1763674787594.m4a')
analyzer.load_audio()
analyzer.analyze_pitch(quick=True)
ref_f0, song_title = analyzer.fetch_reference('https://www.youtube.com/watch?v=dAezp422I_A')
if ref_f0 is not None:
    score, feedback = analyzer.calculate_rating(ref_f0)
    print(f'\n\n=== FINAL RESULT ===')
    print(f'Song: {song_title}')
    print(f'Score: {score:.1f}/100')
    print(f'Feedback: {feedback}')
else:
    print('Failed to download YouTube audio')
