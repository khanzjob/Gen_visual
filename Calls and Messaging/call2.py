import random

# Sample contact database (you can replace this with a real database)
contacts = {
    'Alice': '+1234567890',
    'Bob': '+9876543210',
}

# Text-to-speech function (you may need to install the 'gTTS' library)
def speak(text):
    print("Assistant:", text)

# Function to add a new contact
def add_contact(name, phone):
    contacts[name] = phone
    speak(f"Contact {name} added successfully.")

# Function to search for a contact
def search_contact(name):
    if name in contacts:
        speak(f"The phone number for {name} is {contacts[name]}.")
    else:
        speak(f"Sorry, {name} was not found in your contacts.")

# Function to update a contact's phone number
def update_contact(name, new_phone):
    if name in contacts:
        contacts[name] = new_phone
        speak(f"Contact {name}'s phone number updated successfully.")
    else:
        speak(f"Sorry, {name} was not found in your contacts.")

# Function to delete a contact
def delete_contact(name):
    if name in contacts:
        del contacts[name]
        speak(f"Contact {name} deleted successfully.")
    else:
        speak(f"Sorry, {name} was not found in your contacts.")

# Main loop for user interaction
while True:
    user_input = input("You: ").lower()

    if "exit" in user_input or "quit" in user_input:
        speak("Goodbye!")
        break

    if "add contact" in user_input:
        speak("Sure, please provide the name and phone number.")
        contact_name = input("You: ")
        contact_phone = input("You: ")
        add_contact(contact_name, contact_phone)

    elif "search contact" in user_input:
        speak("Who are you looking for?")
        contact_to_find = input("You: ")
        search_contact(contact_to_find)

    elif "update contact" in user_input:
        speak("Whose contact information would you like to update?")
        contact_to_update = input("You: ")
        new_phone = input("You: Enter the new phone number: ")
        update_contact(contact_to_update, new_phone)

    elif "delete contact" in user_input:
        speak("Whose contact would you like to delete?")
        contact_to_delete = input("You: ")
        delete_contact(contact_to_delete)

    else:
        responses = [
            "I'm sorry, I didn't understand that.",
            "I'm not sure what you mean.",
            "Could you please repeat that?",
        ]
        speak(random.choice(responses))
