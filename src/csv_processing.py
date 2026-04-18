import os , json ,pandas as pd

def load_settings():
    with open("config/settings.json", "r") as f:
        data = json.load(f)
    return data

def csv_data_extraction(file_path, bank):
    df = pd.read_csv(file_path)
    settings = load_settings()
    
    if bank in settings["bank_mappings"]:
        mapping = settings["bank_mappings"][bank]
    
    else:
        print(df.columns.tolist())
        user_date = input("Which column provides the date: ")
        user_description = input("Which column provides the description: ")
        user_amount_type = input("Amount type - enter 'single' for one amount column, or 'split' for separate Money: ")
        
        if user_amount_type == "single":
            user_amount = input("Which column provides the amount: ")
            mapping = {
                "date": user_date,
                "description": user_description,
                "amount_type": "single",
                "amount": user_amount
            }
        else:
            user_money_in = input("Which column provides the money received: ")
            user_money_out = input("Which column provides the money payed: ")
            mapping = {
                "date": user_date,
                "description": user_description,
                "amount_type": "split",
                "money_in": user_money_in,
                "money_out": user_money_out
            }
            
        settings["bank_mappings"][bank] = mapping
        with open("config/settings.json", "w") as f:
            json.dump(settings, f, indent=4)
            
    if mapping["amount_type"] == "split":
        df[mapping["money_in"]] = df[mapping["money_in"]].fillna(0)
        df[mapping["money_out"]] = df[mapping["money_out"]].fillna(0)
        
    result = []
    for _, row in df.iterrows():
        if mapping["amount_type"] == "single":
            amount = row[mapping["amount"]]
        else:
            amount = row[mapping["money_in"]] - row[mapping["money_out"]]
        result.append({
            "date": row[mapping["date"]],
            "description": row[mapping["description"]],
            "amount": amount
        })
    return result