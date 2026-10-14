import pandas as pd
import re

INPUT_PATH = "data/cleaned_houses.xlsx"

df = pd.read_excel(INPUT_PATH)


def normalize_location(location):
    if pd.isna(location):
        return location

    location = str(location).lower().strip()

    # 1. Keep only the text before the first comma
    location = location.split(",", maxsplit=1)[0].strip()

    # 2. Remove whitespace around hyphens and slashes
    location = re.sub(r"\s*([-\/])\s*", r"\1", location)

    # 3. Remove "kungälv-" or "kungälv " at the beginning
    location = re.sub(r"^kungälv(?:-| )+", "", location)

    # 4. Keep only the main location for specified prefixes
    main_locations = [
        "ytterby",
        "tjuvkil",
        "romelanda",
        "duvesjön",
        "kode",
        "centralt",
        "kärna",
        "marstrand",
        "aröd",
        "harestad",
        "solberga",
        "rörtången",
        "tega",
        "kovikshamn",
        "ödsmålsmosse",
        "munkegärde",
        "överön",
        "vävra",
        "svartedalen"


    ]

    for main_location in main_locations:
        pattern = rf"^{re.escape(main_location)}(?:$|[\s/-])"
        if re.match(pattern, location):
            return main_location

    return location


df["Location"] = df["Location"].apply(normalize_location)

location_corrections = {
    "lövön-kungälv/marstrand": "marstrand",
    "marstrandsön": "marstrand",
    "ödsmål": "ödsmålsmosse",
    "ödsmåls mosse/rörtången": "ödsmålsmosse",
    "diseröd centrum": "diseröd",
    "kungälvs kommun": "kungälv",
    "övre tega-ytterby": "tega",
    "övre tega": "tega",
    "lycke bremnäs": "lycke",

}

df["Location"] = df["Location"].replace(location_corrections)

print("Number of unique locations:", df["Location"].nunique())
print("\nLocation occurrences:")
print(df["Location"].value_counts().sort_index().to_string())
print((df["Location"].value_counts() ==1).sum())
print(sum(df["Location"].value_counts()))

df.to_excel("data/standard_data.xlsx", index=False)