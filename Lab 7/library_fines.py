def parse_member_id(member_id):
    if not isinstance(member_id, str):
        return None
    parts = member_id.split('-')
    if len(parts) != 2:
        return None
    member_type, number = parts[0].strip(), parts[1].strip()
    if not member_type:
        return None
    try:
        number = int(number)
    except ValueError:
        return None
    return member_type.upper(), number


def total_fine(days_csv):
    if not isinstance(days_csv, str):
        return None
    if not days_csv.strip():
        return 0
    fine = 0
    for token in days_csv.split(','):
        token = token.strip()
        if not token:
            return None
        try:
            days = int(token)
        except ValueError:
            return None
        if days > 14:
            fine += (days - 14) * 2
    return fine


def shelf_code(title):
    if not isinstance(title, str):
        return None
    words = title.split()
    if len(words) < 2:
        return None
    return (words[0][0] + words[1][0]).upper()


def main():
    print("==== Running parse_member_id ====")
    result = parse_member_id(input("Enter a member ID (e.g. STU-1023): "))
    if result is None:
        print("Invalid member ID. Expected the form TYPE-NUMBER, e.g. STU-1023.")
    else:
        print("Member Type and Number:", result)

    print("\n==== Running total_fine ====")
    result = total_fine(input("Enter days kept for each book as CSV (e.g. 10,20,30): "))
    if result is None:
        print("Invalid input. Expected comma-separated whole numbers, e.g. 10,20,30.")
    else:
        print("Total Fine:", result)

    print("\n==== Running shelf_code ====")
    result = shelf_code(input("Enter a book title with at least two words: "))
    if result is None:
        print("Invalid title. Please enter a title with at least two words.")
    else:
        print("Shelf Code:", result)


if __name__ == "__main__":
    main()
