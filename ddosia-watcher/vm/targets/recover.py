import json
from glob import glob
import sys
import sqlite3

def write_reg_sqlite(reg, db="../database.db"):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	query = """INSERT INTO regs (`host`,`host_id`,`request_id`,`schema`,`last_time_seen`) VALUES(?,?,?,?,CURRENT_TIMESTAMP) ON CONFLICT(request_id) DO UPDATE SET host = excluded.host, host_id = excluded.host_id, schema = excluded.schema, last_time_seen = CURRENT_TIMESTAMP;"""
	host = reg['host']
	host_id = reg['target_id']
	request_id = reg['request_id']
	schema = reg
	values = (host, host_id, request_id, json.dumps(schema))
	cursor.execute(query, values)
	conn.commit()
	conn.close()

def imprimir_resumen(resumen: dict, out_file:bool = False):
    print(f"\nRESUMEN\n{'-'*90}")
    tabla = "URL\t\t\t\t\t\t\t\t\tIP\n"
    for ind, (url, ips) in enumerate(resumen.items()):
        url_formatted = f"{ind}.{url}".ljust(70)
        ips_formatted = "\n\t\t\t\t\t\t\t\t\t".join(ips)
        tabla += f"{url_formatted}\t{ips_formatted}\n"
    print(tabla)
    # Optional
    if out_file:
        with open("resumen.txt",'w', encoding='utf-8') as f:
            f.write( tabla )

def recover_targets( out_file:bool = False):
    resumen = {}
    result = []
    for file in glob(r'.\dumps\*'):
        with open(file, 'rb') as archivo:
            texto = archivo.read().decode(errors='ignore')

        if '"targets"' in texto:
            print(f"Estructured data in {file}")
            try:
                texto = texto.split('"targets":[')[1]
            except:
                continue
            contador = 0
            for ind,lett in enumerate(texto):
                if lett == "[":
                    contador += 1
                elif lett == "]":
                    contador -= 1
                    if contador == -1:
                        texto = f"[{texto[:ind]}]"
                        result = result + json.loads(texto)
                        break

    try:
        for target in result:
            if 'host' in target:
                write_reg_sqlite(target)
                if target['host'] in resumen:
                    if not target['ip'] in resumen[target['host']]:
                        resumen[target['host']].append(target['ip'])
                else:
                    resumen[target['host']] = [ target['ip'] ]
        result = json.dumps(result, indent=4)
    except json.decoder.JSONDecodeError as error:
        print(f"[ERROR] Decoding JSON: {error}\n json:{result}")
        
    with open('out.json','w', encoding='utf-8') as f:
        f.write(result)
    
    imprimir_resumen(resumen, out_file)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--out', action='store_true', help="Para sacar output en ficheros")
    args = parser.parse_args()
    recover_targets( out_file=args.out )
