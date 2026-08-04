from app.services.pseudonymization.pseudonymizer import Pseudonymizer

pseudo = Pseudonymizer()

print(pseudo.pseudonymize("John Smith", "PATIENT"))
print(pseudo.pseudonymize("Michael Brown", "PATIENT"))
print(pseudo.pseudonymize("John Smith", "PATIENT"))
print(pseudo.pseudonymize("john@gmail.com", "EMAIL"))
print(pseudo.pseudonymize("08123456789", "PHONE"))

print()

print(pseudo.get_mapping())