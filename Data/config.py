"""
Configurare Globală pentru Disertație - YouTube Comments Analysis
Facultatea de Sociologie și Asistență Socială, UBB Cluj-Napoca
Master: Analiza Datelor Complexe

Autor: Răzvan-Andrei Enache
Coordonator: Lect. Dr. Univ. Cristian Pop
An: 2026
"""

import os
import re
import numpy as np
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# =============================================================================
# LOAD ENVIRONMENT VARIABLES (din fișierul .env)
# =============================================================================
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)
HF_TOKEN = os.getenv("HF_TOKEN")

# =============================================================================
# SEED-URI PENTRU REPRODUCTIBILITATE
# =============================================================================
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# =============================================================================
# PATHS
# =============================================================================
BASE_DIR = Path(__file__).parent
DATA_RAW = BASE_DIR / 'data' / 'raw'
DATA_PROCESSED = BASE_DIR / 'data' / 'processed'
DATA_OUTPUT = BASE_DIR / 'dissertation_outputs'

# Create directories if they don't exist
for path in [DATA_RAW, DATA_PROCESSED, DATA_OUTPUT]:
    path.mkdir(parents=True, exist_ok=True)

# Input files
FILE_COMMENTS_RAW = DATA_RAW / 'yt_raw_comments.csv'
FILE_METADATA_RAW = DATA_RAW / 'yt_raw_metadata.csv'

# Output files
FILE_COMMENTS_CLEANED = DATA_PROCESSED / 'comments_cleaned.csv'
FILE_COMMENTS_ANALYZED = DATA_PROCESSED / 'comments_analyzed.csv'
FILE_STATISTICAL_RESULTS = DATA_OUTPUT / 'statistical_results.md'
FILE_VALIDATION_SAMPLE = DATA_OUTPUT / 'validation_sample.csv'

# =============================================================================
# COLUMN MAPPING (din CSV-urile tale către pipeline)
# =============================================================================
COMMENTS_COLUMN_MAP = {
    'Video ID': 'video_id',
    'Author Name': 'author_name',
    'Comment Text': 'comment_text',
    'Comment Date': 'comment_date',
    'Comment Likes': 'comment_likes',
    'Replies': 'replies',
    'Is Creator': 'is_creator'
}

METADATA_COLUMN_MAP = {
    'Video ID': 'video_id',
    'Video Title': 'video_title',
    'Video Date': 'video_date',
    'Video Views': 'video_views',
    'Video Likes': 'video_likes',
    'Video Comment Count': 'video_comment_count',
    'Video URL': 'video_url',
    'Spam Filtered': 'spam_filtered'
}

# =============================================================================
# PERIOADA ELECTORALĂ (Turul 2 - 2025)
# =============================================================================
DATE_START = '2025-05-01'   # Prima zi de campanie oficială tur 2
DATE_END = '2025-05-18'     # Ziua înainte de rezultate (confirmare rezultate)

# =============================================================================
# FILTRE CALITATE
# =============================================================================
MIN_WORD_COUNT = 5          # Comentarii cu minim 5 cuvinte (pentru RQ3)
MIN_CHAR_LENGTH = 20        # Lungime minimă în caractere
EXCLUDE_SPAM = True         # Excludem videoclipuri marcate ca spam
EXCLUDE_CREATOR_COMMENTS = True  # Excludem comentariile creatorului canalului

# =============================================================================
# CANDIDATE KEYWORDS (română)
# =============================================================================
SIMION_KEYWORDS = [
    'simion',
    'george simion',
    'aur',
    'george'
]

NICUSOR_KEYWORDS = [
    'nicușor',
    'nicuşor',  # diacritice alternative
    'nicusor',
    'nicușor dan',
    'nicusor dan'
]

# =============================================================================
# STOPWORDS ROMÂNEȘTI (pentru BERTopic și preprocessing)
# =============================================================================
ROMANIAN_STOPWORDS = {
    'și', 'în', 'cu', 'de', 'la', 'pe', 'că', 'să', 'nu', 'da',
    'un', 'una', 'unei', 'unui', 'acest', 'aceasta', 'aceste', 'acești',
    'este', 'sunt', 'fi', 'fost', 'fiind', 'am', 'ai', 'a', 'au', 'avea',
    'pentru', 'prin', 'dar', 'sau', 'mai', 'foarte', 'prea', 'tot', 'toți',
    'toate', 'totul', 'ce', 'cei', 'cele', 'cine', 'când', 'unde', 'cum',
    'dacă', 'iar', 'ori', 'ne', 'vă', 'îmi', 'îți', 'își', 'noastră', 'voastră',
    'din', 'care', 'acea', 'acel', 'aceia', 'acelea', 'oricare', 'oricine',
    'ceva', 'cineva', 'nimic', 'nimeni', 'alt', 'alta', 'alții', 'altele',
    'asemenea', 'astfel', 'așa', 'atunci', 'acum', 'azi', 'ieri', 'mâine',
    'bine', 'rău', 'mare', 'mic', 'nou', 'vechi', 'prim', 'ultim',
    'doi', 'două', 'trei', 'patru', 'cinci', 'zece', 'sută', 'mie',
    'ca', 'si', 'la', 'din', 'care', 'acea', 'acel', 'aceia', 'acelea',
    'intr', 'intru', 'printr', 'fara', 'dupa', 'pana', 'spre', 'contra',
    'acum', 'apoi', 'inca', 'doar', 'chiar', 'parca', 'oare', 'prea',
    'mult', 'putin', 'atat', 'cat', 'tot', 'toti', 'toate', 'totul',
    'cel', 'cea', 'celui', 'celei', 'celor', 'unui', 'unei', 'unora',
    'altul', 'alta', 'altii', 'altele', 'altora', 'fiecare', 'fieci',
    'oricare', 'oricum', 'oricand', 'oricat', 'deci', 'insa', 'totusi',
    'asadar', 'precum', 'adica', 'respectiv', 'ulterior', 'anume', 'numai',
    'numai', 'nici', 'niciun', 'nicio', 'niciuna', 'niciunii', 'niciunele',
    'vreun', 'vreuna', 'vreunii', 'vreunele', 'cutare', 'atari', 'ataria',
    'aiurea', 'incolo', 'acolo', 'aici', 'dincolo', 'departe', 'aproape',
    'cam', 'prea', 'foarte', 'destul', 'suficient', 'prea', 'cam',
    'ei', 'ele', 'el', 'ea', 'eu', 'tu', 'noi', 'voi', 'ei', 'ele',
    'mie', 'tie', 'lui', 'ei', 'noua', 'voua', 'lor', 'meu', 'mea',
    'mei', 'mele', 'tau', 'ta', 'tai', 'tale', 'sau', 'sa', 'ti', 'mi',
    'o', 'il', 'ii', 'le', 'li', 'm', 't', 's', 'l', 'i', 'am', 'ai',
    'are', 'avem', 'aveti', 'au', 'as', 'ai', 'ar', 'am', 'ati', 'ar',
    'fost', 'fi', 'fiu', 'fii', 'fim', 'fiti', 'fi', 'fiind', 'avand',
    'fac', 'faci', 'face', 'facem', 'faceti', 'fac', 'facut', 'faca',
    'zic', 'zici', 'zice', 'zicem', 'ziceti', 'zic', 'zis', 'zica',
    'vin', 'vii', 'vine', 'venim', 'veniti', 'vin', 'venit', 'vina',
    'iau', 'iei', 'ia', 'luam', 'luati', 'iau', 'luat', 'lua',
    'mananc', 'mananci', 'mananca', 'mancam', 'mancati', 'mananca',
    'beau', 'bei', 'bea', 'bem', 'beti', 'beau', 'baut', 'bea',
    'dorm', 'dormi', 'doarme', 'dormim', 'dormiti', 'dorm', 'dormit',
    'merg', 'mergi', 'merge', 'mergem', 'mergeti', 'merg', 'mers',
    'vad', 'vezi', 'vede', 'vedem', 'vedeti', 'vad', 'vazut', 'vada',
    'stiu', 'stii', 'stie', 'stim', 'stieti', 'stiu', 'stiut', 'stia',
    'vreau', 'vrei', 'vrea', 'vrem', 'vreti', 'vor', 'vrut', 'vrea',
    'pot', 'poti', 'poate', 'putem', 'puteti', 'pot', 'putut', 'putea',
    'trebuie', 'trebui', 'trebuit',
    'rog', 'rogi', 'roaga', 'rugam', 'rugati', 'roaga', 'rugat',
    'intreb', 'intrebi', 'intreaba', 'intrebam', 'intrebati', 'intreaba',
    'raspund', 'raspunzi', 'raspunde', 'raspundem', 'raspundeti', 'raspund',
    'spun', 'spui', 'spune', 'spunem', 'spuneti', 'spun', 'spus', 'spuna',
    'cred', 'crezi', 'crede', 'credem', 'credeti', 'cred', 'crezut', 'creda',
    'vreau', 'vrei', 'vrea', 'vrem', 'vreti', 'vor', 'vrut', 'vrea',
    'ok', 'okay', 'da', 'nu', 'ba', 'pai', 'ei', 'he', 'hai', 'hopa',
    'aha', 'hm', 'hmm', 'eh', 'ei', 'ma', 'te', 'se', 'ne', 'va', 'le',
    'mi', 'ti', 'si', 'ti', 'vi', 'li'
}

# =============================================================================
# MODELE NLP
# =============================================================================
ROBERTA_MODEL = 'readerbench/ro-sentiment'  # 2 clase: positive/negative
BERTOPIC_EMBEDDING_MODEL = 'readerbench/RoBERT-base'  # ROMÂNESC
BERTOPIC_MIN_TOPIC_SIZE = 10      # ← Mai mic = mai multe topic-uri
BERTOPIC_TOP_N_WORDS = 10
BERTOPIC_N_TOPICS = None

# =============================================================================
# CONFIGURĂRI STATISTICE
# =============================================================================
SIGNIFICANCE_LEVEL = 0.05
BOOTSTRAP_SAMPLES = 2000
BOOTSTRAP_CI = 0.95
ENGAGEMENT_Q99_CAP = 0.99  # Cap engagement la Q99 pentru outlieri

# =============================================================================
# OUTPUT FORMATS
# =============================================================================
DECIMAL_PRECISION = 4
TABLE_FORMAT = 'markdown'  # sau 'latex' dacă folosești LaTeX

# =============================================================================
# PLOT SETTINGS (pentru toate notebook-urile)
# =============================================================================
def setup_plot_style():
    """Configurează stilul pentru grafice (apelat în fiecare notebook când e nevoie)"""
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    sns.set_theme(style='whitegrid', palette='muted')
    plt.rcParams.update({
        'figure.figsize': (12, 6),
        'figure.dpi': 120,
        'font.size': 10
    })

# Pandas display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1200)
pd.set_option('display.max_colwidth', 100)

# =============================================================================
# FUNCȚII UTILITARE 
# =============================================================================

def calculate_caps_ratio(text: str) -> float:
    """
    Calculează proporția de cuvinte ALL CAPS.
    
    Args:
        text: Textul de analizat
        
    Returns:
        Proporția de cuvinte scrise cu majuscule (0.0 - 1.0)
    """
    if pd.isna(text) or not isinstance(text, str) or len(text.strip()) == 0:
        return 0.0
    words = text.split()
    if len(words) == 0:
        return 0.0
    caps_words = sum(1 for w in words if w.isupper() and len(w) > 1)
    return caps_words / len(words)


def count_aggressive_punctuation(text: str) -> int:
    """
    Numără semnele de punctuație 'agresive' (!, ?).
    
    Args:
        text: Textul de analizat
        
    Returns:
        Numărul de semne de punctuație agresive
    """
    if pd.isna(text) or not isinstance(text, str):
        return 0
    return len(re.findall(r'[!?]+', text))


def calculate_text_length(text: str) -> int:
    """
    Calculează lungimea textului în caractere.
    
    Args:
        text: Textul de analizat
        
    Returns:
        Lungimea în caractere
    """
    if pd.isna(text) or not isinstance(text, str):
        return 0
    return len(text.strip())


def calculate_word_count(text: str) -> int:
    """
    Calculează numărul de cuvinte.
    
    Args:
        text: Textul de analizat
        
    Returns:
        Numărul de cuvinte
    """
    if pd.isna(text) or not isinstance(text, str):
        return 0
    return len(text.strip().split())


# =============================================================================
# FUNCȚIE PENTRU REMOVE STOPWORDS (pentru BERTopic)
# =============================================================================

def remove_stopwords_romanian(text: str, stopwords_set: set = None) -> str:
    """
    Remove stopwords din text românesc.
    
    Args:
        text: Textul de procesat
        stopwords_set: Set de stopwords (opțional, folosește default dacă None)
        
    Returns:
        Text fără stopwords
    """
    if stopwords_set is None:
        stopwords_set = ROMANIAN_STOPWORDS
    
    if pd.isna(text) or not isinstance(text, str):
        return ''
    
    words = text.lower().split()
    filtered_words = [w for w in words if w not in stopwords_set and len(w) > 2]
    
    return ' '.join(filtered_words)


print("=" * 70)
print("✅ CONFIGURARE GLOBALĂ ÎNCĂRCATĂ CU SUCCES")
print("=" * 70)