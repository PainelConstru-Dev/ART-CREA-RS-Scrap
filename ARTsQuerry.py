from ARTsScrap import *

def get_arts():
    files = os.listdir('data/json')
    if not files:
        return None
    for file in files:
        arts = []
        try:
            with open(f'data/json/{file}', "r", encoding="utf-8") as json_file:
                print(f"Reading data from {file}")
                data = json.load(json_file)
                for art in data:
                    if art.get('Data').get('Situation') != 'REGISTRADA':
                        continue
                    art_number = art.get('Data').get('ART')
                    address = art.get('Data').get('Address')
                    date = art.get('Data').get('Start Date')
                    if address == None:
                        address = 'Not informed'
                    if date == None:
                        date = 'Not informed'
                    art = {
                        'ART': art_number,
                        'Address': address,
                        'Start Date': date
                    }
                    arts.append(art)
        except json.JSONDecodeError:
            print(f"Error reading {file}")
            return None
        save_data_to_csv(arts)
        print(f"Data from {file} saved")
    print("All data saved")
    return arts

def main():
    get_arts()

if __name__ == '__main__':
    main()