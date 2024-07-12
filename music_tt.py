import matplotlib.pyplot as plt
import numpy as np
from moviepy.editor import VideoClip, AudioFileClip
from moviepy.video.io.bindings import mplfig_to_npimage
from pydub import AudioSegment

audio = AudioSegment.from_mp3(YOURPATH)

samples = np.array(audio.get_array_of_samples())
sample_rate = audio.frame_rate
channels = audio.channels

duration = len(samples) / (sample_rate * channels)
fps = 30

fig, ax = plt.subplots()
fig.patch.set_facecolor("green")

audio_duration = len(audio) / 1000.0


def make_frame(t):
    ax.clear()

    start_index = int(t * sample_rate * channels)
    end_index = start_index + int(sample_rate/ fps *  channels)
    frame_samples = samples[start_index:end_index:channels]

    step = max(len(frame_samples)  // 10, 1)
    selected_samples = np.abs(frame_samples[::step][:10] * 2)

    ax.bar(np.arange(10), selected_samples, color="white")
    ax.set_ylim(0, 32767)
    ax.axis("off")

    return mplfig_to_npimage(fig)

animation = VideoClip(make_frame, duration=duration)

animation = animation.set_fps(fps)

audio_clip = AudioFileClip(YOURPATH)
animation = animation.set_audio(audioclip)

animation.write_videofile("audio.visualization.mp4", fps=fps, codec="libx264")