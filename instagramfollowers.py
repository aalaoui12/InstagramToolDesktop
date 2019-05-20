from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from pyvirtualdisplay import Display
from explicit import waiter, XPATH
from bs4 import BeautifulSoup
import time

# This program takes around 1 minute for someone with 250 followers/following

def startDriver():
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Chrome()
    return driver
def quitDriver(driver):
    driver.quit()

def login(driver, user, pwd): # returns true if login works, otherwise returns false

    driver.get("https://www.instagram.com/accounts/login/")

    # find and write in input fields to login
    waiter.find_write(driver, "//div/input[@name='username']", user, by=XPATH)
    waiter.find_write(driver, "//div/input[@name='password']", pwd, by=XPATH)
    # submit
    waiter.find_element(driver, "//div/button[@type='submit']", by=XPATH).click()

    # waits until the homepage loads before exiting function

    try:
        waiter.find_element(driver, "//a/span[@aria-label='Find People']", by=XPATH)
    except:
        print("Doesn't work")
        return False

    return True


def getFollowers(driver, user):
    driver.get("https://www.instagram.com/" + user)

    numFollowers = int(waiter.find_element(driver, "//li[2]/a/span", by=XPATH).text) # li[2] refers to second li in structure
    print("You have " + str(numFollowers) + " followers")

    waiter.find_element(driver, "//a[@href='/{0}/followers/']".format(user), by=XPATH).click()
    dialog = waiter.find_element(driver, "//div[@role='dialog']/div[2]/ul", by=XPATH)  # makes sure followers have loaded. select ul in div with role of dialog
    dialog.click()

    units = waiter.find_elements(driver, "//div[@role='dialog']/div[2]/ul/div/li", by=XPATH)
    numUnits = len(units)
    print("There are " + str(numUnits) + " followers per scroll.")

    scrollFinished = False
    sameCounter = 0  # makes sure we should truly stop scrolling, once this reaches 5 we stop

    while(scrollFinished is False and (numFollowers > 12)):  # no need to scroll if numfollowers is 12 or less (this was originally 22)
        followers = waiter.find_elements(driver, "//div[@role='dialog']/div[2]/ul/div/li", by=XPATH)
        lastFollower = len(followers) - 1

        dialog.click()  # ensures dialog is focused
        try:
            driver.execute_script("arguments[0].scrollIntoView();", followers[lastFollower])
            time.sleep(0.25)
        except StaleElementReferenceException:  # in case an element reloads, we're "taking a breather"
            time.sleep(3.5)
            continue

        if(lastFollower > 22 and lastFollower == oldLastFollower):  # only stop when it has loaded all followers
            sameCounter = sameCounter + 1
            if(sameCounter == 5):
                scrollFinished = True  # to avoid any bugs

        oldLastFollower = lastFollower
        time.sleep(.5)

    units = waiter.find_elements(driver, "//div[@role='dialog']/div[2]/ul/div/li", by=XPATH)
    numUnits = len(units)
    print("To confirm, you have " + str(numUnits) + " followers.")

    followers = parseHTML(driver)
    print(len(followers))
    return followers


def getFollowing(driver, user):
    driver.get("https://www.instagram.com/" + user)
    numFollowing = int(waiter.find_element(driver, "//li[3]/a/span", by=XPATH).text)

    print("You are following " + str(numFollowing) + " people")

    waiter.find_element(driver, "//a[@href='/{0}/following/']".format(user), by=XPATH).click()
    dialog = waiter.find_element(driver, "//div[@role='dialog']/div[2]/ul", by=XPATH)
    dialog.click()

    units = waiter.find_elements(driver, "//div[@role='dialog']/div[2]/ul/div/li", by=XPATH)
    numUnits = len(units)
    print("There are " + str(numUnits) + " followers per scroll.")

    scrollFinished = False
    sameCounter = 0

    while(scrollFinished is False and (numFollowing > 12)):  # no need to scroll if numfollowers is 12 or less (this used to be 24)
        following = waiter.find_elements(driver, "//div[@role='dialog']/div[2]/ul/div/li", by=XPATH)
        lastFollowing = len(following) - 1

        dialog.click()

        try:
            driver.execute_script("arguments[0].scrollIntoView();", following[lastFollowing])
            time.sleep(0.25)
        except StaleElementReferenceException:  # in case an element reloads, we're "taking a breather"
            time.sleep(3.5)
            continue

        if(lastFollowing > 24 and lastFollowing == oldLastFollowing):
            sameCounter = sameCounter + 1
            if(sameCounter == 5):
                scrollFinished = True  # to avoid any bugs

        oldLastFollowing = lastFollowing
        time.sleep(.5)

    following = parseHTML(driver)
    print(len(following))
    return following

def getNonFollowers(followers, following):
    nonFollowers = {}  # those you follow that don't follow back

    for x in following:
        followsBack = False  # tracks whether following follows back
        for y in followers:
            if(x == y):
                followsBack = True
        if(followsBack is False):
            nonFollowers[x] = following[x]

    print("nonfollowers has " + str(len(nonFollowers)))

    return nonFollowers


def parseHTML(driver):  # now we parse!
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    followList = soup.findAll('li', attrs={'class': 'wo9IH'})

    followsDict = {}
    for row in followList:
        data = row.div.findAll("div")[2]
        username = data.find("a").text.strip()
        fullName = data.find('div', attrs={'class': 'wFPL8'}).text.strip()

        followsDict[username] = fullName

    return followsDict



