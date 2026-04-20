import ollama, json
from csv_processing import load_settings

def merchant_hint(description):
    settings = load_settings()
    for merchant, categories in settings["local_merchants_categories"].items():
        if merchant in description.lower():
            merchant_hint = f"""
            This transaction appears to be from {merchant} which typically covers: {categories}
            Use the description and the amount to determine the most accurate category
            """
            break
    else:
        merchant_hint = ""
        
    return merchant_hint
            

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
        - Electronics & Appliances
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
        
    prompt = system_prompt + description + merchant_hint(description)

    response = ollama.chat(
        model = "llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    
    result = json.loads(response["message"]["content"])
    return result["category"]