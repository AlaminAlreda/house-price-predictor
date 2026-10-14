import pandas as pd
import re

# --------------------------------------------------
# 1. Load the raw dataset
# --------------------------------------------------

INPUT_PATH = "data/matrix.xlsx"
OUTPUT_PATH = "data/cleaned_houses.xlsx"

df = pd.read_excel(INPUT_PATH)

print("Original shape:", df.shape)


# --------------------------------------------------
# 2. Drop Total Area
# --------------------------------------------------

df = df.drop(columns=["Total Area"])


# --------------------------------------------------
# 3. Drop rows with missing values
# --------------------------------------------------

df = df.dropna().copy()

print("Shape after dropping missing rows:", df.shape)


# --------------------------------------------------
# 4. Convert Area into Living Area + Additional Area
# --------------------------------------------------

def split_area(area):
    """
    Convert values such as:
        '143 + 25 m²' -> (143, 25)
        '123 m²'      -> (123, 0)
    """

    # Remove 'm²' and surrounding whitespace
    area = area.replace("m²", "").strip()

    # Case: "143 + 25"
    if "+" in area:
        parts = area.split("+")

        living_area = float(parts[0].strip())
        additional_area = float(parts[1].strip())

        return living_area, additional_area

    # Case: "123"
    else:
        living_area = float(area)
        additional_area = 0

        return living_area, additional_area


# Apply the function to the Area column
df[["Living Area", "Additional Area"]] = (
    df["Area"]
    .apply(split_area)
    .apply(pd.Series)
)


# --------------------------------------------------
# 5. Remove the original Area column
# --------------------------------------------------

df = df.drop(columns=["Area"])


# --------------------------------------------------
# 6. Convert Rooms to numeric
# --------------------------------------------------

# Example:
# "7 rum" -> 7
# "4 rum" -> 4

df["Rooms"] = (
    df["Rooms"]
    .str.replace("rum", "", regex=False)
    .str.strip()
    .astype(float)
)


# --------------------------------------------------
# 7. Convert Land Area to numeric
# --------------------------------------------------

# Example:
# "2 303 m² tomt" -> 2303

df["Land Area"] = (
    df["Land Area"]
    .str.replace("\xa0", "", regex=False)  # remove non-breaking spaces
    .str.replace(" ", "", regex=False)     # remove normal spaces
    .str.replace("mÂ²", "", regex=False)   # remove corrupted m²
    .str.replace("m²", "", regex=False)    # remove normal m²
    .str.replace("tomt", "", regex=False)
    .str.replace(",",".")
    .str.strip()
    .astype(float)
)


# --------------------------------------------------
# 8. Convert Price to numeric
# --------------------------------------------------

# Example:
# "3 005 000 kr" -> 3005000

df["Price"] = (
    df["Price"]
    .str.replace("kr", "", regex=False)
    .str.replace("\xa0", "", regex=False)
    .str.replace(" ", "", regex=False)
    .str.strip()
    .astype(float)
)


# --------------------------------------------------
# 9. Convert Date to datetime
# --------------------------------------------------

# Swedish month names need to be translated before
# pandas can reliably convert them.

swedish_months = {
    "januari": "January",
    "februari": "February",
    "mars": "March",
    "april": "April",
    "maj": "May",
    "juni": "June",
    "juli": "July",
    "augusti": "August",
    "september": "September",
    "oktober": "October",
    "november": "November",
    "december": "December"
}

for swedish, english in swedish_months.items():
    df["Date"] = df["Date"].str.replace(
        swedish,
        english,
        case=False,
        regex=False
    )

df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d %B %Y"
)


# --------------------------------------------------
# 10. Check the resulting dataset
# --------------------------------------------------

print("\nFinal dataset information:")
print(df.info())

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isna().sum())


# --------------------------------------------------
# 11. Save the cleaned dataset
# --------------------------------------------------

df.to_excel(OUTPUT_PATH, index=False)

print(f"\nCleaned dataset saved to: {OUTPUT_PATH}")