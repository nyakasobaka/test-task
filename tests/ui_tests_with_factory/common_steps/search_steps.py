

def serch_by_text(ui_page, text: str):
    ui_page.top_menu.send_text_to_search_input(text).click_search_button()


