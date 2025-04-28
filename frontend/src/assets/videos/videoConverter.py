from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip

# Create text clip
text = TextClip("Let's Learn: 2 + 3 = 5", fontsize=50, color='white', size=(800, 600))
text = text.set_duration(10).set_position('center')

# Optional: Add background music
music = AudioFileClip("background_music.mp3").subclip(0, 10)

# Combine
video = CompositeVideoClip([text])
video = video.set_audio(music)
video.write_videofile("addition_lesson.mp4", fps=24)
