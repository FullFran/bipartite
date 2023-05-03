from pymongo import MongoClient
from nltk.corpus import stopwords

# Conexion a la base de datos
client = MongoClient('localhost', 27017)
db = client.caobanutresa_repeat_nouns_emojis_adjectives

# Se obtiene el vocabulario
vocab = db.tweets_words.distinct('word')

# Se obtienen todos los usuarios
users = list(db.tweets_users.find({},{'text_emojis_nouns':1, 'id':1, 'emojis':1, '_id': 0}))

# Arreglo con las palabras a remover
remove_words = []
with open('remove_words.txt', encoding="utf8") as f:
    for line in f:
        remove_word = line.replace('\n', '')
        remove_words.append(remove_word)
print("remove_words:", remove_words)
print("len(remove_words):", len(remove_words))
print()

# Arreglo con las cadenas de caracteres a remover
remove_chars = []
with open('remove_chars.txt', encoding="utf8") as f:
    for line in f:
        remove_char = line.replace('\n', '')
        remove_chars.append(remove_char)
print("remove_chars:", remove_chars)
print("len(remove_chars):", len(remove_chars))
print()

# Total de palabras encontradas en la base de datos
total_words = len(vocab)
print('total palabras vocabulario:', total_words)
print('total usuarios:', len(users))

# Variables usadas para controlar el numero de palabras removidas
word_count = 1
word_count_percent = 0
# Arreglo de enlaces
edges = []

# Se recorren los usuarios y las palabras que han usado ('text_emojis_nouns')
# Se realiza la respectiva limpieza y se agregan al arreglo de enlaces
count = 0
for user in users:
    if 'text_emojis_nouns' in user:
        ramain_emojis = []
        if 'emojis' in user:
            ramain_emojis = user['emojis']
        text_emojis_nouns_lower = list(map(lambda x:x.lower(),user['text_emojis_nouns']))
        for word in text_emojis_nouns_lower:
            word_lower = word.lower()
            add_word_flag = True
            if (word_lower in stopwords.words('spanish')) or (word_lower in stopwords.words('english')) or (word_lower in stopwords.words('portuguese')) or (len(word_lower) < 3 and word_lower not in ramain_emojis):
                # print(word_lower)
                add_word_flag = False
                count += 1
            if word_lower in remove_words:
                # print("word_lower:", word_lower)
                add_word_flag = False
                count += 1
            for remove_char in remove_chars:
                if remove_char in word_lower:
                    # print(word_lower)
                    add_word_flag = False
                    count +=1
            if word_lower.startswith("@"):
                add_word_flag = False
                count += 1
            if add_word_flag:
                edges.append((user['id'],word_lower))
print("count:", count)
print(len(edges))

# Se guardan los enlaces en un archivo de texto
edges_file = open('edges_file_total_network_weights_undirected.txt', 'w')

print('source\ttarget\ttype', file=edges_file)

for k, v in sorted(edges, key=lambda x: x[1]):
    print(k+'\t'+v+'\tUndirected', file=edges_file)
print(len(edges))