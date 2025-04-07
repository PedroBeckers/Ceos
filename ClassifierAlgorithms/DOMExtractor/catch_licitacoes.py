import os
import zipfile
import json
import unicodedata
import re
import html

from TF_IDF.tf_idf import tokenize

# "concorrência, concurso, leilão, pregão e diálogo competitivo."

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
                    #print(tokenize(publicacao.get('titulo'))) #titulo nao contem palavras citadas pela prof
                    #classification = classify_by_title()      #esperando novo metodo para classificar entre lic e nao lic
                    text_to_file(final_text, "textos_licitacoes.txt")
                    text_to_file(title, "titulos_licitacoes.txt")
                else:
                    print("Texto ausente")
            else:
                print(f"Publicação ignorada: Categoria '{categoria_normalizada}'.")
        
        print(f"\nO arquivo JSON '{json_name}' possui {qty} publicações de categoria licitação.")
        diff = qty - text_qty
        print(f"Publicações que possuiam texto: {text_qty}")
        print(f"Publicações que não possuiam texto: {diff}")

# Funcao para gravar texto da licitacao em um arquivo txt 
def text_to_file(text, path):
    with open(path, "a", encoding="utf-8") as arc:
        #arc.write(classification)
        arc.write(text + "\n---\n")

'''
def classify_by_title(tokens):
   if 
        
        
        
        
'''

# Função principal para processar os arquivos ZIP
def process_zip_files():
    
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
                    
                    traverse_json_files(extract_path)
                                
            else:
                traverse_json_files(os.path.splitext(processing_path)[0])
                    
# Iterar sobre todos json, tanto os extraidos de um zip, quanto os que nao foram extraidos             
def traverse_json_files(path):
    
    item_qty = len(os.listdir(path))
    print(f"{item_qty} arquivos JSON encontrado(s).\n")
    
    for root, _, files in os.walk(path):
        for file in files:
            
            if file.endswith(".json"):
                process_json_file(os.path.join(root, file))
                
                                
if __name__ == "__main__":
    process_zip_files()
    print("\nProcessamento concluído.")
    
    
    
    
    
    
    
    
    