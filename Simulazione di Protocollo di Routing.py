"""
Progetto Python: Simulazione di Protocollo di Routing
"""

"""
Nome: Nikolai
Cognome: Zanni
Matricola: 0001069041

Nome: Emily
Cognome: Pedini
Matricola: 0001081969

Nome: Benedetta
Cognome: Barone
Matricola: 0001081612
"""

"""
Progetto Python: Simulazione di Protocollo di Routing
Descrizione: Creare uno script Python che simuli un protocollo di routing semplice, come il Distance Vector Routing. 
Gli studenti implementeranno gli aggiornamenti di routing tra i nodi, con il calcolo delle rotte più brevi.
Obiettivi: Implementare la logica di aggiornamento delle rotte, gestione delle tabelle di routing e calcolo delle distanze tra nodi.
Consegne richieste: Codice Python ben documentato, output delle tabelle di routing per ogni nodo e relazione finale che spieghi 
il funzionamento dello script.
"""

DISTANZA_MASSIMA = float('inf')  #distnza massima per i nodi non raggiungibili

"""
Inizializza un nodo.
"""
class Nodo:
    
    def __init__(self, nome):
        self.nome = nome  #nome del nodo.
        self.tabella_instradamento = {}  #tabella di instradamento del nodo: {destinazione: (costo, prossimo_passo)}.
        self.vicini = {}  #distanze ai vicini diretti: {vicino: costo}.

    """
    Aggiorna la tabella di instradamento in base al vettore delle distanze ricevuto da un vicino.
    """
    def aggiorna_tabella(self, mittente, vettore_distanze):
        aggiornata = False
        for destinazione, costo in vettore_distanze.items():
            if destinazione == self.nome:  
                continue
            nuovo_costo = costo + self.vicini[mittente] #calcola il nuovo costo passando per il vicino.
            if destinazione not in self.tabella_instradamento or nuovo_costo < self.tabella_instradamento[destinazione][0]: 
                self.tabella_instradamento[destinazione] = (nuovo_costo, mittente)  #aggiorna se il percorso è nuovo o più conveniente.
                aggiornata = True  #true se la tabella è stata aggiornata.
        return aggiornata

    """
    Genera e invia il proprio vettore delle distanze basato sulla tabella di instradamento.
    """
    def invia_vettore_distanze(self):
        return {dest: costo for dest, (costo, _) in self.tabella_instradamento.items()}

    """
    Restituisce una rappresentazione leggibile della tabella di instradamento del nodo.
    """
    def __str__(self):
        return "; ".join(
            f"{dest}: {'inf' if costo >= DISTANZA_MASSIMA else f'{costo},{prossimo_passo}'}"
            for dest, (costo, prossimo_passo) in sorted(self.tabella_instradamento.items())
        )

"""
Costruisce il vettore delle distanze da una tabella di instradamento.
"""
def costruisci_vettore_distanze(tabella_instradamento):
    return {dest: costo for dest, (costo, _) in tabella_instradamento.items()}

"""
Stampa un messaggio di log con lo stato di una tabella di instradamento.
"""
def log_tabella(nodo, messaggio, tabella):
    print(f"{nodo} {messaggio}: [{tabella}]")

"""
Simula il protocollo di Distance Vector Routing su una rete definita da un grafo.
"""
def simula_instradamento(grafo):
    with open("Risultati_Simulazione_di_Protocollo_di_Routing.txt", "w") as file:  #apre un file per salvare tutti i risultati.
        def print_to_file(*args, **kwargs):
            print(*args, **kwargs)  # stampa su terminale.
            print(*args, **kwargs, file=file)  #stampa sul file.
        nodi = {nome: Nodo(nome) for nome in grafo}  #crea un oggetto Nodo per ogni nodo nel grafo, inizializzando la rete.
        for nodo, vicini in grafo.items():  #configura le tabelle di instradamento iniziali per ogni nodo.
            for vicino, costo in vicini.items(): 
                nodi[nodo].vicini[vicino] = costo  #aggiunge i vicini diretti con i loro costi.
                nodi[nodo].tabella_instradamento[vicino] = (costo, vicino)  #configura il prossimo passo per i vicini.
            for altro_nodo in grafo:
                if altro_nodo != nodo and altro_nodo not in nodi[nodo].tabella_instradamento:
                    nodi[nodo].tabella_instradamento[altro_nodo] = (DISTANZA_MASSIMA, None) #per i nodi non direttamente vicini, imposta il costo come infinito.
        print_to_file("Tabelle di instradamento iniziali:") #stampa le tabelle di instradamento iniziali.
        for nodo in nodi:
            print_to_file(f"DV({nodo}) = {nodi[nodo].invia_vettore_distanze()}")
        iterazione = 0
        while True:  #inizia il ciclo per calcolare le rotte fino a convergenza.
            iterazione += 1
            print_to_file(f"\nIterazione: {iterazione}")
            aggiornamenti = {nodo: nodi[nodo].invia_vettore_distanze() for nodo in nodi}  #ottiene i vettori delle distanze aggiornati di tutti i nodi.
            ci_sono_aggiornamenti = False  # flag per verificare se ci sono stati aggiornamenti.
            for nodo in nodi:
                for vicino in nodi[nodo].vicini:
                    tabella_prima = str(nodi[nodo])  #salva lo stato della tabella prima dell'aggiornamento.
                    aggiornata = nodi[nodo].aggiorna_tabella(vicino, aggiornamenti[vicino]) #per ogni nodo, aggiorna la tabella basandosi sui dati ricevuti dai vicini.
                    tabella_dopo = str(nodi[nodo])  #salva lo stato della tabella dopo l'aggiornamento.
                    print_to_file(f"\n{nodo} riceve DV({vicino}): {aggiornamenti[vicino]}")
                    print_to_file(f"{nodo} Tabella prima: [{tabella_prima}]")
                    print_to_file(f"{nodo} Tabella dopo: [{tabella_dopo}]")
                    if aggiornata:
                        ci_sono_aggiornamenti = True  # se c'è stato un aggiornamento, cambia il flag in true.
            print_to_file("\nTabelle di instradamento dopo l'iterazione:") #stampa le tabelle di instradamento aggiornate.
            for nodo in nodi:
                print_to_file(f"DV({nodo}): {nodi[nodo].invia_vettore_distanze()}")
            if not ci_sono_aggiornamenti:
                print_to_file("\nNessun aggiornamento necessario")
                break  #termina il ciclo se non ci sono stati ulteriori aggiornamenti.


if __name__ == "__main__":
    grafo = {
        'A': {'A': 0, 'B': 1, 'C': 6},
        'B': {'B': 0, 'A': 1, 'C': 2, 'D': 1},
        'C': {'C': 0, 'A': 6, 'B': 2, 'D': 3, 'E': 7},
        'D': {'D': 0, 'B': 1, 'C': 3, 'E': 2},
        'E': {'E': 0, 'C': 7, 'D': 2},
    }
    simula_instradamento(grafo)

