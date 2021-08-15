import requests


class Client:
    def __init__(self):
        self.serverUrl = "http://127.0.0.1:5000"

    def Run(self):
        while True:
            print("-------------------------------------------------------------------------")
            print("Funçoes disponiveis:")
            print("- Para adicionar um novo empregado digite: ADD_EMPLOYEE")
            print("- Para atualizar os dados de um empregado digite: UPDATE")
            print("- Para remover um empregado digite: RMV_EMPLOYEE")
            print("- Para ler um cartão de pontos digite: TCARD")
            print("- Para adicionar uma venda digite: SELL")
            print("- Para desfazer qualquer ação digite: UNDO")
            print("- Para sair do programa digite: END")
            print("-------------------------------------------------------------------------")
            comando = input("Digite um comando ")
            print("-------------------------------------------------------------------------")

            if comando == "END":
                break

            if comando == "ADD_EMPLOYEE":
                self.ADD_EMPLOYEE()

    def ADD_EMPLOYEE(self):
        url = self.serverUrl + "/ADD_EMPLOYEE"

        print("Criando um novo empregado...")
        print("Digite as informações do empregado:")
        data = {
            "nome": input("Nome:"),
            "endereco": input("Endereco: "),
            "tipo": input("Escolha o tipo entre, Assalariado, Comissionado e Horista: "),
            "salario": float(input("Salario: ")),
            "comissao": float(input("Comissao: ")),
            "salarioHora": float(input("Salario Hora: ")),
            "sindicato": input("Pertence a um sindicato SIM/NAO: "),
            "taxa": float(input("Taxa do sindicato: ")),
            "taxa_add": float(input("Taxa adicional do sindicato: ")),
            "diaMes": int(input("Dia do pagamento no mês: ")),
            "diaSem": input("Dia do pagamento na semana: "),
            "tipoSem": input("Tipo da semana PAR/IMPAR/NaN: ")
        }

        r = requests.post(url=url, json=data)

        print("")
        print("Empregado criado com sucesso!")
        print(r.text)
        print("-------------------------------------------------------------------------")


c = Client()

c.Run()