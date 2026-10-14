import pandas as pd

DATA_PATH = "data/matrix.xlsx"


def main():
    df = pd.read_excel(DATA_PATH)

    print("Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nFirst 5 rows:")
    print(df.head())


if __name__ == "__main__":
    main()