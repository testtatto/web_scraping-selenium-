from selenium import webdriver


# 1日の釣果詳細を1行ごとにリストに入れる関数
def get_daily_record(choka_list, element, index, date):
    row = 1
    common_xpath = '//*[@id="' + index + '"]/table/tbody/tr[' + str(row) + ']/'
    # 魚種が登録されていないところをテーブルの終点として1行ずつリストに入れていく
    while len(element.find_elements_by_xpath(common_xpath + 'td[2]')) != 0:

        fish_category = element.find_element_by_xpath(common_xpath + 'td[2]').text  # 魚種
        amount = element.find_element_by_xpath(common_xpath + 'td[3]').text  # 匹数
        size = element.find_element_by_xpath(common_xpath + 'td[4]').text  # 大きさ
        weight = element.find_element_by_xpath(common_xpath + 'td[5]').text  # 重さ
        special_mention = element.find_element_by_xpath(common_xpath + 'td[6]').text  # 特記
        point = element.find_element_by_xpath(common_xpath + 'td[7]').text  # ポイント

        choka_list.append([date, fish_category, amount, size, weight, special_mention, point])
        row += 1
        common_xpath = '//*[@id="' + index + '"]/table/tbody/tr[' + str(row) + ']/'


# 1画面内の釣果詳細をリストに入れていく関数
def choka_list_in_page(driver, choka_list):
    chokaBox_elements = driver.find_elements_by_class_name('chokaBox')
    for i in chokaBox_elements:
        chokaBox_index = i.get_attribute('id')  # 日ごとにつけられている識別番号
        chokaBox_element = driver.find_element_by_id(chokaBox_index)
        choka_date = driver.find_element_by_xpath('//*[@id="' + str(chokaBox_index) + '"]/header/ul/li').text
        get_daily_record(choka_list, chokaBox_element, chokaBox_index, choka_date)


# 「次」ボタンを押して次画面に遷移する関数
def next_page(driver):
    next_button = driver.find_element_by_link_text('次')
    next_button.click()


if __name__ == '__main__':
    DRIVER_PATH = './driver/chromedriver.exe'
    URL = 'https://www.fishing-v.jp/choka/choka_detail.php?s=11284'
    PAGES = 3  # 何ページ分読み込むかの設定値
    driver = webdriver.Chrome(DRIVER_PATH)
    driver.get(URL)

    all_choka_list = []
    for times in range(1, PAGES + 1):
        print(str(times) + "ページの取り込みを開始します")
        choka_list_in_page(driver, all_choka_list)
        print(str(times) + "ページの取り込みが完了しました")
        next_page(driver)

    print(all_choka_list)
