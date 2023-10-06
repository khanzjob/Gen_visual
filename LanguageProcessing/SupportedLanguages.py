
import pandas as pd
import streamlit as st

def generate_language_table():
    
    # Comprehensive list of world languages and their ISO codes
    world_languages_data = {
    "Language": [
        "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Assamese", "Aymara", "Azerbaijani",
        "Bambara", "Basque", "Belarusian", "Bengali", "Bhojpuri", "Bosnian", "Bulgarian", "Catalan", 
        "Cebuano", "Chinese (Simplified)", "Chinese (Traditional)", "Corsican", "Croatian", "Czech", 
        "Danish", "Dhivehi", "Dogri", "Dutch", "English", "Esperanto", "Estonian", "Ewe", "Filipino", 
        "Finnish", "French", "Frisian", "Galician", "Georgian", "German", "Greek", "Guarani", "Gujarati",
        "Haitian Creole", "Hausa", "Hawaiian", "Hebrew", "Hindi", "Hmong", "Hungarian", "Icelandic", 
        "Igbo", "Ilocano", "Indonesian", "Irish", "Italian", "Japanese", "Javanese", "Kannada", "Kazakh",
        "Khmer", "Kinyarwanda", "Konkani", "Korean", "Krio", "Kurdish (Kurmanji)", "Kurdish (Sorani)", 
        "Kyrgyz", "Lao", "Latin", "Latvian", "Lingala", "Lithuanian", "Luganda", "Luxembourgish", 
        "Macedonian", "Maithili", "Malagasy", "Malay", "Malayalam", "Maltese", "Maori", "Marathi", 
        "Meiteilon (Manipuri)", "Mizo", "Mongolian", "Myanmar (Burmese)", "Nepali", "Norwegian", 
        "Odia (Oriya)", "Oromo", "Pashto", "Persian", "Polish", "Portuguese", "Punjabi", "Quechua", 
        "Romanian", "Russian", "Samoan", "Sanskrit", "Scots Gaelic", "Sepedi", "Serbian", "Sesotho", 
        "Shona", "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali", "Spanish", "Sundanese", "Swahili",
        "Swedish", "Tajik", "Tamil", "Tatar", "Telugu", "Thai", "Tigrinya", "Tsonga", "Turkish", "Turkmen",
        "Twi", "Ukrainian", "Urdu", "Uyghur", "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yiddish", "Yoruba", "Zulu"
    ],

    "ISO-639 code": [
        "af", "sq", "am", "ar", "hy", "as", "ay", "az", "bm", "eu", "be", "bn", "bho", "bs", "bg", "ca", 
        "ceb", "zh-CN", "zh-TW", "co", "hr", "cs", "da", "dv", "doi", "nl", "en", "eo", "et", "ee", "fil", 
        "fi", "fr", "fy", "gl", "ka", "de", "el", "gn", "gu", "ht", "ha", "haw", "he", "hi", "hmn", "hu", 
        "is", "ig", "ilo", "id", "ga", "it", "ja", "jv", "kn", "kk", "km", "rw", "gom", "ko", "kri", "ku", 
        "ckb", "ky", "lo", "la", "lv", "ln", "lt", "lg", "lb", "mk", "mai", "mg", "ms", "ml", "mt", "mi", 
        "mr", "mni-Mtei", "lus", "mn", "my", "ne", "no", "or", "om", "ps", "fa", "pl", "pt", "pa", "qu", 
        "ro", "ru", "sm", "sa", "gd", "nso", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", 
        "sw", "sv", "tg", "ta", "tt", "te", "th", "ti", "ts", "tr", "tk", "ak", "uk", "ur", "ug", "uz", 
        "vi", "cy", "xh", "yi", "yo", "zu"
    ]
    }

    # Local languages
    local_languages = ["Luganda", "Runyankole", "Acholi", "Lugbara", "Ateso"]

    # Create a DataFrame for world languages
    df_world_languages = pd.DataFrame(world_languages_data)

    # Add columns for local languages with all "Yes" values (assuming all translations are supported)
    for local_language in local_languages:
        df_world_languages[local_language] = "Yes"
        
    return df_world_languages

def DisplayLanguages():
    st.title("Languages Supported for Translation")
    st.write("Below is a table showing all world languages, their ISO-639 codes, and support for translation to the local languages:")
        
    # Generate the language table
    df = generate_language_table()
        
        # Display the table in Streamlit
    st.table(df)
    

    
if __name__ == "__main__":
    DisplayLanguages()
        
    
   