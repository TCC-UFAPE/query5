import json
import re
import os

def salvar_codigo_em_arquivo(item_vul: dict, conteudo: str, diretorio: str):
    cwe_id = item_vul.get("CWE ID", "CWE_desconhecido")
    commit_id = item_vul.get("commit_id", "commit_desconhecido")
    
    cwe_id_seguro = cwe_id.replace('/', '_').replace('\\', '_')
    commit_id_seguro = commit_id.replace('/', '_').replace('\\', '_')

    nome_arquivo_final = f"{cwe_id_seguro}_{commit_id_seguro}.txt"
    
    caminho_completo = os.path.join(diretorio, nome_arquivo_final)
    
    try:
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f"-> Arquivo salvo com sucesso em: '{caminho_completo}'")
    except Exception as e:
        print(f"-> Ocorreu um erro ao salvar o arquivo '{caminho_completo}': {e}")

def reconstruir_codigo_original_do_patch(patch_str: str) -> str:
    linhas_originais = []
    for linha in patch_str.splitlines():
        if linha.startswith('+'):
            continue
        elif linha.startswith('-'):
            linhas_originais.append(linha[1:])
        elif linha.startswith(' '):
            linhas_originais.append(linha[1:])
    
    return "\n".join(linhas_originais)

def processar_vulnerabilidade(item_vul: dict, diretorio_saida: str):
    summary = item_vul.get("Summary", "")
    match = re.search(r"The\s+([a-zA-Z0-9_]+)\s+function", summary)

    if not match:
        print("Nao foi possivel determinar o nome da funcao vulneravel a partir do resumo.")
        return

    vulnerable_function_name = match.group(1)
    print(f"Buscando pela funcao: '{vulnerable_function_name}'")

    codigo_para_salvar = None
    
    func_before = item_vul.get("func_before", "")
    if f" {vulnerable_function_name}(" in func_before:
        print("Codigo-fonte completo encontrado no campo 'func_before'.")
        codigo_para_salvar = func_before
    else:
        patch_data = item_vul.get("patch", "")
        if patch_data:
            print("Codigo-fonte completo nao encontrado. Reconstruindo a partir do patch.")
            codigo_para_salvar = reconstruir_codigo_original_do_patch(patch_data)
        else:
            print("Nenhum codigo ou patch encontrado para este item.")

    if codigo_para_salvar:
        salvar_codigo_em_arquivo(item_vul, codigo_para_salvar, diretorio_saida)

if __name__ == "__main__":
    pasta_base = 'bigvul'
    pasta_de_analises = 'analises'
    nome_arquivo_json = 'tupla-bigvul.json'

    caminho_json_entrada = os.path.join(pasta_base, nome_arquivo_json)
    diretorio_saida_final = os.path.join(pasta_base, pasta_de_analises)

    try:
        os.makedirs(diretorio_saida_final, exist_ok=True)
        print(f"Pasta de saida '{diretorio_saida_final}' pronta.")
    except OSError as e:
        print(f"Erro ao criar a pasta '{diretorio_saida_final}': {e}")
        exit()

    try:
        with open(caminho_json_entrada, 'r', encoding='utf-8') as f:
            lista_de_vulnerabilidades = json.load(f)
        
        total_itens = len(lista_de_vulnerabilidades)
        print(f"Arquivo JSON '{caminho_json_entrada}' carregado. Encontradas {total_itens} vulnerabilidades para processar.")
        
        for i, item in enumerate(lista_de_vulnerabilidades):
            print(f"\n--- Processando item {i+1}/{total_itens} ---")
            cve_id_item = item.get('CVE ID', 'N/A')
            print(f"CVE: {cve_id_item}")
            processar_vulnerabilidade(item, diretorio_saida_final)

        print("\nAnalise concluida!")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_json_entrada}' nao foi encontrado.")
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{caminho_json_entrada}' nao contem um JSON valido.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")