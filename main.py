import requests
from utils import login, fetch_incarichi, insert_or_update_postgres


with requests.Session() as s:
    login(s)
    incarichi = fetch_incarichi(s)
    print("Numero totale affidamenti presenti: ", len(incarichi))
    for incarico in incarichi:
        insert_or_update_postgres(incarico)