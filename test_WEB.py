
class Test_Web:

    def test_click_button(self, set_up_tear_down) -> None:
        page = set_up_tear_down
        page.get_by_role("listitem").filter(has_text="List users").click()
        page.locator("//*[@id='console']/div[1]/ul/li[2]").click()
        page.get_by_role("listitem").filter(has_text="Single user not found").click()
        page.get_by_role("listitem").filter(has_text="List <resource>").click()
        page.locator("//*[@id='console']/div[1]/ul/li[5]").click()
        page.get_by_role("listitem").filter(has_text="Single <resource> not found").click()
        page.get_by_role("listitem").filter(has_text="Create").click()
        page.get_by_role("listitem").filter(has_text="Update").first.click()
        page.get_by_role("listitem").filter(has_text="Update").nth(1).click()
        page.get_by_role("listitem").filter(has_text="Delete").click()
        page.get_by_role("listitem").filter(has_text="Register - successful").click()
        page.get_by_role("listitem").filter(has_text="Register - unsuccessful").click()
        page.get_by_role("listitem").filter(has_text="Login - successful").click()
        page.get_by_role("listitem").filter(has_text="Login - unsuccessful").click()
        page.get_by_role("listitem").filter(has_text="Delayed response").click()

    def test_API_WEB_assert(self, set_up_tear_down, api_web_assert) -> None:
        page = set_up_tear_down

        page.get_by_role("listitem").filter(has_text="Create").click()

        page.locator("//*[@id='console']/div[2]/div[2]/p/strong/span[text()='201']").click()

        RSP_CODE = page.locator("//*[@id='console']/div[2]/div[2]/p/strong/span[text()='201']").inner_text()

        page.locator("//*[@id='console']/div[2]/div[2]/pre").click()

        rsp_body = page.locator("//*[@id='console']/div[2]/div[2]/pre").inner_text()

        assert api_web_assert.status_code == int(RSP_CODE)
        assert api_web_assert.json()["name"] == rsp_body[15:23]
