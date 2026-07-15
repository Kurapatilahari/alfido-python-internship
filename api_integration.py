"""
Task 2: API Integration & JSON Handling
------------------------------------------
Goal: Learn how Python communicates with external APIs and handles JSON data.

This script demonstrates:
    1. Fetching data using the 'requests' library
    2. Parsing JSON responses
    3. Applying filtering / search logic
    4. Handling API errors (timeouts, bad status codes, connection issues)

Public API used: https://jsonplaceholder.typicode.com (free fake REST API,
no key required, safe for demos).

Author: <Your Name>
"""

import json
import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError, RequestException

BASE_URL = "https://jsonplaceholder.typicode.com"
OUTPUT_FILE = "users_output.json"


def fetch_data(endpoint, timeout=10):
    """
    Fetch JSON data from a given API endpoint.
    Returns parsed JSON (list/dict) on success, or None on failure.
    """
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # raises HTTPError for 4xx/5xx responses
        print(f"[OK] Fetched data from {url} (status {response.status_code})")
        return response.json()

    except ConnectionError:
        print(f"[ERROR] Could not connect to {url}. Check your internet connection.")
    except Timeout:
        print(f"[ERROR] Request to {url} timed out after {timeout}s.")
    except HTTPError as e:
        print(f"[ERROR] HTTP error from {url}: {e}")
    except RequestException as e:
        # Catch-all for any other 'requests' related issue
        print(f"[ERROR] Unexpected request error: {e}")
    except json.JSONDecodeError:
        print(f"[ERROR] Response from {url} was not valid JSON.")

    return None


def filter_users_by_city(users, city_keyword):
    """Return only the users whose address.city contains the given keyword (case-insensitive)."""
    if not users:
        return []
    keyword = city_keyword.lower()
    return [u for u in users if keyword in u.get("address", {}).get("city", "").lower()]


def search_users_by_name(users, name_keyword):
    """Return users whose name contains the given keyword (case-insensitive)."""
    if not users:
        return []
    keyword = name_keyword.lower()
    return [u for u in users if keyword in u.get("name", "").lower()]


def summarize_user(user):
    """Return a short, readable summary line for a user dict."""
    return f"{user['id']:>2} | {user['name']:<20} | {user['email']:<28} | {user['address']['city']}"


def save_json(data, filename):
    """Save Python data as a nicely formatted JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"[OK] Saved output to {filename}")
    except IOError as e:
        print(f"[ERROR] Could not write {filename}: {e}")


def main():
    print("=" * 70)
    print("TASK 2: API INTEGRATION & JSON HANDLING")
    print("=" * 70)

    # 1. Fetch all users from the API
    users = fetch_data("users")
    if users is None:
        print("[FATAL] No data retrieved, exiting.")
        return

    print(f"\nTotal users fetched: {len(users)}")
    print("\n--- All Users ---")
    print(f"{'ID':>2} | {'Name':<20} | {'Email':<28} | City")
    print("-" * 70)
    for u in users:
        print(summarize_user(u))

    # 2. Apply filtering logic: users in cities containing 'south' or similar
    print("\n--- Filter: cities containing 'south' ---")
    filtered = filter_users_by_city(users, "south")
    if filtered:
        for u in filtered:
            print(summarize_user(u))
    else:
        print("No matches found.")

    # 3. Apply search logic: users whose name contains 'a'
    print("\n--- Search: names containing 'a' ---")
    matched = search_users_by_name(users, "a")
    for u in matched:
        print(summarize_user(u))

    # 4. Demonstrate error handling with a deliberately bad endpoint
    print("\n--- Demonstrating error handling (bad endpoint) ---")
    bad_result = fetch_data("this-endpoint-does-not-exist")
    if bad_result is None:
        print("[OK] Error was handled gracefully, script did not crash.")

    # 5. Save the fetched + filtered data to a JSON file
    output = {
        "total_users": len(users),
        "filtered_by_city_south": filtered,
        "searched_by_name_a": matched,
    }
    save_json(output, OUTPUT_FILE)

    print("\n[DONE] API integration task complete.")


if __name__ == "__main__":
    main()
