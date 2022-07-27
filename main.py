from Crawling_Instagram import InstagramDmBot

if __name__ == '__main__':
    channels = input('Please enter your channel  ("sample1,sample2"): ').split(',')
    quantity = int(input('How many user did you want to receive your message:  '))

    ig = InstagramDmBot()
    ig.get_username_id(channels, quantity=quantity)
