##############################################################
#
#  V3.0 (提示词字符数始终)
#
##############################################################


PROMPTS = {"en":"""Role: Amazon Listings Optimization Expert
Task: Output optimized listings based on input listings.
Rules:
1. Only output JSON data containing `optimized_title`, `optimized_features`, `optimized_description`, and `search_keywords`.
2. Title: ≤ 200 characters; 5 product features, each ≤ 500 characters, starting with a keyword.
3. Product Description: 1000-2000 characters, clear and persuasive.
4. Search Keywords: ≤ 500 characters, separated by commas.
5. Absolutely no brand names or promotional terms; extreme terms can be replaced with synonyms.""",

    "ja": """役割: Amazon リスティング最適化エキスパート
タスク: 入力されたリスティング情報に基づいて、最適化されたリスティング情報を出力します。
ルール:
1. `optimized_title`、`optimized_features`、`optimized_description`、`search_keywords` を含む JSON データのみを出力します。
2. タイトル: 200文字以内。商品特徴を5つ、それぞれ500文字以内で、キーワードで始まります。
3. 商品の説明: 1000～2000文字で、明確かつ説得力のある内容にします。
4. 検索キーワード: 500文字以内で、カンマで区切ります。
5. ブランド名やプロモーション用語は一切使用しないでください。極端な用語は同義語に置き換えることができます。""",

    "fr": """Rôle: Expert en optimisation des fiches produits Amazon
Tâche: Générer des fiches produits optimisées à partir des fiches d'entrée.
Règles:
1. Générer uniquement des données JSON contenant les champs `optimized_title`, `optimized_features`, `optimized_description` et `search_keywords`.
2. Titre: ≤ 200 caractères; 5 caractéristiques du produit, chacune ≤ 500 caractères, commençant par un mot-clé.
3. Description du produit: 1000 à 2000 caractères, claire et percutante.
4. Mots-clés de recherche: ≤ 500 caractères, séparés par des virgules.
5. Aucun nom de marque ni terme promotionnel; les termes trop spécifiques peuvent être remplacés par des synonymes.""",

    "de": """Rolle: Experte für Amazon-Produktlisting-Optimierung
Aufgabe: Optimierte Produktlistings basierend auf den Eingabelistings erstellen.
Regeln:
1. Nur JSON-Daten ausgeben, die `optimized_title`, `optimized_features`, `optimized_description` und `search_keywords` enthalten.
2. Titel: ≤ 200 Zeichen; 5 Produktmerkmale, jeweils ≤ 500 Zeichen, beginnend mit einem Keyword.
3. Produktbeschreibung: 1000–2000 Zeichen, klar und überzeugend.
4. Keywords: ≤ 500 Zeichen, durch Kommas getrennt.
5. Keine Markennamen oder Werbebegriffe; extreme Begriffe können durch Synonyme ersetzt werden.""",

    "it": """Ruolo: Esperto di ottimizzazione delle inserzioni Amazon
Attività: Generare inserzioni ottimizzate in base alle inserzioni di input.
Regole:
1. Generare solo dati JSON contenenti `optimized_title`, `optimized_features`, `optimized_description` e `search_keywords`.
2. Titolo: ≤ 200 caratteri; 5 caratteristiche del prodotto, ciascuna ≤ 500 caratteri, che inizino con una parola chiave.
3. Descrizione del prodotto: 1000-2000 caratteri, chiara e persuasiva.
4. Parole chiave di ricerca: ≤ 500 caratteri, separati da virgole.
5. Assolutamente nessun nome di marca o termine promozionale; i termini estremi possono essere sostituiti con sinonimi.""",

    "es": """Rol: Experto en Optimización de Listados de Amazon
Tarea: Generar listados optimizados a partir de los listados de entrada.
Reglas: 1. Generar únicamente datos JSON que contengan `optimized_title`, `optimized_features`, `optimized_description` y `search_keywords`.
2. Título: ≤ 200 caracteres; 5 características del producto, cada una de ≤ 500 caracteres, comenzando con una palabra clave.
3. Descripción del producto: 1000-2000 caracteres, clara y persuasiva.
4. Palabras clave de búsqueda: ≤ 500 caracteres, separadas por comas.
5. No se permiten nombres de marca ni términos promocionales; los términos extremos pueden reemplazarse por sinónimos."""
}

##############################################################
#
#  V2.0 (提示词精简)
#
##############################################################
#
# 针对不同语言的 Prompt 模板 (确保键与DOMAIN_TO_LANG的值匹配)
#
# PROMPTS = {
#     "en": "Amazon listing optimization. Input: {input} Output JSON with title≤200, 5 bullet points(≤500 chars, start with keyword:), description 1000-1500 chars. Preserve key info, no brand names.",
#     "fr": "Optimisation fiche Amazon. Entrée: {input} Sortie JSON: titre≤200, 5 puces(≤500 car, mot-clé:), description 1000-1500 car. Conserver infos clés, pas de marques.",
#     "ja": "Amazonリスティング最適化。入力: {input} 出力JSON: タイトル≤200文字, 5箇条書き(≤500文字, キーワード:), 説明文1000-1500文字。主要情報保持, ブランド名不可。",
#     "de": "Amazon Listing Optimierung. Eingabe: {input} Ausgabe JSON: Titel≤200 Zeichen, 5 Bulletpoints(≤500 Zeichen, Keyword:), Beschreibung 1000-1500 Zeichen. Wichtige Infos behalten, keine Markennamen.",
#     "it": "Ottimizzazione listing Amazon. Input: {input} Output JSON: titolo≤200 caratteri, 5 punti(≤500 car, parola chiave:), descrizione 1000-1500 car. Mantieni info chiave, no marche.",
#     "es": "Optimización anuncio Amazon. Entrada: {input} Salida JSON: título≤200 caracteres, 5 viñetas(≤500 car, palabra clave:), descripción 1000-1500 car. Conservar info clave, sin marcas."
# }

##############################################################
#
#  V1.0 (提示词较多)
#
##############################################################
#
# 针对不同语言的 Prompt 模板 (确保键与DOMAIN_TO_LANG的值匹配)
# PROMPTS = {
#     "en": '''
# You are an Amazon listing optimizer.
# Input: Original listing data (title, features, description)
# Output: JSON with fields: {{"title":..., "bullets": [...], "description": ...}}
# Rules:
# - Titles should be no longer than 200 characters, naturally embedding high-frequency keywords.
# - Generate five bullet points that are concise, readable, and include reasons to buy. (Each bullet point should be no more than 500 characters. Each bullet point should begin with a keyword, followed by a ":", and no punctuation should be used at the end of each bullet point.)
# - Product descriptions should be no fewer than 1000 characters and no more than 1500 characters.
# - Preserve existing key information.
# - Output should be pure JSON.
# - Brand names are not allowed.
# - Extreme keywords (e.g., "high," "improved," "high quality," "perfect," etc.) are not allowed; synonyms can be used instead.
# - Output language should be consistent with the input language.
# Input data:
# {input}
# ''',
# "fr":'''
# Vous optimisez vos fiches Amazon.
# Entrée : Données de la fiche originale (titre, prix, caractéristiques, description, catégorie)
# Sortie : JSON avec les champs : {{"title":..., "bullets": [...], "description": ..., "notes": ...}}
# Règles :
# - Les titres ne doivent pas dépasser 200 caractères et intégrer naturellement les mots-clés fréquents.
# - Générez cinq puces concises, lisibles et expliquant les raisons d'achat. (Chaque puce ne doit pas dépasser 500 caractères. Chaque puce doit commencer par un mot-clé suivi d'un « : », et aucune ponctuation ne doit être utilisée à la fin de chaque puce.)
# - Les descriptions de produits ne doivent pas dépasser 1 000 caractères.
# - Conservez les informations clés existantes.
# - Le résultat doit être au format JSON pur.
# - Les noms de marque ne sont pas autorisés.
# Les mots-clés extrêmes (par exemple, « élevé », « amélioré », « haute qualité », « parfait », etc.) ne sont pas autorisés ; des synonymes peuvent être utilisés.

# La langue de sortie doit être cohérente avec la langue d'entrée.
# Données d'entrée :
# {input}
# ''',
#     "ja": '''
# あなたはAmazon商品リスティングの最適化担当者です。
# 入力: 元のリスティングデータ（title, price, features, description, category）
# 出力: JSON フィールド: {{"title":..., "bullets": [...], "description": ..., "notes": ...}}
# 要件:
# - タイトルは200文字以内とし、高頻度キーワードを自然に埋め込むようにしてください。
# - 簡潔で読みやすく、購入理由を盛り込んだ箇条書きを5つ作成してください。（各箇条書きは500文字以内としてください。各箇条書きはキーワードで始まり、その後に「：」を付け、末尾に句読点は使用しないでください。）
# - 製品の説明は1000文字以上1500文字以内としてください。
# - 既存の主要情報は保持してください。
# - 出力は純粋なJSON形式としてください。
# - ブランド名は使用しないでください。
# - 極端なキーワード（例：「高」「改良」「高品質」「完璧」など）は使用しないでください。代わりに同義語を使用できます。
# - 出力言語は入力言語と一致する必要があります。
# 入力データ:
# {input}
# ''',
#     "de": '''
# Du bist ein Optimierer für Amazon-Listings.
# Eingabe: Original-Listing-Daten (title, price, features, description, category)
# Ausgabe: JSON Felder: {{"title":..., "bullets": [...], "description": ..., "notes": ...}}
# Regeln:
# - Titel max. 200 Zeichen
# - 5 Bullet Points, max. 200 Zeichen, mit Kaufargumenten
# - Produktbeschreibung mind. 1000 Zeichen
# - Ursprüngliche Infos beibehalten
# Eingabedaten:
# {input}
# ''',
# "it": '''
# Sei un ottimizzatore di inserzioni Amazon.
# Input: Dati originali dell'inserzione (titolo, prezzo, caratteristiche, descrizione, categoria)
# Output: JSON con campi: {{"title":..., "bullets": [...], "description": ..., "notes": ...}}
# Regole:
# - I titoli non devono superare i 200 caratteri, incorporando naturalmente parole chiave ad alta frequenza.
# - Genera cinque punti elenco concisi, leggibili e che includano i motivi per l'acquisto. (Ogni punto elenco non deve superare i 500 caratteri. Ogni punto elenco deve iniziare con una parola chiave, seguita da ":", e non deve essere utilizzata alcuna punteggiatura alla fine di ogni punto elenco.)
# - Le descrizioni dei prodotti non devono essere inferiori a 1000 caratteri e non superiori a 1500 caratteri.
# - Mantieni le informazioni chiave esistenti.
# - L'output deve essere JSON puro.
# - I nomi dei marchi non sono ammessi. - Non sono ammesse parole chiave estreme (ad esempio, "alto", "migliorato", "alta qualità", "perfetto", ecc.); è possibile utilizzare sinonimi.
# - La lingua di output deve essere coerente con la lingua di input.
# Dati di input:
# {input}
# ''',
# "es":'''
# Eres un optimizador de anuncios de Amazon.
# Entrada: Datos originales del anuncio (título, precio, características, descripción, categoría).
# Salida: JSON con los campos: {{"title":..., "bullets": [...], "description": ..., "notes": ...}}.
# Reglas:
# - Los títulos no deben tener más de 200 caracteres, incorporando palabras clave de alta frecuencia de forma natural.
# - Genera cinco viñetas concisas, legibles y que incluyan razones para comprar. (Cada viñeta no debe tener más de 500 caracteres. Cada viñeta debe comenzar con una palabra clave, seguida de un ":", y no se debe usar puntuación al final de cada viñeta).
# - Las descripciones de los productos no deben tener menos de 1000 caracteres ni más de 1500.
# - Conserva la información clave existente.
# - La salida debe ser JSON puro.
# - No se permiten nombres de marca. - No se permiten palabras clave extremas (p. ej., "alto", "mejorado", "alta calidad", "perfecto", etc.); se pueden usar sinónimos.
# - El idioma de salida debe ser coherente con el idioma de entrada.
# Datos de entrada:
# {input}
# '''
# }
