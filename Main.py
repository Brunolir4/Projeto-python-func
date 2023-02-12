import requests, json, time



def GetStr(string, delimiter1, delimiter2, index):
    result = []
    try:
        result = string.split(delimiter1)
        result = result[index].split(delimiter2)
    except:
        result[0] = "NULL"
    return result[0]

def validate_string(string):
    if(string is None):
        string = "N/A"
    else:
        string = string
        
        
def validate_cpf(cpf):
    # validar quantidade de caracteres digitados
    if len(cpf) > 14 or len(cpf) < 11 or len(cpf) > 11:
        return(0)

    # verificar se todos os dígitos são iguais
    else:
        valid = 0
        for dig in range(0, 11):
            valid += int(cpf[dig])
            dig += 1
        if int(cpf[0]) == valid / 11:
            return(0)

        # rotina de cálculos do dígito verificador do CPF
        else:
            # verificação do 10º dígito verificador
            soma = 0
            count = 10
            for i in range(0, len(cpf)-2):
                soma = soma + (int(cpf[i])*count)
                i+=1
                count-=1
            dg1 = 11-(soma%11)
            if dg1 >= 10:
                dg1 = 0

            # verificação do 11º dígito verificador
            soma = 0
            count = 10
            for j in range(1, len(cpf)-1):
                soma = soma + (int(cpf[j])*count)
                j+=1
                count-=1
            dg2 = 11-(soma%11)
            if dg2 >= 10:
                dg2 = 0

            # mensagem ao usuário
            if int(cpf[9]) != dg1 or int(cpf[10]) != dg2:
                return("0")
            else:
                return("1")

headers = {
    'authority': 'storage.googleapis.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

i = 0
while(True):
    try:
        response = requests.get('https://storage.googleapis.com/raccoon-humane/psel.json', headers=headers)
        break
    except:
        i += 1
        print("Connection Trouble, retrying request instance -> ["+str(i)+"], sleeping -> ["+str(i*i)+"]")
        time.sleep(i*i)
        

if(response.status_code == 200):    
    if("nome" in response.text):
        rows = response.text.count("nome")+1
        
        nomes = []
        cpfs = []
        cargos = []
        salarios = []
        adicional_insalubridades = []
        cpfs_invalido = []
        
        i = 1
        while(i != rows):
            nome = GetStr(response.text, 'nome": "', '"', i)
            cpf = GetStr(response.text, 'cpf": "', '"', i)
            cargo = GetStr(response.text, 'cargo": "', '"', i)
            salario = GetStr(response.text, 'salario": ', '\n', i).replace("\r", "")
            
            if(validate_cpf(cpf.replace(".", "").replace("-", ""))) == "0":
                cpf_invalido = True
            else:
                cpf_invalido = False
                
            
            if(cargo == "Assassin"):
                adicional_insalubridade = float(salario) * 0.05
            elif(cargo == "Batman"):
                adicional_insalubridade = float(salario) * 0.10
            elif(cargo == "Butler"):
                adicional_insalubridade = 0
            elif(cargo == "Side Kick"):
                adicional_insalubridade = float(salario) * 0.15
            elif(cargo == "The Chief Demon"):
                adicional_insalubridade = float(salario) * 0.125
                
                
            nomes.append(nome.encode('utf-8').decode('utf-8'))
            cpfs.append(cpf)
            cargos.append(cargo)
            salarios.append(salario)
            adicional_insalubridades.append(adicional_insalubridade)
            cpfs_invalido.append(cpf_invalido)
            
            
            i += 1
            
        

    
    data = []
    i = 0
    while i != rows-1:
        data = data+[{'nome': nomes[i], 'cpf': cpfs[i], 'cargo': cargos[i], 'salario': salarios[i], 'cpf_valido': cpfs_invalido[i], 'adicional_insalubridade': adicional_insalubridades[i]}]
        i += 1

    json_data = json.dumps(data)

    print(json_data)
    
    f = open("FORMATADO.json", 'w')
    f.write(json_data)
    f.close()