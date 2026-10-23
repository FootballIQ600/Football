
import pandas as pd
import requests
from io import BytesIO
from pathlib import Path

# Save the CSV in the same folder as this script.
OUTPUT = Path(__file__).resolve().parent / "historical_results.csv"

SEASONS = {
    "2025/26": "2526",
    "2026/27": "2627",
}

LEAGUES = {
    "Premier League": "E0",
    "Championship": "E1",
    "League One": "E2",
    "League Two": "E3",
}


def download_results():
    all_matches = []
    failed_downloads = []

    for season, season_code in SEASONS.items():
        for league, league_code in LEAGUES.items():
            url = (
                "https://www.football-data.co.uk/mmz4281/"
                f"{season_code}/{league_code}.csv"
            )

            print(f"Downloading {league}, {season}...")

            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()

                if not response.content.strip():
                    print("  Download was empty.")
                    failed_downloads.append(f"{league}, {season}")
                    continue

                df = pd.read_csv(
                    BytesIO(response.content),
                    encoding="latin-1",
                    on_bad_lines="skip",
                )

                required = {
                    "Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"
                }

                if not required.issubset(df.columns):
                    print("  Unexpected file format.")
                    failed_downloads.append(f"{league}, {season}")
                    continue

                df["Season"] = season
                df["Competition"] = league
                df["Date"] = pd.to_datetime(
                    df["Date"], dayfirst=True, errors="coerce"
                )
                df["FTHG"] = pd.to_numeric(df["FTHG"], errors="coerce")
                df["FTAG"] = pd.to_numeric(df["FTAG"], errors="coerce")

                df = df.dropna(
                    subset=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"]
                )

                all_matches.append(df)
                print(f"  Imported {len(df)} completed matches.")

            except (requests.RequestException, ValueError) as exc:
                print(f"  Download failed: {exc}")
                failed_downloads.append(f"{league}, {season}")

    # Never replace the existing CSV if any download failed.
    if failed_downloads:
        print("\nSome downloads failed. Existing CSV has been preserved.")
        for item in failed_downloads:
            print(f"- {item}")
        return

    if not all_matches:
        print("\nNo results were downloaded. Existing CSV preserved.")
        return

    results = pd.concat(all_matches, ignore_index=True)

    results = results.sort_values(
        ["Date", "Competition", "HomeTeam"]
    ).reset_index(drop=True)

    results.to_csv(OUTPUT, index=False, date_format="%Y-%m-%d")

    print("\nImport complete!")
    print(f"Total completed matches: {len(results)}")
    print(f"Saved to: {OUTPUT}")


if __name__ == "__main__":
    download_results()
