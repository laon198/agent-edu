from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.korail.com/ticket/main")
    page.locator(".btn_start").click()
    
    input("Enter를 입력하면 종료됩니다.")
    browser.close()
