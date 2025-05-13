''' Extrator de textos de arquivo JSON para montagem do dataset '''

# Dataset atual possui 246 samples, onde 96 não são licitações (classe 0), e 150 são licitações

# Estou usando inicialmente o arquivo samples_100.json para tentar equilibrar as samples de classe 0 e classe 1,
# e verificar funcionalidade do projeto antes de executar com mais samples.

import json
import re
import html

json_path = "./data/samples_100.json"
txt_path = "./data/textos_licitacoes.txt"

dataset_path = "./dataset/dataset_licitacoes.txt"

class0 = 0
class1 = 0

def init():
    title("INICIALIZANDO EXTRATOR")

def end():
    print("\nFinalizando execução...\n")

def title(text):
    l = len(text) + 2 * 3
    print("\n" + "*" * l)
    print(" " * 3 + text)
    print("*" * l + "\n")

def print_class_qty():
    print("\nExibindo quantidades de classes gravadas no dataset...")
    print("Classe 0: " + str(class0))
    print("Classe 1: " + str(class1) + "\n")

def open_json(path):
    print("Abrindo json...")
    while(True):
        print("\nDeseja continuar? Digite S caso queira continuar, ou n caso contrario: ", end="")
        ans = input()
        if ans == "S":
            with open(path, "r", encoding="utf-8") as file:
                process_json(json.load(file))
                return
        elif ans == "n":
            print("\nOperação cancelada")
            print("Finalizando método...\n")
            return
        else:
            print("\nEntrada inválida. Tente novamente")

def process_json(json_data):
    print("Processando json...")
    for p in json_data:
        text = p["texto"]
        write_dataset(decode_html(text))
    print("Processamento finalizado\n")
    print_class_qty()

def open_txt(path):
    print("Abrindo txt...")
    while(True):
        print("\nDeseja continuar? Digite S caso queira continuar, ou n caso contrario: ", end="")
        ans = input()
        if ans == "S":
            with open(path, "r", encoding="utf-8") as file:
                process_txt(file)
                return
        elif ans == "n":
            print("\nOperação cancelada")
            print("Finalizando método...\n")
            return
        else:
            print("\nEntrada inválida. Tente novamente")

# Como json so possui publicacoes que sao licitacoes, foi preciso adicionar ao dataset samples de publicacoes que nao sao licitacoes.
# Solucao temporaria para obter publicacoes que nao sao licitacoes. Provavelmente sera alterado
def process_txt(file, wanted_class = "0"):
    linha = file.readline()
    while(linha != ""):
        if linha == "0\n" and wanted_class == "0":
            linha = file.readline()                               # linha recebe texto
            write_dataset(linha.rstrip("\n"), classification="0") # linha é gravada no dataset
            linha = file.readline()                               # linha recebe "---"
            linha = file.readline()                               # linha recebe classificação do próximo sample ou string vazia caso EOF
        elif linha == "1\n" and wanted_class == "1":
            linha = file.readline()           # linha recebe texto
            write_dataset(linha.rstrip("\n")) # linha é gravada no dataset
            linha = file.readline()           # linha recebe "---"
            linha = file.readline()           # linha recebe classificação do próximo sample ou string vazia caso EOF
        else:
            for _ in range(3):
                linha = file.readline()
    print_class_qty()

def write_dataset(text, classification = "1"):
    global dataset_path, class0, class1
    with open(dataset_path, "a", encoding="utf-8") as file:
        file.write(classification + "\n" + text + "\n---\n")
        if classification == "1":
            class1 += 1
        elif classification == "0":
            class0 += 1

# Normaliza texto com marcas de html. Parâmetro: string a ser normalizada. Retorna: texto pronto para escrita
def decode_html(text):
    
    #Remove tags html
    text = re.sub(r'<[^>]+>', '', text)
    
    #Recodifica caracteres especiais 
    text = html.unescape(text)
    
    #Remove emojis e caracteres invalidos
    text = re.sub(r'[\U00010000-\U0010FFFF\u200B-\u200D\uFEFF]', '', text)
    text = text.replace("�", "")
        
    #Remove espacos e quebras de linha desnecessarias
    final_text = " ".join(text.split())
    
    return final_text

def main():
    init()
    open_json(json_path)
    open_txt(txt_path)
    end()

if __name__ == "__main__":
    main()
