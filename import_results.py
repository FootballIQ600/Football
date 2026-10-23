
import pandas as pd
import requests
from io import BytesIO
from pathlib import Path

# Football-data.co.uk season codes
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

OUTPUT = Path("historical_results.csv")


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
                    print("  No data available yet.")
                    continue

                df = pd.read_csv(
                    BytesIO(response.content),
                    encoding="latin-1",
                    on_bad_lines="skip",
                )

                required = {"Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"}

                if not required.issubset(df.columns):
                    print("  File does not contain the expected columns.")
                    failed_downloads.append(f"{league}, {season}")
                    continue

                df["Season"] = season
                df["Competition"] = league
                df["Date"] = pd.to_datetime(
                    df["Date"], dayfirst=True, errors="coerce"
                )
                df["FTHG"] = pd.to_numeric(df["FTHG"], errors="coerce")
                df["FTAG"] = pd.to_numeric(df["FTAG"], errors="coerce")

                # Keep completed matches with valid full-time scores.
                df = df.dropna(
                    subset=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"]
                )

                all_matches.append(df)
                print(f"  Imported {len(df)} completed matches.")

            except (requests.RequestException, ValueError) as exc:
                print(f"  Download failed: {exc}")
                failed_downloads.append(f"{league}, {season}")

    if not all_matches:
        print("\nNo historical results were downloaded.")
        print("Check your internet connection and try again.")
        return

    results = pd.concat(all_matches, ignore_index=True)

    results = results.sort_values(
        ["Date", "Competition", "HomeTeam"]
    ).reset_index(drop=True)

    results.to_csv(OUTPUT, index=False, date_format="%Y-%m-%d")

    print("\nImport complete!")
    print(f"Total completed matches: {len(results)}")
    print(f"Date range: {results['Date'].min().date()} "
          f"to {results['Date'].max().date()}")
    print(f"Saved to: {OUTPUT.resolve()}")

    print("\nMatches by competition and season:")
    print(
        results.groupby(["Season", "Competition"])
        .size()
        .to_string()
    )

    if failed_downloads:
        print("\nDownloads to check:")
        for item in failed_downloads:
            print(f"- {item}")

    print(
        "\nNote: a season may have no data yet or be incomplete. "
        "Check the source before treating missing matches as errors."
    )


if __name__ == "__main__":
    download_results()
