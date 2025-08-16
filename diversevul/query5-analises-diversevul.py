import json
import os

def processar_e_salvar_item(item: dict, diretorio_saida: str):
    codigo_fonte = item.get("func")
    if not codigo_fonte:
        print("-> Aviso: Item nao contem codigo no campo 'func'. Pulando.")
        return

    commit_id = item.get("commit_id")
    if not commit_id:
        print("-> Aviso: Item nao contem 'commit_id' para nomear o arquivo. Pulando.")
        return

    nome_arquivo = f"diversevul-analise_{commit_id}.txt"
    caminho_completo = os.path.join(diretorio_saida, nome_arquivo)

    try:
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            f.write(codigo_fonte)
        print(f"-> Arquivo salvo com sucesso em: '{caminho_completo}'")
    except Exception as e:
        print(f"-> Erro ao salvar o arquivo '{caminho_completo}': {e}")

if __name__ == "__main__":
    pasta_base = 'diversevul'
    pasta_de_analises = 'analises' 
    nome_arquivo_json = 'tupla-diversevul.json'

    caminho_json_entrada = os.path.join(pasta_base, nome_arquivo_json)
    diretorio_saida_final = os.path.join(pasta_base, pasta_de_analises)

    try:
        os.makedirs(diretorio_saida_final, exist_ok=True)
        print(f"Pasta de saida '{diretorio_saida_final}' pronta.")
    except OSError as e:
        print(f"Erro ao verificar/criar a pasta '{diretorio_saida_final}': {e}")
        exit()

    try:
        with open(caminho_json_entrada, 'r', encoding='utf-8') as f:
            lista_de_itens = json.load(f)
        
        total_itens = len(lista_de_itens)
        print(f"Arquivo '{caminho_json_entrada}' carregado. Encontrados {total_itens} itens para processar.")
        
        for i, item in enumerate(lista_de_itens):
            print(f"\n--- Processando item {i+1}/{total_itens} ---")
            print(f"Commit ID: {item.get('commit_id', 'N/A')}")
            processar_e_salvar_item(item, diretorio_saida_final)

        print("\nAnalise concluida!")

    except FileNotFoundError:
        print(f"ERRO: O arquivo '{caminho_json_entrada}' nao foi encontrado. Verifique o nome e o local do arquivo.")
    except json.JSONDecodeError:
        print(f"ERRO: O arquivo '{caminho_json_entrada}' nao contem um JSON valido.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")