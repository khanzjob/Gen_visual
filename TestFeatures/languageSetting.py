class LanguageSetting:
    def __init__(self):
        self.language = "english"  # Default language

    def set_language(self, language):
        self.language = language

    def get_language(self):
        return self.language


# language_setting = LanguageSetting()

# # Set the language to Luganda
# language_setting.set_language("Luganda")

# # Get the current language
# current_language = language_setting.get_language()
# # print(current_language)  # Outputs: Luganda