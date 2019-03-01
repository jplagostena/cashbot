from __future__ import print_function
import gspread
import datetime
from oauth2client import file, client
from config import config
import os

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
OOB_CALLBACK_URN = 'urn:ietf:wg:oauth:2.0:oob'


class GoogleSheeter(object):

    def __init__(self, username, creds):
        super().__init__()
        self.username = username
        self.creds = creds

    def update_sheet(self, username, expenditure_dict):
        """
        :param username: nombre de usuario que está realizando la acción
        :param expenditure_dict: diccionario que contiene la info del gasto realizado
        :param creds: credenciales ya obtenidas en el flujo de auth para realizar la acción
        """
        gc = gspread.authorize(self.creds)
        wks = gc.open_by_key(config.SPREADSHEET_ID).worksheet(config.SHEET_TITLE)
        date = datetime.date.today().strftime('%d/%m/%Y')
        description = expenditure_dict[username]['description']
        amount = expenditure_dict[username]['amount']
        category = expenditure_dict[username]['category']
        name = self._get_name()
        # TODO si varias personas están subiendo un gasto al mismo tiempo esto es fruta
        # una posible solución es agregar siempre una -nueva- fila arriba, en vez de abajo
        row_idx = self.next_available_row(wks)
        wks.insert_row((date, name, description, amount, category), int(row_idx), 'USER_ENTERED')

    @staticmethod
    def next_available_row(worksheet):
        str_list = list(filter(None, worksheet.col_values(1)))
        return str(len(str_list) + 1)

    def _get_name(self):
        """
            La tupla config.ENABLED_USERS tiene el conjunto de datos
            (username, real_name) y esto lo que hace es, en base a un username,
            nos devuelve esa info
        """
        #TODO un diccionario? tiene sentido que sean tuplas?
        filtered = list(filter(lambda x: x[0] == self.username, config.ENABLED_USERS))
        if len(filtered) == 0:
            return False
        return filtered[0][1]


class GoogleAuth(object):

    def __init__(self, username):
        super().__init__()
        self.username = username

    def is_authorized(self):
        store = self._get_storage_file()
        credential = store.get()
        return credential and not credential.invalid

    def get_credential(self, code=None):
        store = self._get_storage_file()
        credential = store.get()
        if not credential or credential.invalid:
            if code is None:
                flow = client.flow_from_clientsecrets('creds.json', SCOPES, redirect_uri=OOB_CALLBACK_URN)
                return flow.step1_get_authorize_url()
            else:
                credential = client.credentials_from_clientsecrets_and_code('creds.json', SCOPES, code,
                                                                            redirect_uri=OOB_CALLBACK_URN)
                store.put(credential)
                credential.set_store(store)

        return credential

    def _get_storage_file(self):
        return file.Storage(os.path.join('tokens', self.username + '.json'))

