from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.korail.com/ticket/main")

    page.locator("a.btn_start").click()

    search_input = page.locator('input[name="searchTxt"]')
    search_input.fill("김천구미")
    search_input.press("Enter")

    page.locator("a.btn_end").click()

    search_input = page.locator('input[name="searchTxt"]')
    search_input.fill("포항")
    search_input.press("Enter")

    page.locator('a.btn_brth').click()

        
    page.locator(".tableWrap .day", has_text="23").first.click()    
    page.wait_for_timeout(1000)
    
    for _ in range(10):        
        item = page.locator(
            '.slick-slide.slick-active a',
            has_text="10시"
        )

        if item.count() > 0:
            item.click()
            break

        page.locator("button.slick-next").nth(3).click()
        page.wait_for_timeout(1000)

    page.locator(".btn_bn-blue").click()

    page.locator(".btn_lookup").click()
    input("Enter를 입력하면 종료됩니다.")
    browser.close()
