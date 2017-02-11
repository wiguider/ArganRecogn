# This class has aim : Searching and Downloading Google Images/Image Links
# Import Libraries
import time  # Importing the time library to check the time of code execution
import sys  # Importing the System Library
import urllib2


class ImageProvider:
    # This list is used to search keywords. You can edit this list to search for google images of your choice.
    #  You can simply add and remove elements of the list.
    def __init__(self):
        pass

    search_keyword = ['']
    # This list is used to further add suffix to your search term.
    # Each element of the list will help you download 100 images.
    # First element is blank which denotes that no suffix is added to the search keyword of the above list.
    # You can edit the list by adding/deleting elements from it.
    # So if the first element of the search_keyword is 'Australia'
    # and the second element of keywords is 'high resolution',
    # then it will search for 'Australia High Resolution'
    keywords = None

    # Downloading entire Web Document (Raw Page Content)
    @staticmethod
    def download_page(url):
        version = (3, 0)
        cur_version = sys.version_info
        if cur_version >= version:  # If the Current Version of Python is 3.0 or above
            import urllib.request  # urllib library for Extracting web pages
            try:
                headers = {
                    'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/41.0.2228.0 Safari/537.36"
                }
                req = urllib.request.Request(url, headers=headers)
                resp = urllib.request.urlopen(req)
                respData = str(resp.read())
                return respData
            except Exception as e:
                print(str(e))
        else:  # If the Current Version of Python is 2.x
            import urllib2
            try:
                headers = {
                    'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) "
                                  "Chrome/24.0.1312.27 Safari/537.17"
                }
                req = urllib2.Request(url, headers=headers)
                response = urllib2.urlopen(req)
                page = response.read()
                return page
            except:
                return "Page Not found"

    # Finding 'Next Image' from the given raw page
    @staticmethod
    def images_get_next_item(s):
        start_line = s.find('rg_di')
        if start_line == -1:  # If no links are found then give an error!
            end_quote = 0
            link = "no_links"
            return link, end_quote
        else:
            start_line = s.find('"class="rg_meta"')
            start_content = s.find('"ou"', start_line + 1)
            end_content = s.find(',"ow"', start_content + 1)
            content_raw = str(s[start_content + 6:end_content - 1])
            return content_raw, end_content

    # Getting all links with the help of '_images_get_next_image'
    def images_get_all_items(self, page):
        items = []
        while True:
            item, end_content = self.images_get_next_item(page)
            if item == "no_links":
                break
            else:
                items.append(item)  # Append all the links in the list named 'Links'
                time.sleep(0.1)  # Timer could be used to slow down the request for image downloads
                page = page[end_content:]
        return items

    @staticmethod
    def get_as_name_as(name):
        name_as_list = name.split('_')
        name = ""
        for item in name_as_list:
            name += str(item) + " "
        return name

    # TODO : give the path in argument
    def get_images_from_web(self, name_of_person, number_of_images):
        ############## Main Program ############
        t0 = time.time()  # start the timer
        # Download Image Links
        i = 0
        while i < len(self.search_keyword):
            items = []
            iteration = "Item no.: " + str(i + 1) + " -->" + " Item name = " + str(self.search_keyword[i])
            print (iteration)
            print ("Evaluating...")
            search_keywords = self.search_keyword[i]
            search = search_keywords.replace(' ', '%20')
            j = 0
            temp_name = name_of_person[0]
            name_of_person[0] = self.get_as_name_as(name_of_person[0])
            self.keywords = name_of_person
            while j < len(self.keywords):
                pure_keyword = self.keywords[j].replace(' ', '%20')
                url = 'https://www.google.com/search?q=' + search + pure_keyword \
                      + '&espv=2&biw=1366&bih=667&site=webhp&source=' \
                        'lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
                raw_html = (self.download_page(url))
                time.sleep(0.1)
                items = items + (self.images_get_all_items(raw_html))
                j += 1
            # print ("Image Links = "+str(items))
            print ("Total Image Links = " + str(len(items)))
            print ("\n")
            i += 1

            # This allows you to write all the links into a test file.
            # This text file will be created in the same directory as your code.
            # You can comment out the below 3 lines to stop writing the output to the text file.
            # info = open('output.txt', 'a')  # Open the text file called database.txt
            # Write the title of the page
            # info.write(str(i) + ': ' + str(self.search_keyword[i - 1]) + ": " + str(items) + "\n\n\n")
            # Close the file
            # info.close()
            # stop the timer
        t1 = time.time()
        # Calculating the total time required to crawl,
        # find and download all the links of 60,000 images
        total_time = t1 - t0

        print("Total time taken: " + str(total_time) + " Seconds")
        print ("Starting Download...")

        # To save imges to the same directory
        # IN this saving process we are just skipping the URL if there is any error
        k = 0
        error_count = 0
        while k < len(items):
            from urllib2 import Request, urlopen
            from urllib2 import URLError, HTTPError
            try:
                while number_of_images > 0:
                    req = Request(items[k], headers={
                        "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) "
                                      "Chrome/24.0.1312.27 Safari/537.17"})
                    response = urlopen(req)
                    output_file = open("images_google/" + temp_name + "_000" + str(k + 2) + ".jpg", 'wb')
                    data = response.read()
                    output_file.write(data)
                    response.close()
                    print("completed ====> " + str(k + 1))
                    number_of_images -= 1
                    k += 1
                break
            except IOError as e:  # If there is any IOError
                error_count += 1
                print("IOError on image " + str(k + 1))
                print e
                k += 1
            except HTTPError as e:  # If there is any HTTPError
                error_count += 1
                print("HTTPError" + str(k))
                k += 1
            except URLError as e:
                error_count += 1
                print("URLError " + str(k))
                k += 1
        print("\n")
        print("All are downloaded")
        print("\n" + str(error_count) + " ----> total Errors")
        # ----End of the main program ----#
