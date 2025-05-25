import streamlit as st
import pandas as pd
from datetime import datetime
import json

st.set_page_config(
    page_title="AI Storytelling",
    page_icon="📚",
    layout="wide"
)

# Language selection
languages = {
    "English": "en",
    "हिंदी": "hi",
    "தமிழ்": "ta",
    "తెలుగు": "te",
    "മലയാളം": "ml",
    "বাংলা": "bn"
}

# Sample stories - In production, this would come from an AI model
stories = {
    "Taj Mahal": {
        "en": "The Taj Mahal, a symbol of eternal love, was built by Emperor Shah Jahan in memory of his beloved wife Mumtaz Mahal. This architectural marvel took 22 years to complete, involving 20,000 artisans from across the world.",
        "hi": "ताज महल, शाश्वत प्रेम का प्रतीक, सम्राट शाहजहाँ ने अपनी प्यारी पत्नी मुमताज महल की याद में बनवाया था। इस वास्तुशिल्प चमत्कार को पूरा होने में 22 साल लगे, जिसमें दुनिया भर के 20,000 कारीगरों ने भाग लिया।",
        "ta": "தாஜ் மகால், நித்திய காதலின் சின்னம், பேரரசர் ஷாஜஹான் தனது அன்பு மனைவி மும்தாஜ் மகாலின் நினைவாக கட்டிய கட்டிடம். இந்த கட்டிடக்கலை அதிசயத்தை கட்ட 22 ஆண்டுகள் ஆனது, உலகம் முழுவதிலும் இருந்து 20,000 கைவினைஞர்கள் ஈடுபட்டனர்.",
        "te": "తాజ్ మహల్, శాశ్వత ప్రేమకు చిహ్నం, చక్రవర్తి షాజహాన్ తన ప్రియమైన భార్య ముమ్తాజ్ మహల్ జ్ఞాపకార్థం నిర్మించాడు. ఈ నిర్మాణ అద్భుతాన్ని పూర్తి చేయడానికి 22 సంవత్సరాలు పట్టింది, ప్రపంచం నలుమూలల నుండి 20,000 చేతి వృత్తి కళాకారులు పాల్గొన్నారు.",
        "ml": "താജ് മഹൽ, നിത്യ സ്നേഹത്തിന്റെ പ്രതീകം, ചക്രവർത്തി ഷാജഹാൻ തന്റെ പ്രിയപ്പെട്ട ഭാര്യ മുമ്താസ് മഹലിന്റെ ഓർമ്മയ്ക്കായി നിർമ്മിച്ചതാണ്. ഈ വാസ്തുവിദ്യാ അത്ഭുതം പൂർത്തിയാക്കാൻ 22 വർഷങ്ങൾ എടുത്തു, ലോകത്തിന്റെ നാനാഭാഗത്തുനിന്നും 20,000 കരകൗശല വിദഗ്ധർ ഇതിൽ ഏർപ്പെട്ടു.",
        "bn": "তাজমহল, চিরন্তন প্রেমের প্রতীক, সম্রাট শাহজাহান তার প্রিয় স্ত্রী মমতাজ মহলের স্মৃতিতে নির্মাণ করেছিলেন। এই স্থাপত্য বিস্ময়টি সম্পূর্ণ করতে ২২ বছর লেগেছিল, বিশ্বের বিভিন্ন প্রান্ত থেকে ২০,০০০ কারিগর এতে অংশগ্রহণ করেছিলেন।"
    },
    "Red Fort": {
        "en": "The Red Fort, a UNESCO World Heritage Site, served as the main residence of the Mughal Emperors for nearly 200 years. Its red sandstone walls, standing 75 feet high, witnessed the rise and fall of an empire.",
        "hi": "लाल किला, एक यूनेस्को विश्व धरोहर स्थल, लगभग 200 वर्षों तक मुगल सम्राटों का मुख्य निवास था। इसकी 75 फीट ऊंची लाल बलुआ पत्थर की दीवारें एक साम्राज्य के उत्थान और पतन की गवाह हैं।",
        "ta": "சிவப்பு கோட்டை, யுனெஸ்கோ உலக பாரம்பரிய தளம், கிட்டத்தட்ட 200 ஆண்டுகளாக முகலாய பேரரசர்களின் முக்கிய வசிப்பிடமாக இருந்தது. 75 அடி உயரமுள்ள சிவப்பு மணற்கல் சுவர்கள், ஒரு பேரரசின் எழுச்சி மற்றும் வீழ்ச்சியை கண்டன.",
        "te": "రెడ్ ఫోర్ట్, యునెస్కో ప్రపంచ వారసత్వ ప్రదేశం, దాదాపు 200 సంవత్సరాలు మొఘల్ చక్రవర్తుల ప్రధాన నివాసంగా ఉండింది. 75 అడుగుల ఎత్తు ఉన్న ఎరుపు ఇసుకరాయి గోడలు, ఒక సామ్రాజ్యం యొక్క పెరుగుదల మరియు పతనాన్ని చూసినవి.",
        "ml": "റെഡ് ഫോർട്ട്, യുനെസ്കോ ലോക പൈതൃക സ്ഥലം, ഏകദേശം 200 വർഷങ്ങളായി മുഗൾ ചക്രവർത്തിമാരുടെ പ്രധാന വാസസ്ഥലമായിരുന്നു. 75 അടി ഉയരമുള്ള ചുവന്ന മണൽക്കല്ല് മതിലുകൾ, ഒരു സാമ്രാജ്യത്തിന്റെ ഉയർച്ചയും വീഴ്ചയും കണ്ടു.",
        "bn": "লাল কেল্লা, একটি ইউনেস্কো বিশ্ব ঐতিহ্য স্থান, প্রায় ২০০ বছর ধরে মুঘল সম্রাটদের প্রধান বাসস্থান ছিল। এর ৭৫ ফুট উঁচু লাল বেলেপাথরের দেওয়ালগুলি একটি সাম্রাজ্যের উত্থান ও পতনের সাক্ষী।"
    }
}

st.title("AI Storytelling & Multilingual Experience 📚")

# Language selector
selected_language = st.sidebar.selectbox(
    "Select Language / भाषा चुनें",
    list(languages.keys())
)

# Story selector
selected_story = st.selectbox(
    "Select a Heritage Site",
    list(stories.keys())
)

# Display story in selected language
st.subheader(selected_story)
st.write(stories[selected_story][languages[selected_language]])

# Interactive elements
st.subheader("Interactive Experience")
col1, col2 = st.columns(2)

with col1:
    if st.button("Generate Historical Context"):
        st.write("AI would generate additional historical context here")
    
    if st.button("Show Related Artifacts"):
        st.write("AI would display related artifacts and their stories")

with col2:
    if st.button("Listen to Story"):
        st.write("Audio narration would play here")
    
    if st.button("View 3D Model"):
        st.write("3D model viewer would appear here")

# Additional features
st.subheader("Additional Features")
with st.expander("Cultural Significance"):
    st.write("AI would provide detailed cultural significance of the site")
    
with st.expander("Local Legends"):
    st.write("AI would share local legends and folklore")
    
with st.expander("Visitor Experiences"):
    st.write("AI would show curated visitor experiences and stories")

# Language statistics
st.sidebar.subheader("Language Statistics")
st.sidebar.metric("Available Languages", "6")
st.sidebar.metric("Stories Translated", "12")
st.sidebar.metric("Audio Narrations", "6") 