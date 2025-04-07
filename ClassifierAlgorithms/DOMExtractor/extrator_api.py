import requests
import os
import re

# URL base da API CKAN
BASE_URL = "https://dados.ciga.sc.gov.br/api/3/action/package_search"

# Tags confirmadas a serem processadas
TAGS = [
    "DOMSC",
    "Publicações - DOMSC",
    "Edições Ordinárias - DOMSC"
]

# Pasta de downloads
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Função para limpar nomes de arquivos e pastas
def sanitize_filename(name):
    return re.sub(r'[\\/*?"<>|:]', "_", name)

# Função para verificar arquivos já existentes
def get_existing_files(directory):
    if os.path.exists(directory):
        return set(os.listdir(directory))
    return set()

# Função para baixar os datasets com verificação de arquivos existentes
def download_datasets(tag):
    print(f"Processando tag: {tag}")
    page = 1
    page_size = 5  # Número de resultados por página

    while True:
        print(f"Solicitando página {page} para a tag '{tag}'...")
        try:
            # Fazendo a solicitação paginada
            params = {
                "q": f"tags:\"{tag}\"",  # Usa o formato literal da tag
                "start": (page - 1) * page_size,
                "rows": page_size
            }
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            # Verifica se a resposta foi bem-sucedida
            if not data.get("success"):
                print(f"Erro ao processar a tag {tag}: {data.get('error')}")
                return

            # Processa os resultados
            results = data.get("result", {}).get("results", [])
            if not results:
                print(f"Sem mais resultados para '{tag}'.")
                break

            print(f"Total de datasets na página {page}: {len(results)}")

            for dataset in results:
                title = sanitize_filename(dataset.get("title", "sem_nome"))
                resources = dataset.get("resources", [])
                print(f"\nVerificando dataset: {title}")

                # Criar uma pasta para o dataset
                dataset_dir = os.path.join(DOWNLOAD_DIR, title)
                if not os.path.exists(dataset_dir):
                    os.makedirs(dataset_dir)

                # Obter arquivos já existentes
                existing_files = get_existing_files(dataset_dir)

                # Baixar cada recurso associado
                for resource in resources:
                    resource_url = resource.get("url")
                    resource_name = sanitize_filename(resource.get("name", "arquivo"))

                    # Adicionar extensão .zip caso necessário
                    if not os.path.splitext(resource_name)[1]:
                        resource_name += ".zip"

                    if resource_name in existing_files:
                        print(f"Arquivo já existe, pulando: {resource_name}")
                        continue

                    file_path = os.path.join(dataset_dir, resource_name)
                    print(f"Baixando: {resource_name} - {resource_url}")

                    try:
                        with requests.get(resource_url, stream=True) as r:
                            r.raise_for_status()
                            with open(file_path, 'wb') as f:
                                for chunk in r.iter_content(chunk_size=8192):
                                    f.write(chunk)
                        print(f"Arquivo salvo em: {file_path}")
                    except Exception as e:
                        print(f"Erro ao baixar o recurso: {e}")

            # Próxima página
            page += 1

        except requests.exceptions.RequestException as e:
            print(f"Erro ao processar a tag {tag}: {e}")
            break

# Executa o script
if __name__ == "__main__":
    for tag in TAGS:
        download_datasets(tag)
    print(f"\nAtualização concluída. Arquivos baixados para: {DOWNLOAD_DIR}")