import random

"""
Jugador automático para Buscaminas basado en:
(A) Prior global uniforme: minas_restantes / celdas_desconocidas
(B) Heurística local por reparto: cada casilla numérica r reparte m(r)/|U(r)|
    a sus vecinos desconocidos; combinamos contribuciones por celda con PROMEDIO
    y usamos max(prior, avg) como probabilidad final.
"""


class Player:
    '''
    Administra el conocimiento del tablero (revealed, flags, unknown)
    y elige la siguiente celda a destapar minimizando la probabilidad estimada.
    '''
    m_Plays = None

    '''
    Inicializa el estado interno del jugador.
    - revealed: dict {(i,j) -> número}
    - flags: set {(i,j)} si marcas minas (opcional, aquí no marcamos)
    - unknown: set {(i,j)} celdas no destapadas ni marcadas
    - w, h, n: dimensiones y número total de minas (se fijan al primer choose)
    '''
    def __init__(self, args):
        self.revealed = {}
        self.flags = set()
        self.unknown = None   # se inicializa perezosamente con (w,h)
        self.w = None
        self.h = None
        self.n_total = None
        self.m_Plays = []     # historial de jugadas

    # end def

    '''
    Recalcula y devuelve la probabilidad estimada para la celda (i,j),
    usando el prior global y la heurística por promedio.
    Nota: internamente calcula todas las probabilidades y retorna la de (i,j).
    '''
    def recalculate_probability(self, w, h, n, i, j):
        # Si es la primera vez, inicializa el universo de celdas
        if self.unknown is None:
          self.w, self.h, self.n_total = w, h, n
          self.unknown = set()
          # Ciclo externo: filas i en [0, w)
          for i in range(w):
              # Ciclo interno: columnas j en [0, h)
              for j in range(h):
                  self.unknown.add((i, j))


        probs = estimate_probs_uniform_and_local(
            self.w, self.h, self.n_total, self.revealed, self.flags, self.unknown
        )
        return probs.get((i, j), 1.0)

    # end def

    '''
    Elige la celda con la MENOR probabilidad estimada de contener mina.
    - Si es la primera llamada, inicializa unknown con todas las celdas (w x h).
    - Calcula prior y contribuciones locales; combina por promedio.
    - Desempata por orden lexicográfico (i, j) para reproducibilidad.
    Retorna: (i, j)
    '''
    def choose_cell(self, w, h, n):
        # Inicialización perezosa del universo de celdas
        if self.unknown is None:
          self.w, self.h, self.n_total = w, h, n
          self.unknown = set()
          # Ciclo externo: filas i en [0, w)
          for i in range(w):
              # Ciclo interno: columnas j en [0, h)
              for j in range(h):
                  self.unknown.add((i, j))


        probs = estimate_probs_uniform_and_local(
            self.w, self.h, self.n_total, self.revealed, self.flags, self.unknown
        )
        i, j = choose_min_prob_cell(probs)
        self.m_Plays.append((i, j))
        return (i, j)

    # end def

    '''
    Reporta el resultado de destapar (i,j) con valor numérico 'val' del Board.
    - Actualiza revealed y elimina (i,j) de unknown.
    - (Opcional) si implementaras flags, podrías marcarlas en otra función.
    '''
    def report(self, i, j, val):
        # Guardar el número visto y quitar de desconocidas
        self.revealed[(i, j)] = val
        if self.unknown is not None:
            self.unknown.discard((i, j))

    # end def

# end class


def neighbors(w, h, i, j):
    """
    Genera todos los vecinos (8 casillas adjacentes) de (i,j) dentro del tablero.
    - Doble for sobre el rango [i-1, i+1] x [j-1, j+1]
    Retorna: lista de (x, y)
    """
    neighbors_list = []
    # Ciclo externo: x en {i-1, i, i+1}
    for x in range(i - 1, i + 2):
        # Ciclo interno: y en {j-1, j, j+1}
        for y in range(j - 1, j + 2):
            if (x, y) != (i, j) and 0 <= x < w and 0 <= y < h:
                neighbors_list.append((x, y))
    return neighbors_list


def combine_avg(contribs, prior):
    """
    Combina contribuciones locales por PROMEDIO y respeta un piso 'prior'.
    - Si no hay contribuciones, devuelve prior.
    - Si hay, p_final = max(prior, promedio(contribs)).
    """
    if not contribs:
        return prior
    avg = sum(contribs) / len(contribs)
    return max(prior, avg)


def frontier_numbers(revealed, unknown, flags, w, h):
    """
    Construye la 'frontera': todas las casillas numéricas reveladas que
    tienen al menos un vecino desconocido.
    Para cada número r en (i,j), devuelve tupla:
      (i, j, r, unk_list, flags_count)
    donde:
      - unk_list: lista de vecinos desconocidos U(r)
      - flags_count: cuántos vecinos marcados como mina (si se usa flags)
    Recorre:
      - for (i,j), r in revealed.items(): todas las casillas destapadas
      - for (x,y) in neighbors(...): sus 8 vecinos
    """
    fr = []
    # Recorre todas las casillas reveladas
    for (i, j), r in revealed.items():
        unk = []
        flg = 0
        # Recorre todos los vecinos de (i,j)
        for (x, y) in neighbors(w, h, i, j):
            if (x, y) in unknown:
                unk.append((x, y))
            elif (x, y) in flags:
                flg += 1
        if unk:
            fr.append((i, j, r, unk, flg))
    return fr


def estimate_probs_uniform_and_local(w, h, n_total, revealed, flags, unknown):
    """
    Calcula la probabilidad estimada de mina para cada celda desconocida:
    1) Prior global uniforme = minas_restantes / celdas_desconocidas
    2) Heurística:
       - Para cada casilla numérica r con U(r) desconocidos y F(r) flags:
         m_pend = r - F(r)
         contribución por vecino = m_pend / |U(r)|   (si m_pend > 0)
       - Para una celda dada, combina contribuciones con PROMEDIO
         y aplica p_final = max(prior, avg)
    Retorna: dict { (i,j) -> prob_estimada }
    """
    mines_known = len(flags)
    celdas_desconocidas = len(unknown)

    if celdas_desconocidas == 0:
        return {}

    minas_restantes = n_total - mines_known
 
    prior = minas_restantes / celdas_desconocidas if celdas_desconocidas > 0 else 1.0


    fr = frontier_numbers(revealed, unknown, flags, w, h)

    # Si no hay frontera, todas las desconocidas comparten el prior
    if not fr:
        return {cell: prior for cell in unknown}

    # Junta contribuciones por celda desconocida
    per_cell = {cell: [] for cell in unknown}
    # Recorre cada número en la frontera
    for (i, j, r, unk, flg) in fr:
        m_pend = r - flg
        if m_pend <= 0:

            continue
        c = m_pend / len(unk)
        # Recorre vecinos desconocidos para asignarles contribución
        for cell in unk:
            per_cell[cell].append(c)

    probs = {}
    # Recorre todas las celdas desconocidas
    for cell in unknown:
        contribs = per_cell.get(cell, [])
        probs[cell] = combine_avg(contribs, prior)

    return probs


def choose_min_prob_cell(probs):
    """
    Elige la celda con menor probabilidad; desempata por (i, j).
    Recorre el diccionario (cell -> prob) y aplica min con tupla de orden.
    Retorna: (i, j)
    """
    # La key evalúa: (prob, i, j) para desempatar determinísticamente
    return min(probs.items(), key=lambda kv: (kv[1], kv[0][0], kv[0][1]))[0]
