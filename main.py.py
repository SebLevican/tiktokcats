import cat
import joinvideos

def main():
    cat.scrape_tiktok_videos()
    print('joining videos')
    #number min of videos and min of minutes
    joinvideos.join_videos(11, 10)

if __name__ == '__main__':
    main()