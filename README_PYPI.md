# ffmpeg-for-python

Wrapper para o binário FFmpeg, permitindo o uso de comandos FFmpeg via Python. Para saber como usar FFmpeg, consulte a documentação no [site oficial](https://ffmpeg.org/ffmpeg.html)


---


**conversão básica**

```python

from ffmpeg_for_python import FFmpeg, FFmpegExceptions

# Cria uma instância do wrapper FFmpeg
ffmpeg = FFmpeg()
# Caminho do arquivo de entrada e saída
input_video = 'input_video.mp4'
output_video = 'output_video.mkv'

# Define o arquivo de entrada e o arquivo de saída
(ffmpeg
        .overwrite_output  # Sobrescrever se existir
        .input(input_video)  # Vídeo de entrada
        .output(output_video)  # Vídeo final
)

    # Executa o comando FFmpeg e exibe a saída
try:
        ffmpeg.run(capture_output=True)
except FFmpegExceptions as e:
        print("Erro ao executar FFmpeg:", e)
```
---

**remux audio e video**

```python
from ffmpeg_for_python import FFmpeg, FFmpegExceptions
# Cria uma instância do wrapper FFmpeg
ffmpeg = FFmpeg()
# Caminho dos arquivos de entrada e saída
input_video = 'input_video.mp4'
input_audio = 'input_audio.mp4'
output_video = 'output_video.mp4'
# Define os arquivos de entrada e o arquivo de saída
(ffmpeg
        .overwrite_output  # Sobrescrever se existir
        .input(input_video)  # Vídeo de entrada
        .input(input_audio)  # Áudio
        .args(arguments=['-c:a', 'copy', '-c:v', 'copy'])  # Parâmetros de cópia de áudio e vídeo
        .output(output_video)  # Vídeo final
)

# Executa o comando FFmpeg e exibe a saída
try:
        ffmpeg.run(capture_output=True)
except FFmpegExceptions as e:
        print("Erro ao executar FFmpeg:", e)
```
---