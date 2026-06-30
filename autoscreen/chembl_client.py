import requests
import pandas as pd


def fetch_bioactivities(target_id):

    url = (
        f"https://www.ebi.ac.uk/chembl/api/data/activity"
        f"?target_chembl_id={target_id}"
        f"&limit=1000"
        f"&format=json"
    )

    response = requests.get(url)

    activities = response.json()["activities"]
    
    rows = []

    for act in activities:

        smiles = act.get("canonical_smiles")
        value = act.get("standard_value")
        units = act.get("standard_units")

        if smiles and value:

            rows.append({
                "smiles": smiles,
                "activity": float(value),
                "units": units
            })

    return pd.DataFrame(rows), target_id
if __name__ == "__main__":
    target_id = "CHEMBL1824"
    df,_ = fetch_bioactivities(target_id)
    print(df.head())