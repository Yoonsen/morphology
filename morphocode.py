import sqlite3
import torch
import pyro
import pyro.distributions as dist
from pyro.infer import SVI, Trace_ELBO
from pyro.optim import Adam

# --- DEL 1: DATABASEN (SQLite) ---

def setup_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Skjema basert på Johnsens logikk [cite: 13, 19]
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY,
        word TEXT UNIQUE NOT NULL,
        is_stem_word BOOLEAN DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS splits (
        id INTEGER PRIMARY KEY,
        word_id INTEGER,
        stem TEXT NOT NULL,
        suffix TEXT NOT NULL,
        stem_is_word BOOLEAN,
        FOREIGN KEY (word_id) REFERENCES words(id)
    );

    CREATE TABLE IF NOT EXISTS affix_stats (
        suffix TEXT PRIMARY KEY,
        total_stems INTEGER,      -- |y*| [cite: 79]
        stems_in_wordlist INTEGER -- |y* ∩ W| [cite: 84, 117]
    );

    CREATE INDEX IF NOT EXISTS idx_splits_suffix ON splits(suffix);
    """)
    conn.commit()
    return conn

def populate_affix_stats(conn):
    """Beregner alfa/beta grunnlag basert på distribusjonell evidens [cite: 7, 85]"""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM affix_stats")
    
    # Johnsens ratio: stems som er ord delt på alle mulige stems [cite: 9, 116]
    sql = """
    INSERT INTO affix_stats (suffix, total_stems, stems_in_wordlist)
    SELECT 
        suffix, 
        COUNT(DISTINCT stem) as total_stems,
        SUM(CASE WHEN stem_is_word = 1 THEN 1 ELSE 0 END) as stems_in_wordlist
    FROM splits
    GROUP BY suffix
    HAVING total_stems > 1
    """
    cursor.execute(sql)
    conn.commit()

# --- DEL 2: PYRO MODELLERING (The Principled Argument) ---

def model(word_ids, trigram_ids, word_exists):
    """
    Probabilistisk modell som erstatter Johnsens manuelle beregninger[cite: 90, 119].
    """
    # Prior for global affiks-produktivitet
    alpha_prior = pyro.sample("alpha_prior", dist.Gamma(1.0, 1.0))
    
    # Her peller vi ut data for hver splitt-hypotese
    with pyro.plate("data", len(word_ids)):
        # Vi henter alfa og beta fra SQLite i praksis (her forenklet for Pyro-eksempel)
        # alpha = stems_in_wordlist + trigram_vekt
        # beta = total_stems - stems_in_wordlist
        
        # Sannsynlighet for at splitten er korrekt gitt kontekst og distribusjon [cite: 58, 101]
        theta = pyro.sample("theta", dist.Beta(alpha_prior, 1.0))
        
        # Observasjon: Er dette et faktisk ord i W? [cite: 57]
        pyro.sample("obs_word", dist.Bernoulli(theta), obs=word_exists)

def guide(word_ids, trigram_ids, word_exists):
    """Lærer parameterne som best forklarer dataene uten '6. roten' [cite: 93]"""
    # Pyro lærer seg vektene (variational parameters)
    auto_alpha = pyro.param("auto_alpha", torch.ones(len(word_ids)), 
                            constraint=dist.constraints.positive)
    
    with pyro.plate("data", len(word_ids)):
        pyro.sample("theta", dist.Beta(auto_alpha, 1.0))

# --- DEL 3: ANALYSE-FUNKSJON ---

def analyze_word(conn, word, context_trigram_id):
    """
    Modernisert versjon av beslutningsskjemaet[cite: 129].
    Bruker trigrammer for å løse tvetydighet (f.eks. pilspiss).
    """
    cursor = conn.cursor()
    # Hent alle mulige splitter for ordet [cite: 43]
    cursor.execute("""
        SELECT s.stem, s.suffix, a.stems_in_wordlist, a.total_stems 
        FROM splits s
        JOIN affix_stats a ON s.suffix = a.suffix
        JOIN words w ON s.word_id = w.id
        WHERE w.word = ?
    """, (word,))
    
    hypotheses = cursor.fetchall()
    results = []
    
    for stem, suffix, in_w, total in hypotheses:
        # Beregn alfa og beta (Principled Argument [cite: 6, 117])
        # Vi legger til en fiktiv trigram-støtte her (din indeks)
        trigram_support = 1.0 # placeholder
        
        alpha = 1.0 + in_w + trigram_support
        beta = 1.0 + (total - in_w)
        
        # Beregn sannsynlighet (erstatter Johnsens 'mean - std.dev') [cite: 90]
        prob = alpha / (alpha + beta)
        results.append((stem, suffix, prob))
        
    # Returner best rangerte hypotese [cite: 129]
    return sorted(results, key=lambda x: x[2], reverse=True)

# --- HOVEDLØP ---

if __name__ == "__main__":
    db_path = "morfologi_2026.db"
    # 1. Oppsett
    conn = setup_database(db_path)
    
    # 2. Populer statistikk basert på dine 1.6 mill rader
    # populate_affix_stats(conn) 
    
    # 3. Eksempel på analyse
    # result = analyze_word(conn, "mannen", 12345)
    # print(f"Beste splitt: {result[0]}")
