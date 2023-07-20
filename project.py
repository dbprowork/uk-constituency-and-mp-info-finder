import requests
import json
import sys


class Constituency:
    """Get, store and prepare constituency information."""
    def __init__(self, search):
        """Instantiate and get API based on user input."""
        self.search = search
        self.rsp = requests.get(f"https://members-api.parliament.uk/api/Location/Constituency/Search?searchText={search}&skip=0&take=20")
        self.dict = self.rsp.json()
        self.options = []
        for i in range(0, len(self.dict['items'])):
            self.options.append(self.dict['items'][i]['value']['name'])


    def c_confirm(self):
        """Confirm search."""
        conf = input(f"You have selected {self.options[0]}. Is this correct (Y/N)? ").lower()
        if conf == "y":
            self.ind = 0
        else:
            sys.exit("Unable to get correct result with the information given. Restart to try again.")


    def c_refine(self):
        """Refine search."""
        print(f"Did you mean:")
        for i in range(len(self.options)):
            print(f"{i+1} {self.options[i]}")
        try:
            select = int(input("Enter number: "))
        except ValueError:
            print("Choice must be a number.")
            select = int(input("Enter number: "))
        self.ind = select-1


    def c_prep(self):
        """Prepare data for output."""
        self.name = self.dict['items'][self.ind]['value']['name']
        self.id = self.dict['items'][self.ind]['value']['id']
        self.mp = self.dict['items'][self.ind]['value']['currentRepresentation']['member']['value']['nameDisplayAs']
        self.mp_id = self.dict['items'][self.ind]['value']['currentRepresentation']['member']['value']['id']
        self.party = self.dict['items'][self.ind]['value']['currentRepresentation']['member']['value']['latestParty']['name']


class MP:
    """Get, store and present MP information."""
    def __init__(self, mp_name, mp_id):
        """Instantiate and get API using info from Constituency class (MP name and MP ID)."""
        self.mp_name = mp_name
        self.contact_rsp = requests.get(f"https://members-api.parliament.uk/api/Members/{mp_id}/Contact")
        self.contact_dict = self.contact_rsp.json()
        self.focus_rsp = requests.get(f"https://members-api.parliament.uk/api/Members/{mp_id}/Focus")
        self.focus_dict = self.focus_rsp.json()
        self.ler_rsp = requests.get(f"https://members-api.parliament.uk/api/Members/{mp_id}/LatestElectionResult")
        self.ler_dict = self.ler_rsp.json()


    def m_prep(self):
        """Prepare data for output."""
        self.mp_contact = self.contact_dict['value'][0]['email']
        self.ler = self.ler_dict['value']['result']
        self.focus = [self.focus_dict['value'][i]['focus'] for i in range(len(self.focus_dict['value']))]


def c_input_check(constituency):
    c_check_cont = 0
    while c_check_cont == 0:
        if not constituency.search.isalpha():
            sys.exit(f"Search cannot include numbers or special characters. Restart to try again.")
        elif len(constituency.options) == 1:
            constituency.c_confirm()
        elif len(constituency.options) > 1:
            constituency.c_refine()
        elif len(constituency.options) == 0:
            sys.exit(f"{constituency.search.title()} not recognised. Restart to try again.")
        try:
            constituency.c_prep()
            c_check_cont = 1
        except IndexError:
            print("Option not available.")
            constituency.c_refine()


def c_out(constituency, choice):
    """Present data to user."""
    if not choice.isdigit():
        return "Choice must be a number."
    elif int(choice) < 1 or int(choice) > 3:
        return "Option not available."
    else:
        if choice == "1":
            return f"The constituency ID for {constituency.name} is {constituency.id}."
        elif choice == "2":
            return f"The MP for {constituency.name} is {constituency.mp}."
        elif choice == "3":
            return f"{constituency.name} is held by {constituency.party}."


def m_out(mp, choice):
    """Present data to user."""
    if not choice.isdigit():
        return "Choice must be a number."
    elif int(choice) < 1 or int(choice) > 3:
        return "Option not available."
    else:
        if choice == "1":
            return f"The email address for {mp.mp_name} is {mp.mp_contact.rstrip()}."
        elif choice == "2":
            if not mp.focus:
                return f"{mp.mp_name} has no no listed focus."
            else:
                if isinstance(mp.focus, str):
                    return f"{mp.mp_name}'s registered focus is: {mp.focus}"
                elif isinstance(mp.focus, list):
                    return mp.focus
        elif choice == "3":
            return f"The last election result for {mp.mp_name} was {mp.ler}."


def main():
    cont_list = ["y", "yes", "n", "no"]

    # Create Consituency object.
    constituency = Constituency(input("Enter constituency name: ").lower())
    # Check input.
    c_input_check(constituency)
    # Loop for constituency information.
    cont_list = ["y", "yes", "n", "no"]
    c_cont = "y"
    while c_cont == "y" or c_cont == "yes":
        c_choice = input("Would you like:\n1 Constituency ID\n2 Constituency MP\n3 Constituency Party\nEnter number: ")
        print(c_out(constituency, c_choice))
        c_cont = input("Continue (Y/N)? ").lower()
        while c_cont not in cont_list:
            print("Try again.")
            c_cont = input("Continue (Y/N)? ").lower()


    # Create MP object if requested.
    transfer = input(f"Would you like further information about {constituency.mp}, the MP for {constituency.name} (Y/N)? ").lower()
    while transfer not in cont_list:
        print("Try again.")
        transfer = input(f"Would you like further information about {constituency.mp}, the MP for {constituency.name} (Y/N)? ").lower()
    if transfer == "y" or transfer == "yes":
        mp = MP(constituency.mp, constituency.mp_id)
        mp.m_prep()
        # Loop for mp information.
        m_cont = "y"
        while m_cont == "y" or m_cont == "yes":
            m_choice = input("Would you like:\n1 MP Contact Details\n2 MP Focus\n3 MP Last Election Result\nEnter number: ")
            if m_out(mp, m_choice) == mp.focus:
                print(f"{mp.mp_name}'s registered focus is: ")
                for i in range(0, len(mp.focus)):
                    print(f"- {''.join(mp.focus[i])}")
            else:
                print(m_out(mp, m_choice))
            m_cont = input("Continue (Y/N)? ").lower()
            while m_cont not in cont_list:
                print("Try again.")
                m_cont = input("Continue (Y/N)? ").lower()


    sys.exit("Thank you. Restart to make another enquiry.")


if __name__ == "__main__":
    main()
