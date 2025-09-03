
from scripts.faker_qc import Faker
import random
import json

# Create Faker instances for English and French Canadian locales
fake_en = Faker('en_CA')
fake_fr = Faker('fr_CA')

def generate_person():
    # Randomly choose between French and English name
    if random.choice(['fr', 'en']) == 'fr':
        fake = fake_fr
        language = 'French'
    else:
        fake = fake_en
        language = 'English'
    person = {
        'language': language,
        'name': fake.name(),
        'address': fake.address().replace('\n', ', '),
        'email': fake.email(),
        'phone_number': fake.phone_number(),
        'ssn': fake.ssn(),
        'dob': fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat()
    }
    return person

if __name__ == "__main__":
    users = [generate_person() for _ in range(10)]
    with open("quebec_users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)