import openai
import os

from dotenv import load_dotenv, find_dotenv

from declare_client import dec_to_basic_nl

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.getenv('OPENAI_API_KEY')


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def test_completion():
    test = ("""
        Existence2[Admission NC]
        Chain Response[Admission NC, Release B]
        Chain Response[Admission NC, Release A]
        Chain Precedence[IV Liquid, Admission NC]
        Chain Response[ER Registration, ER Triage]
        Chain Precedence[Release A, Return ER]
        Chain Precedence[ER Sepsis Triage, IV Antibiotics]
        Chain Response[ER Sepsis Triage, IV Antibiotics]
        Chain Precedence[Admission IC, Admission NC]
        Chain Precedence[IV Antibiotics, Admission NC]
        Chain Precedence[Admission NC, Release B]
        Chain Response[Admission IC, Admission NC]
        Chain Response[LacticAcid, Leucocytes]
        Chain Precedence[ER Registration, ER Triage]
    """)

    text = dec_to_basic_nl(test)

    print(text)

    prompt = f"""
    Your task is to generate a short summary of a declarative process specification. 
    The input text consists in a series of short sentences that specify each of the restrictions of the model.
    Perform referring expression generation and combine the following sentences into a better written text, 
    don't use lists or enumerations, write a rich and clear text. 
    ```{text}```
    """

    response = get_completion(prompt)
    print("\n")
    print(response)
