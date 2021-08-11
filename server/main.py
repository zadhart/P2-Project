from flask import request
from create_app import db, app
from Change import Change
from Empregado import Empregado
from Pagamentos import Pagamentos
from Pontos import Pontos
from Vendas import Vendas
from Sindicato import Sindicato

last_changes = []


# Creating the Routes
@app.route("/ADD_EMPLOYEE", methods=["GET", "POST"])
def add_employee():
    content = request.get_json()

    new_employee = Empregado(
        endereco=content["endereco"],
        nome=content["nome"]
    )

    db.session.add(new_employee)

    last_changes.append(Change(prev_data=None,
                                         new_data=new_employee,
                                         change_function="add_employee",
                                         undo_function="rmv_employee"))

    newSind = Sindicato(
        id=new_employee.id,
        membro= content["sindicato"],
        taxa=content["taxa"],
        taxa_add=content["taxa_add"]
    )

    db.session.add(newSind)

    # Estabelecendo o tipo de pagamento do funcionario
    tipoPagam = Pagamentos(
        id=new_employee.id,
        tipo=content["tipo"],
        diaMes=content["diaMes"],
        diaSem=content["diaSem"],
        tipoSem=content["tipoSem"],
        salario=content["salario"],
        comissao=content["comissao"],
        salarioHora=content["salarioHora"]
    )
    db.session.add(tipoPagam)

    db.session.commit()

    print("Created new employee: " + str(new_employee.id))
    return str(new_employee.id)


@app.route("/RMV_EMPLOYEE", methods=["GET", "POST"])
def rmv_employee():
    content = request.get_json()

    obj = db.session.query(Empregado).filter(Empregado.id == content["id"]).first()

    last_changes.append(Change(prev_data=obj,
                               new_data=None,
                               change_function="rmv_employee",
                               undo_function="add_employee"))

    db.session.delete(obj)
    db.session.commit()

    return "Employee removed"


@app.route("/SELL", methods=["GET", "POST"])
def sell():
    content = request.get_json()

    sell = Vendas(
        id=content["id"],
        valor=content["valor"],
        mes=content["mes"],
        semana=content["semana"],
        dia=content["dia"]
    )

    db.session.add(sell)

    last_changes.append(Change(prev_data=sell,
                               new_data=None,
                               change_function="sell",
                               undo_function="cancel_sell"))

    db.session.commit()

    print("Created sale")

    return "Created sale"


@app.route("/TCARD", methods=["GET", "POST"])
def read_tcard():
    content = request.get_json()

    card = Pontos(
        id=content["id"],
        horasTrabalhadas=content["horasTrabalhadas"],
        mes=content["mes"],
        semana=content["semana"]
    )

    db.session.add(card)

    last_changes.append(Change(prev_data=card,
                               new_data=None,
                               change_function="read_tcard",
                               undo_function="unread_tcard"))

    db.session.commit()

    print("Added TCARD")
    return "Added TCARD"


@app.route("/UPDATE", methods=["GET", "POST"])
def update():
    content = request.get_json()

    funcionario = db.session.query(Empregado).filter(Empregado.id == content["id"]).first()

    old_one = funcionario

    funcionario.endereco = content["endereco"]

    funcPagamento = db.session.query(Pagamentos).filter(Pagamentos.id == content["id"]).first()

    funcPagamento.tipo = content["tipo"]
    funcPagamento.diaMes = content["diaMes"]
    funcPagamento.diaSem = content["diaSem"]
    funcPagamento.tipoSem = content["tipoSem"]
    funcPagamento.salario = content["salario"]
    funcPagamento.salarioHora = content["salarioHora"]
    funcPagamento.comissao = content["comissao"]

    funcSindicato = db.session.query(Sindicato).filter(Sindicato.id == content["id"]).first()

    funcSindicato.taxa = content["taxa"]
    funcSindicato.taxa_add = content["taxa_add"]
    funcSindicato.membro = content["sindicato"]

    last_changes.append(Change(prev_data=old_one,
                               new_data=funcionario,
                               change_function="update",
                               undo_function="undo_update"))

    db.session.commit()

    print("updated")
    return "Updated"

@app.route("/UNDO", methods=["GET", "POST"])
def CtrlZ():
    content = request.get_json()
    c = last_changes.pop(0)
    c.undo()

    return "ctrlZ"

@app.route("/RUN", methods=["GET", "POST"])
def Run():
    result = 0
    content = request.get_json()

    # Encontrando todos os empregados assalariados que recebem mensalmente
    assalariados = db.session.query(Pagamentos).filter(Pagamentos.tipo == "Assalariado",
                                                Pagamentos.comissao == 0,
                                                Pagamentos.salarioHora == 0,
                                                Pagamentos.diaMes == content["diaMes"],
                                                Pagamentos.tipoSem == "NaN",
                                                Pagamentos.diaSem == "NaN").all()


    for i in assalariados:
        result += i.salario

    # Encontrando todos os empregados assalariados que recebem semanalmente
    assalariados = db.session.query(Pagamentos).filter(Pagamentos.tipo == "Assalariado",
                                                       Pagamentos.comissao == 0,
                                                       Pagamentos.salarioHora > 0,
                                                       Pagamentos.diaSem == content["diaSem"],
                                                       Pagamentos.tipoSem == content["tipoSem"],
                                                       Pagamentos.diaMes == 0).all()


    for i in assalariados:
        result += i.salario

    # Encontrando todos os empregados horistas que recebem mensalmente
    horistas = db.session.query(Pagamentos).filter(Pagamentos.tipo == "Horista",
                                                       Pagamentos.comissao == 0,
                                                       Pagamentos.salarioHora != 0,
                                                       Pagamentos.diaMes == content["diaMes"],
                                                       Pagamentos.tipoSem == "NaN",
                                                       Pagamentos.diaSem == "NaN").all()
    #print("Horista: ", end="")
    #print(horistas)

    for i in horistas:
        # print("id: ", end="")
        # print(i.id)
        horas = db.session.query(Pontos).filter(Pontos.id == str(i.id),
                                                Pontos.mes == content["mes"],
                                                Pontos.semana == content["semana"]).all()
        # print(horas)
        horas_trab = 0

        for h in horas:
            horas_trab += h.horasTrabalhadas

        # print(i.salarioHora * horas_trab)

        horas_bonus = 0

        if horas_trab > 160:
            horas_bonus = horas_trab - 160
            horas_trab = horas_trab - 160

        result += i.salarioHora * horas_trab
        result += i.salarioHora * horas_bonus * 1.5

    # Encontrando todos os empregados horistas que recebem mensalmente
    horistas = db.session.query(Pagamentos).filter(Pagamentos.tipo == "Horista",
                                                   Pagamentos.comissao == 0,
                                                   Pagamentos.salarioHora != 0,
                                                   Pagamentos.diaMes == 0,
                                                   Pagamentos.tipoSem == content["tipoSem"],
                                                   Pagamentos.diaSem == content["diaSem"]).all()

    for i in horistas:
        # print("id: ", end="")
        # print(i.id)
        horas = db.session.query(Pontos).filter(Pontos.id == str(i.id), Pontos.mes == content["mes"]).all()
        # print(horas)
        horas_trab = 0

        for h in horas:
            horas_trab += h.horasTrabalhadas

        # print(i.salarioHora * horas_trab)

        horas_bonus = 0

        if horas_trab > 160:
            horas_bonus = horas_trab - 160
            horas_trab = horas_trab - 160

        result += i.salarioHora * horas_trab
        result += i.salarioHora * horas_bonus * 1.5

    # Encontrando todos os empregados comissionados que recebem mensalmente
    comissionados = db.session.query(Pagamentos).filter(Pagamentos.tipo == "Comissionado",
                                                   Pagamentos.comissao != 0,
                                                   Pagamentos.salarioHora == 0,
                                                   Pagamentos.diaMes == content["diaMes"],
                                                   Pagamentos.tipoSem == "NaN",
                                                   Pagamentos.diaSem == "NaN").all()

    for i in comissionados:

        vendas = db.session.query(Vendas).filter(Vendas.id == str(i.id), Vendas.mes == content["mes"]).all()

        for v in vendas:

            result += v.valor * i.comissao

    # Encontrando todos os empregados comissionados que recebem mensalmente
    comissionados = db.session.query(Pagamentos).filter(Pagamentos.tipo == "Comissionado",
                                                        Pagamentos.comissao != 0,
                                                        Pagamentos.salarioHora == 0,
                                                        Pagamentos.diaMes == 0,
                                                        Pagamentos.tipoSem == content["tipoSem"],
                                                        Pagamentos.diaSem == content["diaSem"]).all()

    for i in comissionados:
        # print("id: ", end="")
        # print(i.id)
        vendas = db.session.query(Vendas).filter(Vendas.id == str(i.id),
                                                 Vendas.mes == content["mes"],
                                                 Vendas.semana == content["semana"]).all()

        for v in vendas:

            result += v.valor * i.comissao

    return str(result)

if __name__ == '__main__':
    app.run()
