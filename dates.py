from datetime import date

def main():
    today = date.today()
    today_str = today.isoformat()
    print(today)
    print(type(today_str))
    pass

def get_dateinfo(start, year, month, day):
    pass

if __name__ == "__main__":
    main()