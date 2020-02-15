class Incarico:
    def __init__(self, id_incarico, pid, tribunale, rge, data_asta, tipo_uso, citta, stato_incarico, provincia,
                 dati_catastali, ctu, numero_esperimento, prezzo_base, con_incanto, coordinate):
        self.id_incarico = id_incarico
        self.pid = pid
        self.tribunale = tribunale
        self.rge = rge
        self.data_asta = data_asta
        self.tipo_uso = tipo_uso
        self.citta = citta
        self.stato_incarico = stato_incarico
        self.provincia = provincia
        self.dati_catastali = dati_catastali
        self.ctu = ctu
        self.numero_esperimento = numero_esperimento
        self.prezzo_base = prezzo_base
        self.con_incanto = con_incanto
        self.coordinate = coordinate

    def __str__(self):
        return ("id incarico:" + self.id_incarico + " pid:" + self.pid + " Tribunale:" + self.tribunale +
                " RGE:" + self.rge + " Data Asta:" + self.data_asta + " Destinazione d'uso:" + self.tipo_uso +
                " Città:" + self.citta + " Stato incarico:" + self.stato_incarico + " Provincia:" + self.provincia +
                " Dati Catastali:" + self.dati_catastali + " CTU:" + self.ctu +
                " Numero Esperimento:" + self.numero_esperimento + " Prezzo Base:" + self.prezzo_base +
                " Con incanto:" + self.con_incanto + " Coordinate:" + self.coordinate)