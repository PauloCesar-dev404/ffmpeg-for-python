import struct
import sys
import os
import requests
import zipfile
import shutil
import stat
from .exeptions import *
from .__utils import URL_PLATAFOMR,system

lib_name = 'ffmpeg_for_python'
URL_BASE_REPO = "https://raw.githubusercontent.com/PauloCesar-dev404/binarios/main/"




class Configurate:
    """Configura variáveis de ambiente no ambiente virtual ou globalmente."""

    def __init__(self):
        self.VERSION = self.__read_version
        self.FFMPEG_URL = os.getenv('FFMPEG_URL')
        self.FFMPEG_BINARY = os.getenv('FFMPEG_BINARY')
        PATH = os.path.join(self.is_venv, lib_name, 'ffmpeg-bin')
        os.makedirs(PATH, exist_ok=True)
        dirpath = PATH
        self.INSTALL_DIR = os.getenv('INSTALL_DIR', dirpath)
        self.VENV_PATH = os.getenv('VENV_PATH', self.INSTALL_DIR)
        self.configure()

    @property
    def is_venv(self):
        """Verifica se o script está sendo executado em um ambiente virtual e retorna o diretório de bibliotecas globais.
     Se estiver em um ambiente virtual, retorna o diretório de bibliotecas do ambiente virtual. Caso contrário, retorna
     o diretório de bibliotecas globais do Python global."""
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            # Retorna o diretório de bibliotecas do ambiente virtual
            return os.path.join(os.path.dirname(os.path.abspath(sys.executable)), 'Lib',
                                'site-packages') if os.name == 'nt' else os.path.join \
                (os.path.dirname(os.path.abspath(sys.executable)), 'lib',
                 'python{0.major}.{0.minor}'.format(sys.version_info), 'site-packages')
        else:
            # Retorna o diretório de bibliotecas globais do Python global
            return os.path.join(os.path.dirname(os.path.abspath(sys.executable)), 'Lib',
                                'site-packages') if os.name == 'nt' else os.path.join \
                (os.path.dirname(os.path.abspath(sys.executable)), 'lib',
                 'python{0.major}.{0.minor}'.format(sys.version_info), 'site-packages')

    def configure(self):
        """Configura as variáveis de ambiente com base no sistema operacional."""
        if not self.FFMPEG_URL or not self.FFMPEG_BINARY:
            platform_name = system
            if platform_name == 'Windows':
                self.FFMPEG_URL = URL_PLATAFOMR
                self.FFMPEG_BINARY = 'ffmpeg.exe'
            elif platform_name == 'Linux':
                self.FFMPEG_URL = URL_PLATAFOMR
                self.FFMPEG_BINARY = 'ffmpeg'
            else:
                raise DeprecationWarning(f"Arquitetura '{platform_name}' ainda não suportada...\n\n"
                                         f"Versão atual da lib: {self.VERSION}")
            os.environ['FFMPEG_URL'] = self.FFMPEG_URL
            os.environ['FFMPEG_BINARY'] = self.FFMPEG_BINARY

        if not os.getenv('INSTALL_DIR'):
            os.environ['INSTALL_DIR'] = self.INSTALL_DIR

    @property
    def __read_version(self):
        """Lê a versão do arquivo __version__.py."""
        version_file = os.path.join(os.path.dirname(os.path.abspath(__file__)).split('.')[0], '__version__.py')
        if os.path.isfile(version_file):
            with open(version_file, 'r') as file:
                version_line = file.readline().strip()
                if version_line.startswith('__version__'):
                    return version_line.split('=')[1].strip().strip("'")
        return 'Unknown Version'

    def __download_file(self, url: str, local_filename: str):
        """Baixa um arquivo do URL para o caminho local especificado."""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            total_length = int(response.headers.get('content-length', 0))

            with open(local_filename, 'wb') as f:
                start_time = time.time()
                downloaded = 0

                for data in response.iter_content(chunk_size=4096):
                    downloaded += len(data)
                    f.write(data)

                    elapsed_time = time.time() - start_time
                    elapsed_time = max(elapsed_time, 0.001)
                    speed_kbps = (downloaded / 1024) / elapsed_time
                    percent_done = (downloaded / total_length) * 100

                    sys.stdout.write(
                        f"\rBaixando Binários do ffmpeg: {percent_done:.2f}% | Velocidade: {speed_kbps:.2f} KB/s | "
                        f"Tempo decorrido: {int(elapsed_time)}s")
                    sys.stdout.flush()
                sys.stdout.write("\nDownload completo.\n")
                sys.stdout.flush()

        except requests.RequestException as e:
            raise Exception(f"Erro durante o download: {e}")

    def __extract_zip(self, zip_path: str, extract_to: str):
        """Descompacta o arquivo ZIP no diretório especificado."""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
        except zipfile.BadZipFile as e:
            sys.stderr.write(f"Erro ao descompactar o arquivo: {e}\n")
            raise
        finally:
            os.remove(zip_path)

    def remove_file(self, file_path: str):
        """Remove o arquivo ou diretório especificado."""
        if os.path.exists(file_path):
            try:
                shutil.rmtree(file_path, onerror=self.handle_remove_readonly)
            except Exception as e:
                print(f"Erro ao remover {file_path}: {e}")
                raise

    def install_bins(self):
        """Instala o ffmpeg baixando e descompactando o binário apropriado."""
        zip_path = os.path.join(self.INSTALL_DIR, "ffmpeg.zip")
        os.makedirs(self.INSTALL_DIR, exist_ok=True)
        self.__download_file(self.FFMPEG_URL, zip_path)
        self.__extract_zip(zip_path, self.INSTALL_DIR)
        self.remove_file(zip_path)
        bina = os.path.join(self.INSTALL_DIR, self.FFMPEG_BINARY)
        os.environ["PATH"] += os.pathsep + self.INSTALL_DIR
        return

    def handle_remove_readonly(self, func, path, exc_info):
        """Callback para lidar com arquivos somente leitura."""
        os.chmod(path, stat.S_IWRITE)
        func(path)


if __name__ == "__main__":
    FFmpegExceptions("erro de runtime...")
