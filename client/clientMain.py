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
            comando = input("Digite um comando: ")
            print("-------------------------------------------------------------------------")

            if comando == "END":
                break

            elif comando == "ADD_EMPLOYEE":
                self.ADD_EMPLOYEE()

            elif comando == "RMV_EMPLOYEE":
                self.RMV_EMPLOYEE()

            elif comando == "SELL":
                self.SELL()

            elif comando == "TCARD":
                self.TCARD()

            elif comando == "UPDATE":
                self.UPDATE()

            elif comando == "UNDO":
                self.UNDO()

            elif comando == "RUN":
                self.RUN()

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

    def RMV_EMPLOYEE(self):

        url = self.serverUrl + "/RMV_EMPLOYEE"

        print("Apagando o empregado...")

        data = {"id": input("Digite o ID do empregado: ")}

        r = requests.post(url=url, json=data)

        print("")
        print("Empregado apagado com sucesso!")
        print(r.text)
        print("-------------------------------------------------------------------------")

    def SELL(self):
        url = self.serverUrl + "/SELL"

        print("Cadastrando uma nova venda...")

        data = {
            "id": input("Digite o ID do empregado que realizou a venda: "),
            "valor": float(input("Valor da venda: ")),
            "dia": int(input("Dia que a venda foi realizada: ")),
            "mes": int(input("Mes que a venda foi realizada: ")),
            "semana": int(input("Semana que a venda foi realizada: "))
        }

        r = requests.post(url=url, json=data)

        print("")
        print("Venda realizada com sucesso!")
        print(r.text)
        print("-------------------------------------------------------------------------")

    def TCARD(self):
        url = self.serverUrl + "/TCARD"

        print("Lendo um cartao de ponto...")

        data = {
            "id": input("Digite o ID do empregado: "),
            "horasTrabalhadas": int(input("Quantidade de horas trabalhadas: ")),
            "mes": int(input("Mes atual: ")),
            "semana": int(input("Semana atual: "))
        }

        r = requests.post(url=url, json=data)

        print("")
        print("Cartao lido com sucesso!")
        print(r.text)
        print("-------------------------------------------------------------------------")

    def UPDATE(self):
        url = self.serverUrl + "/UPDATE"

        print("Atualizando o empregado...")
        print("Digite as informações do empregado:")
        data = {
            "id": input("ID:"),
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
        print("Empregado atualizado com sucesso!")
        print(r.text)
        print("-------------------------------------------------------------------------")

    def UNDO(self):
        url = self.serverUrl + "/UNDO"

        print("Desfazendo um comando...")

        data = {"id": "1"}

        r = requests.post(url=url, json=data)

        print("")
        print("Comando desfeito com sucesso!")
        print(r.text)
        print("-------------------------------------------------------------------------")

    def RUN(self):
        url = self.serverUrl + "/RUN"

        print("Rodando a folha de pagamento...")
        print("Digite algumas informações:")

        data = {
            "diaSem": input("Dia da semana: "),
            "tipoSem": input("Tipo da semana: "),
            "diaMes": int(input("Dia mes: ")),
            "semana": int(input("Dia semana: ")),
            "mes": int(input("Mes: "))
        }

        r = requests.post(url=url, json=data)

        print("")
        print("Folha de pagamento calculada com sucesso!")
        print(r.text)
        print("-------------------------------------------------------------------------")

c = Client()

c.Run()
