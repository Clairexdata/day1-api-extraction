"""
Day 1 - API Data Extraction and Transformation
Squad Python Specialization - Data Engineering

Fill in every function. Keep the signatures; you may add helpers of your own.
"""
from pathlib import Path

import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_PATH = Path("output") / "customers_clean.csv"


def fetch_users(url: str = API_URL, timeout: float = 10.0) -> list[dict]:
    """Retrieve the list of users from the API.

    Must raise or report a clear error for: connection failures, timeouts,
    non-200 status codes and bodies that are not valid JSON.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        users = response.json()
    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"Could not retrieve users: {error}") from error
    except ValueError as error:
        raise RuntimeError("The API response was not valid JSON.") from error

    if not isinstance(users, list):
        raise RuntimeError("Expected the API to return a list of users.")

    return users


def describe_structure(payload) -> None:
    """Print what Python types the payload and one record are made of
    (the top-level container, a record, and each nested value)."""
    if not isinstance(payload, list):
        raise ValueError("Expected a list of records.")

    print(f"Top-level container type: {type(payload).__name__}")
    if payload:
        record = payload[0]
        print(f"Record type: {type(record).__name__}")
        for key, value in record.items():
            print(f"Key '{key}': type {type(value).__name__}")


def extract_core_fields(users: list[dict]) -> list[dict]:
    """Return one small dict per user with id, name, email, city and company name."""
    core_fields = [
        {
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "city": user.get("address", {}).get("city"),
            "company_name": user.get("company", {}).get("name"),
        }
        for user in users
    ]
    return core_fields


def build_structures(users: list[dict]) -> tuple[list, list[tuple], dict]:
    """Return (list_of_names, list_of_(id, email)_tuples, dict_of_id_to_city).

    Use at least one list comprehension and one dict comprehension.
    """
    list_of_names = [user.get("name") for user in users]
    list_of_email_tuples = [(user.get("id"), user.get("email")) for user in users]
    dict_of_id_to_city = {user.get("id"): user.get("address", {}).get("city") for user in users}
    return list_of_names, list_of_email_tuples, dict_of_id_to_city


def flatten_user(user: dict, parent_key: str = "", sep: str = "_") -> dict:
    """Flatten one nested user record into a single-level dict.

    e.g. a nested address -> geo -> lat becomes the key address_geo_lat.
    """
    items = []
    for k, v in user.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_user(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def to_dataframe(flat_users: list[dict]) -> pd.DataFrame:
    """Build a DataFrame with the columns in the expected-output order."""
    expected_columns = [
        "id",
        "name",
        "username",
        "email",
        "address_street",
        "address_suite",
        "address_city",
        "address_zipcode",
        "address_geo_lat",
        "address_geo_lng",
        "phone",
        "website",
        "company_name",
        "company_catchPhrase",
        "company_bs",
    ]
    df = pd.DataFrame(flat_users)
    df = df.reindex(columns=expected_columns)
    return df


def export_csv(df: pd.DataFrame, path: Path = OUTPUT_PATH) -> Path:
    """Write the DataFrame to CSV (creating the folder if needed) and return the path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def main() -> None:
    users = fetch_users()
    describe_structure(users)
    core_users = extract_core_fields(users)
    names, email_tuples, cities = build_structures(users)
    flat_users = [flatten_user(user) for user in users]
    df = to_dataframe(flat_users)
    output_path = export_csv(df)

    print(
        f"Processed {len(users)} users ({len(core_users)} core records, "
        f"{len(names)} names, {len(email_tuples)} email tuples, "
        f"{len(cities)} cities) and saved CSV to {output_path}."
    )


if __name__ == "__main__":
    main()
