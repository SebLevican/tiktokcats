import random
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import glob
from time import sleep

def is_valid_video(video_path):
    try:
        clip = VideoFileClip(video_path)
        clip.reader.close()
        if clip.audio:
            clip.audio.reader.close_proc()
        return True
    except Exception as e:
        print(f"Video no válido: {video_path}, Error: {e}")
        return False

def normalize_video_with_borders(video_path, resolution=(1080, 1920), fps=30):
    video = VideoFileClip(video_path)
    video = video.set_fps(fps)
    video = video.resize(height=resolution[1]) if video.size[1] < resolution[1] else video.resize(width=resolution[0])
    return video.on_color(size=resolution, color=(0, 0, 0))

def join_videos(num_videos,min_total):
    # Define la carpeta que contiene los videos
    carpeta = 'videos'
    # Define el patrón para buscar los archivos de video
    patron = os.path.join(carpeta, '*.mp4')

    # Obtiene una lista de rutas de los videos que deseas unir
    videos_mp4 = glob.glob(patron)

    # Filtra los videos válidos
    videos_mp4_validos = [video for video in videos_mp4 if is_valid_video(video)]

    # Cargar y normalizar cada video válido como un objeto VideoFileClip
    video_clips = [normalize_video_with_borders(video_path) for video_path in videos_mp4_validos]

    # Verificar que hay suficientes videos válidos
    if len(video_clips) < num_videos:
        raise ValueError(f"No hay suficientes videos válidos en la carpeta para seleccionar al menos {num_videos}.")

    # Elegir aleatoriamente entre 11 y 14 videos
    num_videos = random.randint(num_videos, num_videos+3)
    video_clips_seleccionados = random.sample(video_clips, num_videos)

    # Guardar las rutas de los videos seleccionados
    rutas_videos_seleccionados = [videos_mp4_validos[video_clips.index(clip)] for clip in video_clips_seleccionados]

    # Agregar más videos si la duración total es menor a 10 minutos
    def duracion_total(clips):
        return sum(clip.duration for clip in clips) / 60

    while duracion_total(video_clips_seleccionados) < min_total and len(video_clips_seleccionados) < len(video_clips):
        # Elegir un clip aleatorio que aún no esté en la selección
        nuevo_clip = random.choice([clip for clip in video_clips if clip not in video_clips_seleccionados])
        video_clips_seleccionados.append(nuevo_clip)
        rutas_videos_seleccionados.append(videos_mp4_validos[video_clips.index(nuevo_clip)])

    # Unir los clips de video seleccionados
    video_final = concatenate_videoclips(video_clips_seleccionados)

    # Especificar la ruta donde deseas guardar el video final
    ruta_video_final = 'videos/subir/video1.mp4'

    # Guardar el video final en el archivo especificado
    video_final.write_videofile(ruta_video_final, codec='libx264', audio_codec='aac')

    # Cerrar los clips de video seleccionados para liberar recursos
    for clip in video_clips_seleccionados:
        clip.close()

    sleep(600)

    # Eliminar los videos que se utilizaron
    for video_path in rutas_videos_seleccionados:
        os.remove(video_path)
        print(f"Eliminado: {video_path}")

    print("¡Videos unidos y eliminados exitosamente!")
