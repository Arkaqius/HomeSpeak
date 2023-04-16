import json

def load_udt_json(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def convert_udt_to_spacy(udt_data: list) -> list:
    spacy_data = []
    for item in udt_data:
        text = item["document"]
        entitiesUDT = item["annotation"]['entities']

        entities = []
        for entity in entitiesUDT:
            start = entity["start"]
            end = entity["end"]
            label = entity["label"]
            entities.append((start, end, label))

        spacy_data.append((text, {"entities": entities}))
    return spacy_data

def save_spacy_json(spacy_data: list, file_path: str):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(spacy_data, file, ensure_ascii=False, indent=2)

def main():
    udt_file_path = "./src/NER/modelTraining/rawDataSet/data.json"
    spacy_file_path = "./src/NER/modelTraining/rawDataSet/spacy_training_data.json"

    udt_data = load_udt_json(udt_file_path)
    spacy_data = convert_udt_to_spacy(udt_data['samples'])
    save_spacy_json(spacy_data, spacy_file_path)

if __name__ == "__main__":
    main()
