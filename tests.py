import fortnite_api

fn = fortnite_api.FortniteAPI('my_key')


if __name__ == '__main__':
    fn.creator_code.exists('EasyFNStats')
