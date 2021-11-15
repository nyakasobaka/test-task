class BasePage:
    def __init__(self, conf):
        self.driver = conf.driver
        self.ui_app = conf.ui_app

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
