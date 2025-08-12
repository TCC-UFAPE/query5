import ijson
import json

caminho_arquivo_entrada = "MSR_data_cleaned.json"
caminho_arquivo_saida = "cinco_primeiras_tuplas-bigvul.json"
numero_de_tuplas_a_salvar = 5

primeiras_tuplas = []

try:
    with open(caminho_arquivo_entrada, 'rb') as f_in:
        objetos_do_json = ijson.kvitems(f_in, '')
        
        for i, (chave, valor) in enumerate(objetos_do_json):
            primeiras_tuplas.append(valor)
            
            if (i + 1) >= numero_de_tuplas_a_salvar:
                break

    if primeiras_tuplas:
        with open(caminho_arquivo_saida, 'w', encoding='utf-8') as f_out:
            json.dump(primeiras_tuplas, f_out, indent=4, ensure_ascii=False)
    else:
        print("\nNenhuma tupla foi encontrada. Verifique se o arquivo não está vazio.")
except Exception as e:
    print("Ocorreu um erro inesperado durante o processamento: {e}")