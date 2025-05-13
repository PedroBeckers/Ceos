''' Extrator de textos de arquivo JSON para montagem do dataset '''

import json
import re
import html

json_path = "./data/samples_150.json"
dataset_path = "./dataset/dataset_licitacoes.txt"

json_data = None

def init():
    title("INICIALIZANDO EXTRATOR")

def end():
    print("\nFinalizando execução...\n")

def title(text):
    l = len(text) + 2 * 3
    print("\n" + "*" * l)
    print(" " * 3 + text)
    print("*" * l + "\n")

def open_json(path):
    global json_data
    with open(path, "r", encoding="utf-8") as file:
        json_data = json.load(file)

def process_json():
    for p in json_data:
        text = p["texto"]
        write_dataset(decode_html(text))

def write_dataset(text, classification = "1"):
    global dataset_path
    with open(dataset_path, "a", encoding="utf-8") as file:
        file.write(classification + "\n" + text + "\n---\n")

# Normaliza texto com marcas de html. Parametro: string a ser normalizada. Retorna: texto pronto para escrita
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
    process_json()
    end()

if __name__ == "__main__":
    main()
