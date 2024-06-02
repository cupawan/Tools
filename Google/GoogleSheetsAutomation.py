import gspread
import yaml


class GoogleSheetsAutomation:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.config_file_path,'r') as file:
                config = yaml.safe_load(file)
                return config
        except Exception as e:
            d = {}
            print("Error loading configuration")
            return d
        
    def set_up_gc(self):
        gc = gspread.service_account(filename= self.config['GOOGLE_CLIENT_SECRETS_PATH'])
        return gc
    
    def select_worksheet(self,sheet_name = None, worksheet_index = None, sheet_url = None, worksheet_name = None):
        if sheet_url:
            wks = self.set_up_gc().open_by_url(sheet_url)
        elif sheet_name:
            wks = self.set_up_gc().open(sheet_name)
        if worksheet_index == 0 or worksheet_index:
            sh = wks.get_worksheet(worksheet_index)
        elif worksheet_name:
            sh = wks.get_worksheet(worksheet_name)
        return sh


    
    def insert_values(self,sheet,range_of_cells = None, range_of_cells_vlaues:list = None, single_cell = False, single_cell_value = None,append_row = None, append_rows = None):
        if range_of_cells:
            sheet.update(range_name = range_of_cells, values = [range_of_cells_vlaues])
        elif single_cell:
            sheet.update([[single_cell_value]], single_cell )
        elif append_row:
            sheet.append_row(append_row)
        elif append_rows:
            sheet.append_rows(append_rows)

    def create_new_worksheet(self, new_worksheet_title):
        try:
            self.set_up_gc().create(new_worksheet_title)
            return True
        except Exception as e:
            print(f"Error while creating sheet: {e}")
            return False
        
    def clear_sheet(self, sh):
        try:
            sh.clear()
            return True
        except Exception as e:
            print(f"Error while clearing sheet: {e}")
            return False
        
    def format_sheet(self,sh, params:dict, range):
        try:
            sh.format(range, {'textFormat': params})
            return True
        except Exception as e:
            print(f"Error while formatting sheet: {e}")
            return False
