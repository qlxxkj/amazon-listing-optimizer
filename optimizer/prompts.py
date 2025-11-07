##############################################################
#
#  V3.0 (提示词字符数始终)
#
##############################################################


PROMPTS = {
    "en": """Optimize Amazon listing.
Rules:
1. Output JSON only with optimized_title, optimized_features (list), optimized_description.
2. Title ≤200 chars; 5 features ≤500 chars each, start with keyword.
3. Description 1000–2000 chars, clear, persuasive.
4. Remove brand names, extreme words, and promotional claims.""",

    "ja": """Amazon商品ページ最適化ルール:
1. JSON形式で出力: optimized_title, optimized_features（5つ）, optimized_description。
2. タイトル200文字以内、各特徴500文字以内。
3. 商品説明1000〜2000文字。
4. ブランド名・誇張表現・広告文句は禁止。""",

    "fr": """Optimisation de fiche produit Amazon.
1. Sortie en JSON : optimized_title, optimized_features (5), optimized_description.
2. Titre ≤200 caractères; description 1000–2000 caractères.
3. Supprime les marques et les mots extrêmes.""",

    "de": """Amazon-Listing optimieren.
1. Ausgabe im JSON-Format: optimized_title, optimized_features (5), optimized_description.
2. Titel ≤200 Zeichen, Beschreibung 1000–2000 Zeichen.
3. Marken- und Werbewörter entfernen.""",

    "it": """Ottimizzazione scheda Amazon.
1. Restituisci JSON con optimized_title, optimized_features (5), optimized_description.
2. Titolo ≤200 caratteri, descrizione 1000–2000.
3. Rimuovi marchi e parole estreme.""",

    "es": """Optimiza ficha de Amazon.
1. Salida JSON: optimized_title, optimized_features (5), optimized_description.
2. Título ≤200 caracteres, descripción 1000–2000.
3. Elimina marcas y palabras extremas."""
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
