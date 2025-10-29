import os
import pandas as pd
import json

# -------- Initial Settings --------
BASE_DIR = "/home/dehghani/Projects/countries"
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

COUNTRIES_FILE = os.path.join(BASE_DIR, "csv/countries.csv")
STATES_FILE = os.path.join(BASE_DIR, "csv/states.csv")
CITIES_FILE = os.path.join(BASE_DIR, "csv/cities.csv")

country_ids: list[int] = [103]

# -------- read files --------
print("Reading CSV files...")
countries_df = pd.read_csv(COUNTRIES_FILE)
states_df = pd.read_csv(STATES_FILE)
cities_df = pd.read_csv(CITIES_FILE)

# -------- filter countries --------
for country_id in country_ids:
    country = countries_df[countries_df["id"] == country_id]
    if country.empty:
        print(f"❌ Country with ID {country_id} not found in countries.csv")
        continue

    country_name = country.iloc[0]["name"]
    print(f"\n🌍 Processing country: {country_name} (ID={country_id})")

    country_dir = os.path.join(OUTPUT_DIR, str(country_id))
    os.makedirs(country_dir, exist_ok=True)

    # -------- filter states --------
    country_states = states_df[states_df["country_id"] == country_id]

    if country_states.empty:
        print(f"⚠️ No states found for country {country_name}")
        continue

    print(f"  Found {len(country_states)} states.")

    # -------- find cities for each state --------
    for _, state in country_states.iterrows():
        state_id = int(state["id"])
        state_name = state["name"]

        state_dir = os.path.join(country_dir, str(state_id))
        os.makedirs(state_dir, exist_ok=True)

        state_cities = cities_df[cities_df["state_id"] == state_id]

        if state_cities.empty:
            print(f"    ⚠️ No cities found for state: {state_name}")
            continue

        # --- Replace NaN with None so json.dump writes null ---
        state_cities = state_cities.where(pd.notnull(state_cities), None)

        print(f"    🏙️ {state_name}: {len(state_cities)} cities found")

        # convert to dict
        cities_json = state_cities.to_dict(orient="records")

        # save to json file
        json_path = os.path.join(state_dir, "cities.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(cities_json, f, ensure_ascii=False, indent=2)

print("\n✅ Done! Check the 'output/' folder.")
