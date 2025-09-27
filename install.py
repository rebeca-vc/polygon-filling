import os
import subprocess
import venv

def main():
    # Nome do ambiente virtual 
    venv_dir = "venv"

    # Cria o ambiente virtual se não existir
    if not os.path.exists(venv_dir):
        print("Criando ambiente virtual...")
        venv.EnvBuilder(with_pip=True).create(venv_dir)
    else:
        print("Ambiente virtual já existe.")

    # Caminho do pip dentro do venv 
    pip_executable = os.path.join(venv_dir, "bin", "pip")
    python_executable = os.path.join(venv_dir, "bin", "python")

    # Se o pip não existir, tenta instalar com ensurepip
    if not os.path.exists(pip_executable):
        print("pip não encontrado dentro do venv. Tentando instalar...")
        subprocess.check_call([python_executable, "-m", "ensurepip", "--upgrade"])
        subprocess.check_call([python_executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

    print("Atualizando pip, setuptools e wheel...")
    subprocess.check_call([python_executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

    # Instala dependências do requirements.txt
    if os.path.exists("requirements.txt"):
        print("Instalando dependências...")
        subprocess.check_call([pip_executable, "install", "-r", "requirements.txt"])
    else:
        print("Nenhum requirements.txt encontrado.")

    package_name = "freeglut3-dev"
    command = ["sudo", "apt-get", "install", "-y", package_name]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Pacote {package_name} instalado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar o pacote {package_name}: {e.stderr}")
    
    print("Definindo varíaveis ambiente")
    os.environ['MUJOCO_GL'] = 'glx'
    os.environ['PYOPENGL_PLATFORM'] = 'glx' 
    os.putenv("MUJOCO_GL", "glx")
    os.putenv("PYOPENGL_PLATFORM", "glx")

    print("Ambiente pronto! Para rodar o programa use:")
    print(f"   source {venv_dir}/bin/activate && python src/main.py")

if __name__ == "__main__":
    main()