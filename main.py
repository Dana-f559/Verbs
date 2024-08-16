from bs4 import BeautifulSoup, element
import requests
import csv
import sys
import tabulate

def main():
    
    if len(sys.argv) == 3 and sys.argv[2] == "-d":
        
        display_verbs_tabulate(filename=sys.argv[1])
        sys.exit()

    elif len(sys.argv) == 3 and sys.argv[2] == "-s":
        verb = input("Enter verb you are searching for (in infinitive): ")
        if if_verb_in_verbs(verb, sys.argv[1]):
            verbs = get_csv_file_all_verbs(filename=sys.argv[1])
            print(tabulate_one_verb(verbs=verbs, verb=verb))
        else:
            print("No")
        sys.exit()

    if len(sys.argv) != 2:
        sys.exit("Ussage: python `filename.csv`")

    filename = sys.argv[1]

    print(f"YOURSELF CREATE A FILE CALLED `{filename}`")
    
    verbs = get_verbs(sys.argv[1])
    
    dict_to_csv(verbs=verbs, filename=filename)

def get_verb_html(verb:str, time:str="Prezent") -> element.Tag:
    url = f"https://www.conjugare.ro/romana.php?conjugare={verb}"

    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

    conjunctiv_prezent_tag = soup.find('b', string=time)

    if conjunctiv_prezent_tag is None:
        raise ValueError("wrong variable")
    
    return conjunctiv_prezent_tag.parent

def get_verbs(filename)->dict:
    verbs = {}
    while True:
        try:
            input_verbs = input("VERB: ")
            if if_verb_in_verbs(input_verbs,filename):
                print("Already in the file")
                continue
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

    return verbs

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

def get_csv_file_all_verbs(filename:str)->dict:
    verbs = {}

    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            verbs.update({row["infinitive"]:row})

    return verbs

def dictVerbs_into_list(verbs:dict, n:int) -> list:
    verbs_list = []

    for i in range(0, len(verbs.keys()), n):
        t = {}
        for verb in list(verbs.keys())[i : i+n-1]:
            t.update({verb: verbs[verb]})
        
        verbs_list.append(t)

    return verbs_list

def display_verbs_tabulate(filename:str) -> None:
    verbs = get_csv_file_all_verbs(filename=filename)

    verbs_list = dictVerbs_into_list(verbs, 10)

    for verb in verbs_list:

        infinitive_keys = list(verb.keys())
        table = []

        for entry in verb[infinitive_keys[0]]:
            row = [entry]
            for i in range(len(infinitive_keys)):
                row.append(verb[infinitive_keys[i]][entry])
            table.append(row)

        headers = [""] + infinitive_keys

        tabulated_data = tabulate.tabulate(table, headers=headers,  tablefmt="grid")
        print(tabulated_data, end="\n\n")

def if_verb_in_verbs(verb:str, filename:str)->bool:
    verbs = get_csv_file_all_verbs(filename=filename)
    verbs_items = [item for value_list in verbs.values() for item in value_list.values()]
    
    return True if verb in verbs.keys() else True if verb in verbs_items else False


def tabulate_one_verb(verb:str, verbs:dict)->None:
    try:
        verb_table = [[v, verbs[verb][v]] for v in verbs[verb]]
    except KeyError:
        return "Variable exists in the file, to see it in a table enter the verb in infinitive"
    return tabulate.tabulate(verb_table, tablefmt="grid")

if __name__ == "__main__":
    main()