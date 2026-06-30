def label_activity(df):

    df = df.copy()

    df["label"] = (
        df["activity"] < 1000
    ).astype(int)

    return df