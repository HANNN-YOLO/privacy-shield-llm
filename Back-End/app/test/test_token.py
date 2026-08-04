from app.services.pseudonymization.token_generator import TokenGenerator

generator = TokenGenerator()

print(generator.generate("PATIENT"))
print(generator.generate("PATIENT"))
print(generator.generate("PATIENT"))

print(generator.generate("DOCTOR"))
print(generator.generate("DOCTOR"))

print(generator.generate("EMAIL"))

print(generator.show_counters())