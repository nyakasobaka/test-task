import allure


def attach_png(attachment, attachment_name="Screenshot"):
    """Attach IMAGE/PNG to report"""
    allure.attach(attachment, attachment_name, allure.attachment_type.PNG)

