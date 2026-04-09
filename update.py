import argparse
import sqlite3

import httpx
from tqdm import tqdm

DB_NAME = "downloads_history.db"


def init_db():
    """Initializes the SQLite database and creates the history table."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS release_history (
                repo TEXT PRIMARY KEY,
                last_version TEXT,
                last_filename TEXT
            )
        """)
        conn.commit()


def get_local_record(repo_path):
    """Fetches the stored record for a specific repository."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT last_version, last_filename FROM release_history WHERE repo = ?",
            (repo_path,),
        )
        return cursor.fetchone()


def update_local_record(repo_path, version, filename):
    """Updates or inserts the repository record after a successful download."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO release_history (repo, last_version, last_filename)
            VALUES (?, ?, ?)
        """,
            (repo_path, version, filename),
        )
        conn.commit()


def download_latest_release(repo_path, file_extension, force=False):
    init_db()
    api_url = f"https://api.github.com/repos/{repo_path}/releases"

    # Check local record
    record = get_local_record(repo_path)

    with httpx.Client(follow_redirects=True) as client:
        print(f"Checking updates for {repo_path}...")

        try:
            response = client.get(api_url)
            response.raise_for_status()
            releases = response.json()

            if not releases:
                print("No releases found.")
                return

            latest_release = releases[0]
            version = latest_release.get("tag_name")
            assets = latest_release.get("assets", [])

            asset = next(
                (a for a in assets if a["name"].endswith(file_extension)), None
            )

            if not asset:
                print(f"No asset found with extension: {file_extension}")
                return

            filename = asset["name"]
            download_url = asset["browser_download_url"]
            total_size = asset.get("size", 0)

            # Logic for forced download or database check
            if not force and record and record[1] == filename:
                print(f"[*] Already up to date: '{filename}' (Version: {version}).")
                return

            if force and record and record[1] == filename:
                print(f"[!] Force flag detected. Re-downloading '{filename}'...")
            else:
                print(f"New version found: {version}")

            print(f"Downloading: {filename}")

            with client.stream("GET", download_url) as r:
                r.raise_for_status()
                content_length = int(r.headers.get("Content-Length", total_size))

                with tqdm(
                    total=content_length,
                    unit="B",
                    unit_scale=True,
                    desc=filename,
                    colour="red",
                ) as pbar:
                    with open(filename, "wb") as f:
                        for chunk in r.iter_bytes(chunk_size=8192):
                            size = f.write(chunk)
                            pbar.update(size)

            update_local_record(repo_path, version, filename)
            print("Successfully downloaded and database updated.")

        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e.response.status_code}")
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="GitHub Release Downloader with SQLite History"
    )
    parser.add_argument("repo", help="User/Repo (e.g. 'nvm-sh/nvm')")
    parser.add_argument("extension", help="File extension (e.g. '.sh')")

    # Added force flag
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force download even if the file is already recorded in history",
    )

    args = parser.parse_args()
    download_latest_release(args.repo, args.extension, force=args.force)


if __name__ == "__main__":
    main()
