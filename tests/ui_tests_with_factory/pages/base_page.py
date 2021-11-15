class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def go_to(self, url):
        self.driver.get(url)

    def back(self):
        self.driver.back()

    def forward(self):
        self.driver.forward()

    def refresh(self):
        self.driver.refresh()

    @property
    def title(self):
        return self.driver.title
