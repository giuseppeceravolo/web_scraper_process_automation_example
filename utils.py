from Incarico import Incarico
from PageDetail import PageDetail
import json
from bs4 import BeautifulSoup as bs
import psycopg2
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def login(session):
    login_url = "https://website.homepage.it/php/login.php"
    username = 'username'
    password = 'password'
    login_data = {
        "username": username,
        "password": password,
        "accedi": "accedi",
        "ajaxReq": 1
    }
    session.post(url=login_url, data=login_data, timeout=100, verify=False)


def parse_link(link_id_incarico, link_pid):
    soup_idIncarico = bs(link_id_incarico, features="lxml")
    incarico_link = soup_idIncarico.find("a", href=True).get('href')
    incarico_id = soup_idIncarico.find("a", href=True).string
    soup_pid = bs(link_pid, features="lxml")
    pid = soup_pid.find("a", href=True).string
    return incarico_id, incarico_link, pid


def fetch_incarichi(s):
    get_incarichi_url = "https://website.private.it/php/getIncarichi.php"
    get_incarichi_data = {
        "researchType": "",
        "incaricoId": "",
        "dateFrom": "",
        "dataTo": "",
        "status": ""
    }
    get_incarichi = s.post(url=get_incarichi_url, data=get_incarichi_data, timeout=100, verify=False)
    incarichi_json = json.loads(get_incarichi.content.decode('utf-8-sig'))
    incarichi = []
    for incarico_json in incarichi_json['data']:
        incarico_id, incarico_link, pid = parse_link(incarico_json["idIncarico"], incarico_json["pid"])
        page_detail = PageDetail(incarico_link)
        rge = page_detail.get_rge()
        provincia = page_detail.get_provincia()
        dati_catastali = page_detail.get_dati_catastali()
        ctu = page_detail.get_ctu()
        numero_esperimento = page_detail.get_numero_esperimento()
        prezzo_base = page_detail.get_prezzo_base()
        con_incanto = page_detail.get_con_incanto()
        coordinate = page_detail.get_coordinate
        incarichi.append(Incarico(incarico_id,
                                  pid,
                                  incarico_json["tribunale"],
                                  rge,
                                  incarico_json["dataAsta"],
                                  incarico_json["tipoUso"],
                                  incarico_json["citta"],
                                  incarico_json["statoIncarico"],
                                  provincia,
                                  dati_catastali,
                                  ctu,
                                  numero_esperimento,
                                  prezzo_base,
                                  con_incanto,
                                  coordinate
                                  )
                         )
    return incarichi


def insert_or_update_postgres(incarico):
    sql = """INSERT INTO public.incarichi (id,
                                            pid,
                                            tribunale,
                                            rge,
                                            data_asta,
                                            tipo_uso,
                                            citta,
                                            stato_incarico,
                                            provincia,
                                            dati_catastali,
                                            ctu,
                                            numero_esperimento,
                                            prezzo_base,
                                            con_incanto,
                                            coordinate)
                                    VALUES (%s,
                                            %s,
                                            %s,
                                            %s,
                                            %s,
                                            %s,
                                            %s,
                                            %s,
                                            %s,
                                            %s,
                                            %s,
                                            %s,
                                            %s,
                                            %s,
                                            %s)
            ON CONFLICT DO NOTHING;"""
    conn = None
    try:
        conn = psycopg2.connect(dbname="scrapingdb", user="giuseppe", password="ceravolo",
                                host="199.199.199.199", port="21")
        cur = conn.cursor()
        cur.execute(sql,
                    (incarico.id_incarico,
                     incarico.pid,
                     incarico.tribunale,
                     incarico.rge,
                     incarico.data_asta,
                     incarico.tipo_uso,
                     incarico.citta,
                     incarico.stato_incarico,
                     incarico.provincia,
                     incarico.dati_catastali,
                     incarico.ctu,
                     incarico.numero_esperimento,
                     incarico.prezzo_base,
                     incarico.con_incanto,
                     incarico.coordinate))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()