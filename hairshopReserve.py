from playwright.sync_api import sync_playwright

designer = "여주환 원장"
reserve_date = "23"
reserve_time = "5:00"
style = "남성커트"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # 1. 네이버 접속
    page.goto("https://www.naver.com/")

    # 2. 검색
    search_input = page.locator("#query")
    search_input.fill("김천 마움헤어")
    search_input.press("Enter")

    # 3. 업체 예약 버튼 클릭
    company_booking = page.locator(
        'a[data-nlog-area="plc_btp.booking"]'
    )

    company_booking.wait_for(state="visible")
    company_booking.click()

    # 4. 디자이너 찾기
    item = page.locator("li").filter(
        has_text=designer
    )

    item.first.wait_for(state="visible")

    # 5. 해당 디자이너 예약 버튼
    booking = item.get_by_text(
        "예약",
        exact=True
    ).first

    booking.wait_for(state="visible")

    # 6. 예약 클릭
    booking.click()

    # 새 페이지 생성 대기
    page.wait_for_timeout(2000)

    # 7. 새로 열린 예약 페이지
    pages = page.context.pages
    reserve_page = pages[-1]

    reserve_page.wait_for_load_state("domcontentloaded")
    reserve_page.wait_for_timeout(1000)

    # 8. 달력이 있는 frame 찾기
    target_frame = None

    for _ in range(20):

        for frame in reserve_page.frames:
            try:
                calendar = frame.locator(
                    "tbody.calendar_body"
                )

                if calendar.count() > 0:
                    target_frame = frame
                    break

            except:
                continue

        if target_frame:
            break

        reserve_page.wait_for_timeout(500)

    # 9. 날짜 선택
    date_button = target_frame.locator(
        'button.calendar_date:not([disabled])'
    ).filter(
        has_text=reserve_date
    ).first

    date_button.wait_for(state="visible")
    date_button.click()

    # 10. 시간 선택
    time_button = target_frame.locator(
        "button.btn_time"
    ).filter(
        has_text=reserve_time
    ).first

    time_button.wait_for(state="visible")
    time_button.click()

    # 시술 목록이 렌더링될 시간
    target_frame.wait_for_timeout(1000)

    # 11. 시술 영역 대기
    treatment_section = target_frame.locator(
        'section[data-testid="beauty-treatment-options"]'
    )

    treatment_section.wait_for(state="visible")

    # 12. 원하는 시술 제목 정확하게 찾기
    treatment_title = treatment_section.get_by_text(
        style,
        exact=True
    )

    treatment_title.wait_for(state="visible")

    # 13. 시술 제목을 감싸고 있는 label 찾기
    treatment_label = treatment_title.locator(
        "xpath=ancestor::label[1]"
    )

    # 해당 항목이 화면에 보이도록 스크롤
    treatment_label.scroll_into_view_if_needed()

    # 실제 사용자처럼 label 클릭
    treatment_label.click()

    # 14. 실제 checkbox 상태 확인
    checkbox = treatment_label.locator(
        'input[type="checkbox"]'
    )

    if checkbox.is_checked():
        print(style, "선택 완료")
    else:
        print(style, "선택 실패")

    # 결과 확인용
    reserve_page.wait_for_timeout(20000)

    browser.close()