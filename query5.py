import json

caminho_arquivo_entrada = "diversevul_20230702.json"
caminho_arquivo_saida = "cinco_primeiras_tuplas.json"
numero_de_tuplas_a_ler = 5

lista_de_tuplas = []
try:
    with open(caminho_arquivo_entrada, 'r', encoding='utf-8') as f_in:
        
        for _ in range(numero_de_tuplas_a_ler):
            linha = f_in.readline()
            
            if not linha:
                break
            
            tupla = json.loads(linha)
            lista_de_tuplas.append(tupla)

    if lista_de_tuplas:
        with open(caminho_arquivo_saida, 'w', encoding='utf-8') as f_out:
            json.dump(lista_de_tuplas, f_out, indent=4, ensure_ascii=False)
        
        print(f"Sucesso! As {len(lista_de_tuplas)} primeiras tuplas foram salvas em: {caminho_arquivo_saida}")
    else:
        print("Erro: O arquivo de entrada está vazio ou não pôde ser lido.")

except FileNotFoundError:
    print(f"ERRO: Arquivo de entrada não encontrado em '{caminho_arquivo_entrada}'.")
except json.JSONDecodeError as e:
    print(f"ERRO: Uma das linhas lidas não é um JSON válido. Detalhes: {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")