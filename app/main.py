from database import connect_database


def main():

    print("================================")
    print("🚀 GemRadar AI Starting...")
    print("================================")

    print("✓ Python Environment OK")

    db = connect_database()

    if db:
        print("✓ Database Ready")
        db.close()

    print()
    print("System Ready 🚀")


if __name__ == "__main__":
    main()