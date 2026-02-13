import os
import glob
import subprocess
from datetime import datetime
from pathlib import Path
from getpass import getpass

BASE_ENV = os.environ.copy()
EXPECTED_TEXT = "teste"          
FILES_LIST_TXT = "arquivos.txt"  
GLOB_PATTERN = "file*.enc"       # fallback: se arquivos.txt não existir, pega por padrão
SAVE_MATCHES = False             # True = salva os decifrados corretos; False = não salva nada
OUTPUT_DIR = "decifrados_ok"     # onde salvar se SAVE_MATCHES=True
OPENSSL_ENV_VAR = "OPENSSL_PASS"


def load_files() -> list[str]:
    """Carrega lista de .enc de arquivos.txt (se existir), senão usa glob file*.enc."""
    p = Path(FILES_LIST_TXT)
    if p.exists():
        files = []
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            files.append(line)
        return files
    return sorted(glob.glob(GLOB_PATTERN))


def main():
    arquivos = load_files()

    with open("palavras_relevantes01.txt", "r", encoding="utf-8") as f:
        for linha in f:
            palavra = linha.strip()
            
            if palavra:
                gerar_variacoes(palavra, 1981, arquivos, 1990, seq_max=3)

def gerar_variacoes(palavra, ano_inicio, files, ano_fim=None, seq_max=3):

    if ano_fim is None:
        ano_fim = datetime.now().year

    base = palavra.strip()
    minuscula = base.lower()
    capitalizada = base.capitalize()
    #maiuscula = base.upper()

    # variacoes_base = [minuscula, capitalizada, maiuscula]
    variacoes_base = [minuscula, capitalizada]

    for v in variacoes_base:
        print(v)
        decifra(v, files)

    for i in range(1, seq_max + 1):
        seq = "".join(str(n) for n in range(1, i + 1))
        for v in variacoes_base:
            resultado = v + seq
            print(resultado)
            decifra(resultado, files)
            resultado = seq + v
            print(resultado)
            decifra(resultado, files)

    for ano in range(ano_inicio, ano_fim + 1):
        for v in variacoes_base:
            resultado =  v + str(ano)
            print(resultado)
            decifra(resultado, files)
            resultado =  str(ano) + v
            print(resultado)
            decifra(resultado, files)
    

def decifra(password: str, files):
    #Apenas para fins didaticos, função omitida
    return
if __name__ == "__main__":
    main()
