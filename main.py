from bs4 import BeautifulSoup, element
import requests
import csv
import sys

def main():
    verbs = {}
    if len(sys.argv) != 2:
        sys.exit("Usage: python `filename.csv`")
    filename = sys.argv[1]

    print(f"YOURSELF CREATE A FILE CALLED `{filename}`")
    while True:
        try:
            input_verbs = input("VERB: ")
            infinitive = verbs_infinitive(input_verbs)
            verbs[input_verbs] = {"infinitive": infinitive}
            
            verb_dict = parce_html_table_to_dict(f"{input_verbs}", get_verb_html(input_verbs))
            verbs[input_verbs].update(verb_dict)

        except EOFError:
            break
        except ValueError:
            print("WRONG NAME VAR")

    if verbs == {}:
        sys.exit("\nNO VALID VARS ENTERED")

    dict_to_csv(verbs=verbs, filename=filename)

def get_verb_html(verb:str, time:str="Prezent") -> element.Tag:
    url = f"https://www.conjugare.ro/romana.php?conjugare={verb}"

    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

    conjunctiv_prezent_tag = soup.find('b', string=time)

    if conjunctiv_prezent_tag is None:
        raise ValueError("wrong variable")
    
    return conjunctiv_prezent_tag.parent

def parce_html_table_to_dict(verb:str, html:element.Tag) -> dict[str: dict[str]:str]:
    
    divs = html.find_all("div", class_ ="cont_conj")
    
    return  {i.i.string: i.contents[1].strip() for i in divs}


def verbs_infinitive(verb:str) -> str:
    return get_verb_html(verb, "Infinitiv").find("div", class_="cont_conj").string

def dict_to_csv(verbs:dict, filename:str) -> None:
    has_header = False

    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row != []:
                has_header = True
            break
    

    with open(filename, "a") as file:
    
        fieldnames = list(list(verbs.values())[0].keys())

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if not has_header:
            writer.writeheader()

        for verb in verbs:
            writer.writerow(verbs[verb])
            

if __name__ == "__main__":
    main()