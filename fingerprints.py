from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator
import numpy as np


def smiles_to_fp(smiles):

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None
    
    generator=rdFingerprintGenerator.GetMorganGenerator(2,fpSize=2048)
    fp=generator.GetFingerprint(mol)
    
    arr = np.zeros((2048,))
    Chem.DataStructs.ConvertToNumpyArray(fp, arr)

    return arr
    
if __name__ == "__main__":
    test_smiles = "CC(=O)Nc1ccc(O)cc1"  # Paracetamol
    fingerprint = smiles_to_fp(test_smiles)

    if fingerprint is not None:
        print(f"Fingerprint for {test_smiles}:")
        print(fingerprint)
    else:
        print(f"Invalid SMILES string: {test_smiles}")