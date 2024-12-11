# Definizione della rete e dei collegamenti con i rispettivi costi

"""
#Test 1: rete randomica
network = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 6},
    'C': {'A': 4, 'B': 2, 'D': 3},
    'D': {'B': 6, 'C': 3}
}
"""

"""
#Test 2: rete lineare
network = {
    'A': {'B': 1},
    'B': {'A': 1, 'C': 2},
    'C': {'B': 2, 'D': 3},
    'D': {'C': 3}
}
"""

"""
#Test 3: rete a stella
network = {
    'A': {'B': 2, 'C': 5, 'D': 1},
    'B': {'A': 2},
    'C': {'A': 5},
    'D': {'A': 1}
}
"""

"""
#Test 4: rete con peso disuguale
network = {
    'A': {'B': 3, 'C': 10},
    'B': {'A': 3, 'C': 1, 'D': 8},
    'C': {'A': 10, 'B': 1, 'D': 2},
    'D': {'B': 8, 'C': 2}
}
"""

"""
#Test 5: rete completamente connessa
network = {
    'A': {'B': 2, 'C': 3, 'D': 7},
    'B': {'A': 2, 'C': 1, 'D': 4},
    'C': {'A': 3, 'B': 1, 'D': 2},
    'D': {'A': 7, 'B': 4, 'C': 2}
}
"""

"""
#Test 6: rete disconessa
network = {
    'A': {'B': 1},
    'B': {'A': 1},
    'C': {'D': 2},
    'D': {'C': 2}
}
"""

"""
#Test 7: rete circolare
network = {
    'A': {'B': 2, 'D': 4},
    'B': {'A': 2, 'C': 3},
    'C': {'B': 3, 'D': 1},
    'D': {'A': 4, 'C': 1}
}
"""

"""
#Test 8: rete con un solo nodo
network = {
    'A': {}
}
"""

"""
#Test 9: rete ad albero
network = {
    'A': {'B': 3, 'C': 1},
    'B': {'A': 3, 'D': 4, 'E': 2},
    'C': {'A': 1, 'F': 5},
    'D': {'B': 4},
    'E': {'B': 2},
    'F': {'C': 5}
}
"""

"""
#Test 10: rete con collegamenti unidirezionali
network = {
    'A': {'B': 1},
    'B': {'C': 1},
    'C': {'A': 1}
}
"""

"""
#Test 11: rete con costi elevati
network = {
    'A': {'B': 1, 'C': 100},
    'B': {'A': 1, 'C': 2},
    'C': {'B': 2, 'A': 100}
}
"""

def initialize_routing_tables(network):
    """
    Inizializza le tabelle di routing per ogni nodo
    - Ogni nodo conosce inizialmente solo le distanze verso i vicini diretti
    - La distanza a sé stesso è impostata a 0
    - La distanza verso gli altri nodi è impostata a infinito (float('inf'))
    - Aggiunge anche il next hop per ogni percorso
    """
    tables = {}
    for node in network:
        # Crea una tabella di routing iniziale per ogni nodo
        tables[node] = {
            "cost": {dest: float('inf') for dest in network},  # Imposta tutte le distanze a infinito
            "next_hop": {dest: None for dest in network}  # Imposta tutti i next hop a None
        }
        for neighbor, cost in network[node].items():
            tables[node]["cost"][neighbor] = cost  # Distanza verso i vicini diretti
            tables[node]["next_hop"][neighbor] = neighbor  # Next hop verso i vicini diretti
        tables[node]["cost"][node] = 0  # Distanza a sé stesso impostata a 0
        tables[node]["next_hop"][node] = node  # Next hop verso sé stesso è sé stesso
    return tables

def update_routing_table(tables, network):
    """
    Aggiorna le tabelle di routing utilizzando l'algoritmo Distance Vector
    - Ogni nodo verifica se può migliorare la distanza verso una destinazione passando attraverso uno dei suoi vicini
    - Se trova un percorso più corto aggiorna la sua tabella
    """
    updated = False  # Flag per memorizzare se ci sono stati aggiornamenti
    for node in network:
        for neighbor, cost_to_neighbor in network[node].items():
            # Itera attraverso le destinazioni conosciute dal vicino
            for dest in tables[neighbor]["cost"]:
                # Calcola il costo passando attraverso il vicino
                new_cost = tables[neighbor]["cost"][dest] + cost_to_neighbor
                # Aggiorna la distanza e il next hop se il nuovo costo è inferiore
                if tables[node]["cost"][dest] > new_cost:
                    tables[node]["cost"][dest] = new_cost
                    tables[node]["next_hop"][dest] = neighbor
                    updated = True
    return updated  # Ritorna true se ci sono stati aggiornamenti

def simulate_routing(network, max_iterations=100):
    """
    Simula il protocollo di routing Distance Vector fino alla convergenza
    - Le tabelle di routing sono stampate a ogni iterazione
    - La simulazione termina quando non ci sono più aggiornamenti o si raggiunge il numero massimo di iterazioni
    """
    # Inizializza le tabelle di routing
    tables = initialize_routing_tables(network)
    iteration = 0  # Conta il numero di iterazioni
    while iteration < max_iterations:
        # Stampa le tabelle di routing per l'iterazione corrente
        print(f"Iterazione {iteration}")
        for node, table in tables.items():
            print(f"Tabella di routing per {node}:")
            for dest in sorted(table["cost"].keys()):
                cost = table["cost"][dest]
                next_hop = table["next_hop"][dest]
                print(f"  Verso {dest}: costo = {cost}, next hop = {next_hop}")
        print()

        # Aggiorna le tabelle di routing
        updated = update_routing_table(tables, network)
        if not updated:  # Termina se non ci sono più aggiornamenti
            print("Convergenza raggiunta in " + str(iteration +1) + " iterazioni\n")
            break
        iteration += 1  # Incrementa il contatore delle iterazioni

    if iteration == max_iterations:  # Messaggio che indica che il limite massimo è stato raggiunto
        print("Limite massimo di iterazioni raggiunto\n")

    return tables  # Ritorna le tabelle finali

if __name__ == "__main__":
    # Esegue la simulazione e stampa le tabelle di routing finali
    final_tables = simulate_routing(network)
    print("Tabella di routing finale:")
    for node, table in final_tables.items():
        print(f"{node}:")
        for dest in sorted(table["cost"].keys()):
            cost = table["cost"][dest]
            next_hop = table["next_hop"][dest]
            print(f"  Verso {dest}: costo = {cost}, next hop = {next_hop}")

