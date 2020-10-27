import requests, xlsxwriter, lxml, pandas, datetime
from bs4 import BeautifulSoup

class doviz():

    def __init__(self):
        self.pageDoviz = requests.get("https://www.doviz.com/")
        self.soup = BeautifulSoup(self.pageDoviz.text, 'lxml')
        self.currency_values_list = []
        self.currency_names_list = []
        self.df_dict = {}
        self.currency_percentage_list = []

    def collect_values(self):

        currency_values = self.soup.find_all('span', class_='value')
        for item in currency_values:
            self.currency_values_list.append(item.text)
        print(self.currency_values_list)
    
    def collect_names(self):
        
        currency_names = self.soup.find_all("span", class_="name")
        for name in currency_names:
            self.currency_names_list.append(name.text)
        print(self.currency_names_list)

    def collect_percentage(self):
        currency_percentages = self.soup.select("[class~=change]")
        for item in currency_percentages:
            self.currency_percentage_list.append(item.text.strip())
        print(self.currency_percentage_list)
    
    def create_dataframe(self):
        now = datetime.datetime.today().strftime("%d/%b/%Y - %H.%M.%S")
                      
        self.doviz_df = pandas.DataFrame({'Tarih':now, 'Kur':self.currency_names_list, 'Satış':self.currency_values_list,'Yüzdelik':self.currency_percentage_list})
        print(self.doviz_df)
    
    def excel_writer(self):
        writer = pandas.ExcelWriter('dovizcom_scraper.xlsx', engine="xlsxwriter")
        self.doviz_df.to_excel(writer, sheet_name="Kur Satış")
        writer.save()


deneme = doviz()

deneme.collect_values()
deneme.collect_names()
deneme.collect_percentage()
deneme.create_dataframe()
deneme.excel_writer()