import platform
import os

URL_PLATAFOMR = ''


def get_processor_info():
    system = platform.system()
    architecture = platform.architecture()[0]
    processor = ''
    if system == "Windows":
        processor = platform.processor()
    elif system in ["Linux", "Darwin"]:  # Darwin é o nome do sistema para macOS
        try:
            if system == "Linux":
                # Obtém informações detalhadas do processador no Linux
                with open("/proc/cpuinfo") as f:
                    cpuinfo = f.read()
                    if "model name" in cpuinfo:
                        processor = cpuinfo.split("model name")[1].split(":")[1].split("\n")[0].strip()
                    else:
                        processor = "Unknown"
            elif system == "Darwin":
                # Obtém informações detalhadas do processador no macOS
                processor = os.popen("sysctl -n machdep.cpu.brand_string").read().strip()
        except FileNotFoundError:
            processor = "Unknown"
    d = (f"System: {system} "
         f"Architecture: {architecture} "
         f"Processor: {processor} ")
    return d


# Processa a informação do processador e limpa a string
data = (get_processor_info().replace('Architecture:', '').replace('System:', '').
        replace('Processor:', '').strip().split())

# Remove entradas vazias e limpa espaços em branco
cleaned_data = [item.strip() for item in data if item.strip()]

# Garantindo que há pelo menos três elementos
if len(cleaned_data) >= 2:
    system = cleaned_data[0]
    architecture = cleaned_data[1]
    processor = ' '.join(cleaned_data[2:])  # Junta o restante como o processador

    URL_BASE_REPO = "https://raw.githubusercontent.com/PauloCesar-dev404/binarios/main/"
    # Mapeamento para Linux
    linux_mapping = {
        "x86_64": "amd64",
        "i686": "i686",
        "arm64": "arm64",
        "armhf": "armhf",
        "armel": "armel"
    }
    # Formata a URL com base no sistema e arquitetura
    if system == "Linux" and ('intel' in processor.lower() or 'amd' in processor.lower()):
        url = f"{URL_BASE_REPO}linux/ffmpeg-7.0.2-{linux_mapping.get('x86_64')}.zip"
    elif system == "Linux" and 'i686' in architecture.lower():
        url = f"{URL_BASE_REPO}linux/ffmpeg-7.0.2-{linux_mapping.get('i686')}.zip"
    elif system == "Linux" and 'arm64' in architecture.lower():
        url = f"{URL_BASE_REPO}linux/ffmpeg-7.0.2-{linux_mapping.get('arm64')}.zip"
    elif system == "Linux" and 'armhf' in architecture.lower():
        url = f"{URL_BASE_REPO}linux/ffmpeg-7.0.2-{linux_mapping.get('armhf')}.zip"
    elif system == "Linux" and 'armel' in architecture.lower():
        url = f"{URL_BASE_REPO}linux/ffmpeg-7.0.2-{linux_mapping.get('armel')}.zip"
    elif system == "Windows" and architecture == '64bit':
        url = f"{URL_BASE_REPO}windows/win-ffmpeg-7.0.2-full-amd64-intel64.zip"
    else:
        url = f"Unsupported system or architecture"

    URL_PLATAFOMR = url

else:
    raise DeprecationWarning("Não foi possível obter seu sistema ....consulte o desenvolvedor!")

if __name__ == '__main__':
    raise RuntimeError("este é uma função interna!")
