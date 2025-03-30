from ARTsScrap import *

def get_arts():
    i = 1
    while i <= 4:
        files = os.listdir(f'data/json{i}')
        if not files:
            return None
        for file in files:
            arts = []
            try:
                with open(f'data/json{i}/{file}', "r", encoding="utf-8") as json_file:
                    print(f"Reading data from {file}")
                    data = json.load(json_file)
                    for art in data:
                        if art.get('Data').get('Situation') != 'REGISTRADA':
                            continue
                        art_number = art.get('Data').get('ART')
                        address = art.get('Data').get('Address')
                        start_date = art.get('Data').get('Start Date')
                        payment_date = art.get('Data').get('Payment Date')
                        title = art.get('Titles')
                        if title == None:
                            title = 'Not informed'
                        else:
                            title = title[0]
                        if address == None:
                            address = 'Not informed'
                        if start_date == None:
                            start_date = 'Not informed'
                        if payment_date == None or payment_date == ' / / ':
                            payment_date = 'Not informed'
                        art = {
                            'ART': art_number,
                            'Address': address,
                            'Start Date': start_date,
                            'Payment Date': payment_date,
                            'Title': title
                        }
                        arts.append(art)
            except json.JSONDecodeError:
                print(f"Error reading {file}")
                return None
            save_data_to_csv(arts)
            print(f"Data from {file} saved")
        i += 1
    print("All data saved")
    return arts

def main():
    get_arts()

if __name__ == '__main__':
    main()