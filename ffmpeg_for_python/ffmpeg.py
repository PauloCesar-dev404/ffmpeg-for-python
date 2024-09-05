import os
import platform
import subprocess
import time
from typing import List, Optional
from .exeptions import wraper_erros, FFmpegExceptions
from .__config__ import Configurate

parser = Configurate()
parser.configure()
ffmpeg_binarie = os.path.join(parser.INSTALL_DIR, parser.FFMPEG_BINARY)


def ffmpeg(cls):
    """Decorador que instancia automaticamente a classe FFmpeg."""

    def wrapper(*args, **kwargs):
        # Cria e retorna uma instância da classe FFmpeg
        instance = cls(*args, **kwargs)
        return instance

    return wrapper


@ffmpeg
class FFmpeg:
    """Wrapper para o binário FFmpeg, permitindo o uso de comandos FFmpeg via Python."""

    def __init__(self):
        # Verifica se o binário do FFmpeg existe
        if not self.__verify_path(bin_path=ffmpeg_binarie, path_type='file'):
            parser.install_bins()
        self.__ffmpeg_path = str(ffmpeg_binarie)
        self.__command = [self.__ffmpeg_path]
        self.__overwrite_output = False

    def args(self, arguments: List[str]) -> 'FFmpeg':
        """Adiciona múltiplos argumentos personalizados ao comando FFmpeg."""
        if not all(isinstance(arg, str) for arg in arguments):
            raise TypeError("All arguments should be provided as strings.")
        self.__command.extend(arguments)
        return self

    def run(self, capture_output: bool = False):
        """Executa o comando FFmpeg construído.

        Args:
            capture_output (bool): Se verdadeiro, captura a saída padrão e de erro.

        Returns:
            Optional[str]: A saída do comando, se capturada. Caso contrário, None.
        """

        configs = self.__oculte_comands_your_system.get('startupinfo')
        # Armazenar a saída completa, se for necessário capturá-la
        output = []

        # Executa o comando utilizando subprocess
        with subprocess.Popen(
                self.__command,
                startupinfo=configs,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,  # Linha por linha
                universal_newlines=True  # Garante que novas linhas sejam interpretadas corretamente
        ) as process:
            # Lê a saída de erro padrão (stderr) em tempo real
            for linha in process.stderr:
                time.sleep(0.01)
                linha_filtrada = wraper_erros(linha)
                if linha_filtrada:
                    process.terminate()
                    raise FFmpegExceptions(message=f'Erro na execução do ffmpeg: "{linha_filtrada}"')
                else:
                    if capture_output:
                        print(linha.strip())

            # Espera o processo terminar e captura a saída padrão (stdout)
            stdout, stderr = process.communicate()

            if capture_output:
                output.extend(stdout.splitlines())
                return '\n'.join(output)
            else:
                return stdout.strip() if stdout else None

    def input(self, file_path: str) -> 'FFmpeg':
        """Define o arquivo de entrada para o FFmpeg."""
        cmd = ['-i', file_path]
        self.args(cmd)
        return self

    def output(self, output_path: str) -> 'FFmpeg':
        """Define o arquivo de saída para o FFmpeg e verifica se a sobrescrita está permitida."""
        if os.path.exists(output_path):
            if not self.__overwrite_output:
                raise FFmpegExceptions(f"O arquivo de saída '{output_path}' já existe! Use 'overwrite_output' para "
                                       f"sobrescrevê-lo.")

        # Adiciona o arquivo de saída ao comando
        cmd = [output_path]
        self.args(cmd)
        return self

    @property
    def overwrite_output(self):
        """
        Adiciona o parâmetro '-y' ao comando FFmpeg, o que permite sobrescrever o arquivo de saída
        caso ele já exista.

        Importante: Esta propriedade deve ser definida antes dos parâmetros de entrada e saída
        para garantir que o comando FFmpeg seja construído corretamente. Caso contrário, o comando
        pode não ser executado como esperado.

        Returns:
            FFmpeg: Retorna a instância atual para encadeamento de métodos.
        """
        self.__overwrite_output = True
        cmd = ['-y']
        self.args(cmd)
        return self

    @property
    def copy(self) -> 'FFmpeg':
        """Adiciona o parâmetro '-c copy' ao comando FFm"""
        self.__command.extend(['-c', 'copy'])
        return self

    @property
    def reset(self) -> 'FFmpeg':
        """Reseta o comando para reutilização do objeto."""
        self.__command = [self.__ffmpeg_path]
        return self

    @staticmethod
    def __verify_path(bin_path, path_type: str) -> bool:
        """
        Verifica se um caminho de arquivo ou diretório existe.

        Args:
            bin_path : O caminho a ser verificado.
            path_type (str): O tipo de caminho ('file' para arquivo, 'dir' para diretório).

        Returns:
            bool: True se o caminho existir e for do tipo especificado, False caso contrário.
        """
        if path_type == 'file':
            return os.path.isfile(bin_path)
        elif path_type == 'dir':
            return os.path.isdir(bin_path)
        else:
            raise ValueError("Invalid path_type. Use 'file' or 'dir'.")

    @property
    def __oculte_comands_your_system(self):
        """Identifica o sistema do usuário e cria um dicionário de parâmetros para ocultar saídas de janelas."""
        system_user = platform.system()
        startupinfo_options = {}

        if system_user == "Windows":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            startupinfo_options['startupinfo'] = startupinfo

        elif system_user in ["Linux", "Darwin"]:
            startupinfo_options['stdout'] = subprocess.DEVNULL
            startupinfo_options['stderr'] = subprocess.DEVNULL
            startupinfo_options['stdin'] = subprocess.DEVNULL

        else:
            raise NotImplementedError(f"System {system_user} not supported")

        return startupinfo_options


