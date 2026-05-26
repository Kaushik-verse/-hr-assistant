import os
import subprocess


def main():
    print("Starting AI HR Assistant...")
    # Initialize the database
    from database.db_setup import init_db
    init_db()

    # Run Streamlit App
    ui_path = os.path.join("ui", "app.py")
    subprocess.run(["streamlit", "run", ui_path])


if __name__ == "__main__":
    main()