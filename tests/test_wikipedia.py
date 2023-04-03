import allure
from allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import have
from selene.support.shared import browser


@allure.title('Test search')
def test_search():
    with step('Test search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Search Wikipedia')).click()
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/search_src_text')).type('QA')
        browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title')).should(have.size_greater_than(0))
    with step('Test go to page '):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title')).click()
        browser.element((AppiumBy.CLASS_NAME, 'android.widget.TextView')).should(have.text('An error occurred'))
    with step('Text button "GO BACK"'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/view_wiki_error_button')).click()
        browser.element((AppiumBy.CLASS_NAME, 'android.widget.TextView')).should(have.text('Search Wikipedia'))