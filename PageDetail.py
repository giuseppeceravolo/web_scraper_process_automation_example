from bs4 import BeautifulSoup as bs
import re


class PageDetail:
    def __init__(self, incarico_page_url):
        idIncarico_page = s.get(url=incarico_page_url, timeout=100, verify=False)
        self.pageContent = bs(idIncarico_page.content, features='html.parser')

    def _get_parte1_field(self, fieldname):
        num_info_parte1 = len(self.pageContent.find_all(attrs={"class": "portaItalInfoInner2-2"}))
        for i in range(num_info_parte1):
            if self.pageContent.find_all(attrs={"class": "portaItalInfoInner-2"})[i].text.strip() == fieldname:
                return self.pageContent.find_all(attrs={"class": "portaItalInfoInner2-2"})[i].text.strip()

    def get_rge(self):
        return self._get_parte1_field(fieldname='RGE/Anno:')

    def get_provincia(self):
        return self._get_parte1_field(fieldname='Provincia:')

    def get_dati_catastali(self):
        return self._get_parte1_field(fieldname='Dati catastali:')

    def get_ctu(self):
        return self._get_parte1_field(fieldname='Valore della CTU:')

    def _get_parte2_field(self, fieldname):
        num_info_parte2 = len(self.pageContent.find_all('tr'))
        for i in range(num_info_parte2):
            if self.pageContent.find_all('tr')[0].find_all('td')[i].text.strip() == fieldname:
                return self.pageContent.find_all('tr')[1].find_all('td')[i].text.strip()

    def get_numero_esperimento(self):
        return self._get_parte2_field(fieldname="Esperimento d’Asta n.")

    def get_prezzo_base(self):
        return self._get_parte2_field(fieldname="Basa Asta")

    def get_con_incanto(self):
        return self._get_parte2_field(fieldname="Con Incanto")

    @property
    def get_coordinate(self):
        google_maps_url = str(self.pageContent.find_all(href=re.compile("maps")))
        if len(google_maps_url) == 0:
            return ''
        else:
            return google_maps_url[google_maps_url.find("maps?q=")+7 : google_maps_url.find(" target=")-1].replace(',',';')