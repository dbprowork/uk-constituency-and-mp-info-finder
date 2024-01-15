# UK Constituency and MP Information Finder

#### Project for CS50 Introduction to Programming with Python

#### Description: A program which allows the user to get information about UK constituencies and Members of Parliament (MPs)

#### Background:

The UK government provides a number of APIs relating to its constituencies (geographical areas which are represented in parliament), Members of Parliament (the elected representatives of a constituency in the House of Commons) and Lords (party-sponsored permanent members of the House of Lords).

The APIs are available as part of the [UK Parliament Developer Hub](https://members-api.parliament.uk/index.html).

This program uses the following APIs:

- https://members-api.parliament.uk/api/Location/Constituency/Search
- https://members-api.parliament.uk/api/Members/{mp_id}

#### Aim:

To create a program which allows the user to search for a constituency by name and get the following information about that consituency:

- ID number
- Current Member of Parliament (MP)
- The polical party which currently controls (holds the seat of) the constituency

The program should then, if requested, provide the following information about the selected constituency's MP:

- MP ID number
- A list of the MP's focuses (policy areas that they are interested in), if any

#### Design choices:

The program uses Object Oriented Programming (OOP), due to:

- Common attributes:

    For each enquiry about a constituency, the program would need to provide the same three bits of information each time; ID, MP name and party name.

    For each enquiry about an MP, the program would need to provide the same three bits of information each time; MP ID, MP focus and the MP's last election result.

    It made sense that a class could be created which would contain those attributes on instantiation.

- Processes:

    For each enquiry, the program would need to get the API, select the required bits of information and provide it to the user in a readable format.

    It made sense that a class could achieve this neatly using a few associated methods.

- Style:

    Using classes would allow for neater, more contained code.

#### Classes - Constituency:

Constituency objects are instantiated with a user-input search term. It gets the relevant API and creates a dictionary using Json. A for loop iterates through the dictionary's key-value pairs which match the search term and adds the values to an options list.

If the options list only has one item, the c_confirm method is used to clarify that the item is correct. If the options list has more than one item, the c_refine method is used to output the list and prompt the user to input a number corresponding to each item. Once the correct item is confirmed/selected the relevant method will return an index number for the item.

The c_prep method uses the dictionary created at instantiation to set five attributes:

- The confirmed constituency name
- The constituency ID number
- The constituency MP
- The constituency MPs ID number
- The name of the party which holds the constituency's seat

#### Classes - MP:

MP objects are instantiated using the MP name and MP ID taken from the constituency object. It gets the relevant API and creates three dictionaries:

- self.contact_dict, which holds the MPs contact details
- self.focus_dict, which holds information on the policy interests held by the MP
- self.ler_dict, which holds information on the last election result for the MP; whether they won or retained the seat.

Like the c_prep method for the Constituency class, m_prep used the created dictionaries to set the relevant attributes.

#### Functions - c_input_check

The c_input_function is used to make sure that the initial user-input search term is valid. It will reprompt if the search contains numbers or special characters, exit if there are no search results or pass the search to the relevant Constituency method (c_confirm or c_refine) to confirm or clarify the search.

#### Functions - c_out

The c_out functions returns information based on the object's attributes using f strings. The user requests information using a number from one to three. If the user does not enter a number, or enters a number outside the options given, the function will return a message to the user and they will be reprompted in the main function.

#### Functions - m_out

The m_out function acts the same as the c_out function, but for the MP class.
