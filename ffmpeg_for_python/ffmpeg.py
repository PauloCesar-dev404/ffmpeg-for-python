import os
import platform
import subprocess
import time
from typing import List
from .__config__ import Configurate
from .exeptions import wraper_erros, FFmpegExceptions

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
            capture_output (bool): Se verdadeiro, captura a saída e printa no console.
                                   Se False, a saída é retornada assincronamente em tempo real.

        Yields:
            str: Cada linha da saída filtrada do FFmpeg quando capture_output é False.
        """

        configs = self.__oculte_comands_your_system.get('startupinfo')

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
            try:
                # Lê a saída de erro padrão (stderr) em tempo real
                for linha in process.stderr:
                    time.sleep(0.01)  # Simulação de latência, opcional

                    # Filtra a linha de erro padrão
                    linha_filtrada = wraper_erros(linha)

                    if linha_filtrada:
                        # Se houver um erro detectado, o processo é encerrado
                        process.terminate()
                        raise FFmpegExceptions(message=f'Erro na execução do ffmpeg: "{linha_filtrada}"')
                    else:
                        if capture_output:
                            # Se `capture_output` estiver ativado, imprime a saída
                            print(linha.strip())
                        else:
                            # Retorna a linha assincronamente quando capture_output é False
                            yield linha.strip()

                # Aguarda a conclusão do processo
                process.wait()

            except Exception as e:
                process.terminate()
                raise FFmpegExceptions(message=f'Erro no processo FFmpeg: {str(e)}')

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
    def hide_banner(self) -> 'FFmpeg':
        """oculta o baner do ffmpeg"""
        self.__command.extend(['-hide_banner'])
        return self

    @property
    def copy(self) -> 'FFmpeg':
        """Adiciona o parâmetro '-c copy"""
        self.__command.extend(['-c', 'copy'])
        return self

    @property
    def copy_codecs(self):
        """para remuxar"""
        self.__command.extend(['-c:a', 'copy', '-c:v', 'copy'])
        return self

    def reset_ffmpeg(self) -> 'FFmpeg':
        """Reseta o comando para reutilização do objeto,isso é necessário em caso de uso em loops,
        a cada execução execute o reset para ter certeza que estar limpo o cache de comandos"""
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
    def __oculte_comands_your_system(self) -> dict:
        """Identifica o sistema do usuário e cria um dicionário de parâmetros para ocultar saídas de janelas e do
        terminal."""
        system_user = platform.system()
        startupinfo_options = {}

        if system_user == "Windows":
            # Configuração específica para ocultar o terminal no Windows
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            startupinfo_options['startupinfo'] = startupinfo

            # Definindo stdout, stderr e stdin para DEVNULL para esconder saídas
            startupinfo_options['stdout'] = subprocess.DEVNULL
            startupinfo_options['stderr'] = subprocess.DEVNULL
            startupinfo_options['stdin'] = subprocess.DEVNULL

        elif system_user in ["Linux", "Darwin"]:
            # Para Linux e macOS, ocultar stdout, stderr e stdin
            startupinfo_options['stdout'] = subprocess.DEVNULL
            startupinfo_options['stderr'] = subprocess.DEVNULL
            startupinfo_options['stdin'] = subprocess.DEVNULL

        else:
            # Exceção para sistemas não suportados
            raise NotImplementedError(f"O sistema {system_user} não é suportado para ocultação de comandos.")

        return startupinfo_options
