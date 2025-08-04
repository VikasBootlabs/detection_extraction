import ollama
def generate_response(text) -> str:
    response = ollama.generate(
    model='llama3:8b',
    prompt=f"""{text}\n\n"
                "You are an expert. Understand the given relevant text and extract the following details:\n"
                "- Driving Licence Number\n"
                "- Full Name\n"
                "- Date of Birth\n"
                "- Address\n"
                "- Date of Issue (DOI)\n"
                "- Date of Expiry (DOE)\n"
                "- City\n"
                "- Pincode\n"
                "- State\n"
                "- Blood Group\n\n"
                "Return the result in JSON format."""
    ,
    options={
        "temperature": 0
    },
    format='json',
    )


    return response['response']
