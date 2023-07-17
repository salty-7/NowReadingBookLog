import json
import urllib.request
import webbrowser

class NowBooklog:
    def __init__(self, userid):
        self.userid = userid
        self.booklist = []
        self.booklog_base_url = 'https://api.booklog.jp/v2/json/'
        self.tweet_base_url = 'https://twitter.com/intent/tweet?text='

    def getBooklist(self):
        booklog_url = self.booklog_base_url + self.userid
        req = urllib.request.Request(booklog_url)
        with urllib.request.urlopen(req) as res:
            body = res.read().decode('utf-8')
            if res.status == 200:
                data = json.loads(body)
                self.booklist = data['books']
            else:
                print('Error: ', res.status)
        return len(self.booklist)
    
    def showBookList(self):
        for i, book in enumerate(self.booklist):
            print(i, ": ", book['title'])
    
    def tweetBook(self, selected_id):
        book = self.booklist[selected_id]
        book_title = book['title']
        book_url = book['url']
        tweet_text = "📖読了：" + book_title + " " + book_url
        tweet_url = self.tweet_base_url + tweet_text
        webbrowser.open(tweet_url)

def main():
    # init
    userid = input('Input user_id => ')
    client = NowBooklog(userid)

    # get book list
    print("importing book list.....")
    len_list = client.getBooklist()
    if len_list <= 0:
        print("Error: Book list is empty.")
        return

    # show book list
    client.showBookList()

    # ask which book to tweet
    selected_id = int(input('select index you want to tweet => '))
    if selected_id >= len(client.booklist):
        print("Error: index over the length of the book list.")
        return

    # tweet book
    client.tweetBook(selected_id)

if __name__ == "__main__":
    main()
    input("Push ENTER to Exit.")