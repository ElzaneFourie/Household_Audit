import ollama, json

#def merchant_hint(description):
    

def categorise_transaction(description, amount=None):
    system_prompt = """
        You are a financial transaction categoriser for a household budget app.

        Your job is to categorise bank transaction descriptions into one of the following categories:
        - Groceries
        - Dining & Takeaways
        - Transport & Fuel
        - Utilities
        - Rent & Housing
        - Medical & Health
        - Insurance
        - Entertainment & Subscriptions
        - Education
        - Clothing & Personal Care
        - Savings & Investments
        - Debt & Loans
        - Income
        - Other

        Rules:
        - Always respond with ONLY a JSON object in this exact format: {"category": "Category Name"}
        - Use "Other" if you are unsure
        - Never explain your reasoning, never add extra text
        - Transactions are South African — apply local merchant knowledge when categorising

        Transaction description to categorise:
        """
        
    prompt = system_prompt + description #+ merchant_hint(description) #This will return the text processed from settings with merchant hint

    response = ollama.chat(
        model = "llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    
    result = json.loads(response["message"]["content"])
    return result["category"]

print(categorise_transaction("Purch Checkers Sixty"))