import random, re, string, os

try:
    import nltk
except:
    os.system('cmd /c "pip install numpy"');
    os.system('cmd /c "pip install nltk"');
    os.system('cmd /c "py -m pip install numpy"');
    os.system('cmd /c "py -m pip install nltk"');
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('popular')
    import nltk
    import numpy
try:
    from textblob import TextBlob
except:
    os.system('cmd /c "pip install textblob"');
    os.system('cmd /c "py -m pip install textblob"');
    from textblob import TextBlob
try:
    import wikipedia
except:
    os.system('cmd /c "pip install wikipedia"');
    os.system('cmd /c "py -m pip install wikipedia"');
    import wikipedia
try:
     from bs4 import BeautifulSoup
except:
    os.system('cmd /c "pip install beautifulsoup4"');
    os.system('cmd /c "py -m pip install beautifulsoup4"');
    from bs4 import BeautifulSoup
try:
    import requests
except:
    os.system('cmd /c "pip install requests"');
    os.system('cmd /c "py -m pip install requests"');
    import requests
try:
    from googlesearch import search
except:
    os.system('cmd /c "pip install googlesearch-python"');
    os.system('cmd /c "py -m pip install googlesearch-python"');
    from googlesearch import search
try:
    import pypiwin32
except:
    os.system('cmd /c "pip install pypiwin32"');
    os.system('cmd /c "py -m pip install pypiwin32"');
    #import pypiwin32
try:
    import pyttsx3
    import win32com.client as wincl
except:
    os.system('cmd /c "pip install pyttsx3"');
    os.system('cmd /c "py -m pip install pyttsx3"');
    import pyttsx3
    import win32com.client as wincl


# Türkçe olan sesli motorun seçilmesi
engine = pyttsx3.init("sapi5")
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\Tolga')
voices = engine.getProperty('voices')
for voice in voices:
    print("Voice:")
    print(" - ID: %s" % voice.id)
    print(" - Name: %s" % voice.name)
    print(" - Languages: %s" % voice.languages)
    print(" - Gender: %s" % voice.gender)
    print(" - Age: %s" % voice.age)

GREETING_INPUTS = ["merhaba", "selam", "hey", "naber", "meraba"]
GREETING_RESPONSES = ["merhaba", "hey", "naber", "meraba"]

def clean_text(text):
    # küçük harfe çevirme
    text = text.lower()
    # noktalama işaretlerini kaldırma
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    # sayıları kaldırma
    text = re.sub('\w*\d\w*', '', text)
    return text

def get_sentiment(text):
    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity
    if sentiment > 0.1:
        return "mutlu"
    elif sentiment < -0.1:
        return "üzgün"
    else:
        return "tarafsız"

def get_wikipedia_summary(topic):
    try:
        return wikipedia.summary(topic, sentences=10)
    except:
        return ""

def search_on_bing(query):
    # Bing arama URL'si ve başlığı
    url = f"https://www.bing.com.tr/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3 tr-TR"}

    # İstek gönderme ve yanıtı alma
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    summary=""
    #b_focusTextLarge b_paractl
    try:
        summary = soup.find("div", {"class": "b_focusTextLarge"}).text
    except:pass
    # İlk sonucun metnini döndürme
    try:
        summary += " \n \n "+soup.find("div", {"class": "b_caption"}).text
    except:pass
    try:
        summary += " \n \n "+soup.find("p", {"class": "b_paractl"}).text
    except:pass
    return summary

def get_emotion(text):
    analysis = TextBlob(text)
    emotion = ""
    for word, tag in analysis.tags:
        if tag == "JJ":
            # sıfatları kullanarak duyguyu belirleme
            if word in ["öfkeli", "sinirli", "kızgın", "çılgın"]:
                emotion = "öfkeli"
            elif word in ["mutlu", "sevinçli", "mutlu", "neşeli", "hoşnut"]:
                emotion = "mutlu"
            elif word in ["korkmuş", "endişeli", "korku içinde", "korkunç", "ürkmüş"]:
                emotion = "korkmuş"
            elif word in ["iğrenmiş", "tiksinti", "iğrenç", "tiksindirici"]:
                emotion = "tiksinme"
            elif word in ["şaşırmış", "şaşkın", "şok"]:
                emotion = "şaşkın"
            elif word in ["üzgün", "hüzünlü", "mutsuz", "morali bozuk", "acıklı"]:
                emotion = "üzgün"
    return emotion

def get_response(emotion, text):
    if emotion == "mutlu":
        responses = ["Güzel haber!", "Ne güzel!", "Harika!", "Muhteşem!"]
    elif emotion == "üzgün":
        responses = ["Bu üzücü.", "Üzgünüm.", "Canın sıkkın olduğunu hissedebiliyorum.", "Bu zor bir durum."]
    elif emotion == "öfkeli":
        responses = ["Sakin ol.", "Nefes al.", "Sana yardımcı olabilirim mi?", "Bu konuda ne yapabilirim?"]
    elif emotion == "korkmuş":
        responses = ["Korktuğun için üzgünüm.", "Korkularını anlıyorum.", "Korkunun üstesinden gelebilirsin."]
    elif emotion == "tiksinme":
        responses = ["Bu gerçekten iğrenç.", "Sana nasıl yardımcı olabilirim?", "Bu konuda ne yapabilirim?", "Bu durumda ne düşünüyorsun?"]
    elif emotion == "şaşkın":
        responses = ["Gerçekten mi?", "Şaşırdım!", "Ben de anlamadım.", "Nasıl oldu bu?"]
    else:
        try:
            summary = wikipedia.summary(text, sentences=5)
            return f"\n    : {summary}"
        except wikipedia.exceptions.DisambiguationError:
            return "Anlayamadım ve farklı anlamlar olabilir, lütfen daha açıklayıcı bir soru sorun."
        except wikipedia.exceptions.PageError:
            pass
        try:
            summary = search_on_bing(text)
            return f"\n     : {summary}"
        except Exception as e:
            return "Bilmiyorum." + str(e)
    return random.choice(responses)

#while True:
#    user_input = str(input("Sen: "))
#    user_input = str(clean_text(user_input))
#    if user_input in GREETING_INPUTS:
#        bot_response = random.choice(GREETING_RESPONSES)
#    else:
#        sentiment = get_sentiment(user_input)
#        emotion = get_emotion(user_input)
#        bot_response = get_response(emotion, user_input)
#    print("Miku: " + bot_response)

while True:
    user_input = str(input("Sen: "))
    user_input = str(clean_text(user_input))
    if user_input in GREETING_INPUTS:
        bot_response = random.choice(GREETING_RESPONSES)
    else:
        sentiment = get_sentiment(user_input)
        emotion = get_emotion(user_input)
        bot_response = get_response(emotion, user_input)
    
    #engine.say(bot_response)
    #engine.runAndWait()
    print("Miku: " + bot_response)