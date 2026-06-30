from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
import joblib

from autoscreen.chembl_client import fetch_bioactivities
from autoscreen.preprocessing import label_activity
from autoscreen.fingerprints import smiles_to_fp
from autoscreen.model import train_model
from autoscreen.persistence import save_model, load_model
from autoscreen.drugcentral import load_library 


BASE_DIR = Path(__file__).resolve().parent


class ScreeningPipeline:

    def train(self, target_id: str):

        print(f"Training model for {target_id}")

        # Fetch ChEMBL data

        df, target_id = fetch_bioactivities(target_id)

        # Clean data
        df = label_activity(df)
        df = df.drop_duplicates(subset=["smiles"])

        # Build dataset

        X = []
        y = []

        for _, row in df.iterrows():

            fp = smiles_to_fp(row["smiles"])

            if fp is not None:
                X.append(fp)
                y.append(row["label"])

        # Train model
       
        result = train_model(X, y)

        # Save 
        save_model(
            target_id=target_id,
            model=result["model"],
            
            metadata={
                "created_at": datetime.now().isoformat(),
                "samples": len(X),
                "algorithm": "RandomForest",
                "fingerprint": "Morgan",
                "radius": 2,
                "bits": 2048,
            },
        )

        return result
    
    # Screening function

    def screen(self,target_id,
               output_path=None,
    limit=1000,
    top_n=20):
        
        print("Loading model...")
        model = load_model(target_id)["model"]

        print("Loading compound library...")
        df = load_library(limit)

        output_path=target_id+"_screening_results.csv" if output_path is None else output_path

        X_screen = []
        valid_rows = []

        for idx, row in df.iterrows():

            fp = smiles_to_fp(row["smiles"])

            if fp is not None:
                X_screen.append(fp)
                valid_rows.append(idx)

        X_screen = np.array(X_screen)

        print(f"Screening {len(X_screen)} compounds...")

        probabilities = model.predict_proba(X_screen)[:, 1]

        predictions = model.predict(X_screen)

        results = df.loc[valid_rows].copy()

        results["probability"] = probabilities
        results["prediction"] = predictions

        results = results.sort_values(
            by="probability",
            ascending=False
        )

        results.to_csv(output_path, index=False)

        print(f"Saved results to {output_path}")

        return results.head(top_n)
