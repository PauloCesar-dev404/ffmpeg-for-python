import os.path
import re
from ffmpeg_for_python.__config__ import Configurate
from ffmpeg_for_python.__version__ import __version__, __autor__, __repo__, __source__, __lib__
from setuptools import setup, find_packages
cached = os.path.join('ffmpeg_for_python', '__pycache__')
libs_ = os.path.join('dist')
# Regex para capturar a versão do arquivo
# Regex para capturar a versão do arquivo tanto para .tar.gz quanto para .whl
version_regex = re.compile(r'ffmpeg_for_python-(\d+\.\d+\.\d+)(?:-py3-none-any)?\.(?:tar\.gz|whl)')
# Remover o cache do __pycache__ se existir
if os.path.exists(cached):
    c = Configurate()
    c.remove_file(file_path=cached)
# Remover pacotes antigos da pasta dist, se a versão for diferente da atual
if os.path.exists(libs_):
    for file_name in os.listdir(libs_):
        match = version_regex.match(file_name)
        if match:
            file_version = match.group(1)
            if file_version != __version__:
                file_path = os.path.join(libs_, file_name)
                os.remove(file_path)
                print(f'Removido {file_name} com versão {file_version}')

# Lê o conteúdo do README.md
with open('README_PYPI.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name="ffmpeg-for-python",
    version=__version__,
    description="Wrapper para o binário FFmpeg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=__autor__,
    author_email="paulocesar0073dev404@gmail.com",
    license="MIT",
    keywords=["ffmpeg"],
    requires=['requests'],
    packages=find_packages(),
    package_data={"ffmpeg_for_python.ffmpeg-bin": ["*.*"]},
    zip_safe=False,
    include_package_data=True,
    platforms=["any"],
    project_urls={
        "Código Fonte": __source__,
        "lib": __lib__,
        'GitHub': __repo__,
        "Bugs/Melhorias": f"{__repo__}/issues",
        "Documentação": f"{__repo__}/wiki",
    },

)
