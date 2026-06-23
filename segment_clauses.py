import fitz
import re

pdf_path = "data/contracts/nda.pdf"

doc = fitz.open(pdf_path)

text = ""

for page in doc:
    text += page.get_text()

pattern = r"\n\s*(\d+)\.\s*\n"

matches = list(re.finditer(pattern, text))

clauses = []

for i in range(len(matches)):
    start = matches[i].start()

    if i < len(matches)-1:
        end = matches[i+1].start()
    else:
        end = len(text)

    clause_text = text[start:end].strip()

    clauses.append(clause_text)

print(f"Total Clauses Found: {len(clauses)}")

for idx, clause in enumerate(clauses):
    print("\n" + "="*50)
    print(f"CLAUSE {idx+1}")
    print("="*50)
    print(clause[:500]) 
