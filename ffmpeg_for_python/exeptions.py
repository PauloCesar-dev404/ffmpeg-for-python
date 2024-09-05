import time

INPUT_ERROR = [
    'Error opening input: No such file or directory',
    'Error opening input: Permission denied',
    'Error opening input: Invalid argument',
    'Error opening input: Protocol not found',
    'Error opening input: Unsupported protocol',
    'Error opening input: File format not recognized',
    'Error opening input: Could not open file',
    'Error opening input: Invalid data found when processing input',
    'Error opening input: Input stream is empty',
    'Error opening input: Cannot open file for reading',
    'Error opening input: File is too short',
    'Error opening input: End of file while parsing input',
    'Error opening input: Codec not found',
    'Error opening input: No decoder for codec',
    'Error opening input: Stream not found',
    'Error opening input: Stream codec not found',
    'Error opening input: Stream index out of range',
    'Error opening input: Invalid timestamp',
    'Error opening input: Corrupt file',
    'Error opening input: Unsupported codec',
    'Error opening input: Failed to initialize filter',
    'Error opening input: Error while opening codec',
    'Error opening input: Device not found',
    'Error opening input: Device or resource busy',
    'Error opening input: Invalid option',
    'Error opening input: Unable to seek',
    'Error opening input: Input format not found'
]
OUTPUT_ERROR = [
    'Error opening output file: No such file or directory',
    'Error opening output file: Permission denied',
    'Error opening output file: Invalid argument',
    'Error opening output file: Unsupported protocol',
    'Error opening output file: Protocol not found',
    'Error opening output file: File format not recognized',
    'Error opening output file: Could not open file for writing',
    'Error opening output file: Disk full or quota exceeded',
    'Error opening output file: Cannot create file',
    'Error opening output file: Invalid data found when processing output',
    'Error opening output file: Output stream not found',
    'Error opening output file: Cannot write to file',
    'Error opening output file: File already exists',
    'Error opening output file: Unsupported codec',
    'Error opening output file: Codec not found',
    'Error opening output file: Cannot open codec for writing',
    'Error opening output file: Failed to initialize filter',
    'Error opening output file: Invalid option',
    'Error opening output file: Invalid timestamp',
    'Error opening output file: Corrupt file',
    'Error opening output file: Device or resource busy',
    'Error opening output file: Cannot seek',
    'Error opening output file: Stream index out of range',
    'Error opening output file: Stream codec not found'
]
ERROS = []
for er in INPUT_ERROR:
    ERROS.append(er)
for er in OUTPUT_ERROR:
    ERROS.append(er)


class FFmpegExceptions(Exception):
    def __init__(self, message: str):
        super().__init__(message)

    def __str__(self):
        """
        Retorna a representação em string da exceção.

        Returns:
            str: Mensagem de erro formatada com detalhes adicionais, se presentes.
        """

        return super().__str__()


def wraper_erros(line: str):
    """Verifica se a linha de saida do ffmpeg está no dict de erros e retorna sua categoria"""

    if "Error" in line:
        erro = line.split('Error')[1]
        return erro.strip()
    elif 'already exists. Overwrite? [y/N]' in line:
        erro = line.split('File')[1]
        return erro.strip()



