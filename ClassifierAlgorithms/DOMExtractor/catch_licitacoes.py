import os
import zipfile
import json
import unicodedata
import re
import html

#python nao reconhece modulo TF_IDF -> adicionar pythonpath manualmente no terminal
#PYTHONPATH=$PYTHONPATH:/home/beckerpedro/Documentos/Ceos/ClassifierAlgorithms python3 catch_licitacoes.py
from TF_IDF.tf_idf import tokenize

# Caminho da pasta de downloads
download_path = "./downloads"

# Função para normalizar strings removendo caracteres especiais -> remove cedilha e acentos
def normalize_text(text):
    if text is None:
        return ""
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8').lower()

#remove marcas html, ajusta cedilhas e acentos. deixa a string na forma final para ser adicionada ao arq
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
    

# Função para processar cada arquivo JSON extraído
def process_json_file(file_path):
    
    json_name = os.path.splitext(os.path.basename(file_path))[0]
    print(f"Processando o arquivo JSON: {json_name}\n")
    
    with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as file:
        data = json.load(file)
        publicacoes = data.get("autopublicacoes", [])

        if publicacoes is None:
            print(f"A chave 'autopublicacoes' está vazia ou é nula no arquivo {file_path}. Ignorando.")
            return

        qty = 0
        text_qty = 0
        print("Buscando publicações de categoria licitação...")
        for publicacao in publicacoes:
            categoria_raw = publicacao.get("categoria", "")
            categoria_normalizada = normalize_text(categoria_raw)
            if "licitacoes" in categoria_normalizada:
                qty += 1
                print(f"Publicação identificada como 'licitacoes': {publicacao.get('titulo')}")
                final_text = decode_html(publicacao.get('texto'))
                title = decode_html(publicacao.get('titulo'))
                if final_text != None:
                    text_qty += 1
                    text_to_file(final_text, "textos_licitacoes.txt", classify_by_title(tokenize(title.lower())))
                    text_to_file(title, "titulos_licitacoes.txt")
                else:
                    print("Texto ausente")
            else:
                print(f"Publicação ignorada: Categoria '{categoria_normalizada}'.")
        
        print(f"\nO arquivo JSON '{json_name}' possui {qty} publicações de categoria licitação.")
        diff = qty - text_qty
        print(f"Publicações que possuiam texto: {text_qty}")
        print(f"Publicações que não possuiam texto: {diff}")
        return text_qty

# Funcao para gravar texto da licitacao em um arquivo txt, parametro classification apenas existe caso text seja o texto da publicacao
def text_to_file(text, path, classification=None):
    with open(path, "a", encoding="utf-8") as arc:
        if classification != None:
            arc.write(classification + "\n")
        arc.write(text + "\n---\n")

#recebe titulo tokenizado e retorna "1" caso seja licitacao e "0" caso contrario
def classify_by_title(tokens):
    classification_criteria = ["concorrência", "concurso", "leilão", "pregão"] # "diálogo competitivo" nao incluso pois nao tem exemplar 
    for w in tokens:
        for c in classification_criteria:
            if w == c:
                return "1"
    return "0"

# Função principal para processar os arquivos ZIP. Retorna quantidade de textos
def process_zip_files():
    
    text_sum = 0
    for directory in os.listdir(download_path):
        print(f"\nProcessando o diretório '{directory}'...")
        
        actual_path = os.path.join(download_path, directory)
        dir_qty = len(os.listdir(actual_path))
        print(f"{dir_qty} novos diretórios encontrado(s).")
        
        count = 0
        for item in os.listdir(actual_path):
            count += 1
            
            print(f"\nProcessamento número {count} de {dir_qty}. processando o item: '{item}'...")
            processing_path = os.path.join(actual_path, item)
            
            if item.endswith(".zip"):
                
                print(f"Extraindo arquivo ZIP: '{item}'")
                with zipfile.ZipFile(processing_path, 'r') as zip_ref:
                    extract_path = os.path.splitext(processing_path)[0]
                    zip_ref.extractall(extract_path)
                    
                    text_sum += traverse_json_files(extract_path)
                                
            else:
                text_sum += traverse_json_files(os.path.splitext(processing_path)[0])

            if text_sum >= 50:
                return text_sum
            
                    
# Iterar sobre todos json, tanto os extraidos de um zip, quanto os que nao foram extraidos             
def traverse_json_files(path):
    
    item_qty = len(os.listdir(path))
    print(f"{item_qty} arquivos JSON encontrado(s).\n")
    
    text_sum = 0
    for root, _, files in os.walk(path):
        for file in files:
            
            if file.endswith(".json"):
                text_sum += process_json_file(os.path.join(root, file))
    
    return text_sum
                                
#if __name__ == "__main__":
    #n = process_zip_files()
    #print(f"\nProcessamento concluído. {n} textos foram gravados.")
    #166 textos gravados, minimo maior que 80