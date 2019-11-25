import fortnite_api

fn = fortnite_api.FortniteAPI()


if __name__ == '__main__':
    fn.creator_code.fetch('uhide')
