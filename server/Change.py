from create_app import db

class Change():
    def __init__(self, new_data, prev_data, change_function, undo_function):
        self.prev_data = prev_data
        self.new_data = new_data
        self.change_function = change_function
        self.undo_function = undo_function

    def rmv_employee(self):
        '''content = request.get_json()

        obj = db.session.query(Empregado).filter(Empregado.id == content["id"]).first()'''
        obj = self.new_data
        db.session.delete(obj)
        db.session.commit()

        return "Employee removed"

    def add_employee(self):
        db.session.add(self.prev_data)
        db.session.commit()

    def undoUpdate(self):
        self.rmv_employee()
        self.add_employee()
        db.session.commit()

        print("updated")
        return "Updated"

    def cancelSell(self):
        '''content = request.get_json()

        obj = db.session.query(Vendas).filter(Vendas.vid == content["vid"]).first()'''
        obj = self.prev_data
        db.session.delete(obj)
        db.session.commit()

        return "Sell canceled"

    def unreadTcard(self):
        '''content = request.get_json()

        obj = db.session.query(Pontos).filter(Pontos.pid == content["pid"]).first()'''
        obj = self.prev_data
        db.session.delete(obj)
        db.session.commit()

        return "Unread Tcard"

    def undo(self):
        if self.undo_function == "rmv_employee":
            self.rmv_employee()

        elif self.undo_function == "cancel_sell":
            self.cancelSell()

        elif self.undo_function == "unread_tcard":
            self.unreadTcard()

        else:
            self.undoUpdate()