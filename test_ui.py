from playwright.sync_api import Page, expect
import time

def test_add_todo_item(page: Page):
    page.goto("https://demo.playwright.dev/todomvc")
    new_todo = page.get_by_placeholder("What needs to be done")
    time.sleep(2)
    new_todo.fill("Prepare for HPE interview")
    time.sleep(2)
    new_todo.press("Enter")
    time.sleep(2)
    expect(page.get_by_text("Prepare for HPE interview")).to_be_visible()

def test_complete_todo_item(page: Page):
    page.goto("https://demo.playwright.dev/todomvc")
    new_todo = page.get_by_placeholder("What needs to be done?")
    time.sleep(2)
    new_todo.fill("Buy groceries")
    time.sleep(2)
    new_todo.press("Enter")
    time.sleep(2)
    page.get_by_role("checkbox", name="Toggle Todo").check()
    time.sleep(2)
    expect(page.locator("li.completed")).to_have_count(1)

def test_delete_todo_item(page: Page):
    page.goto("https://demo.playwright.dev/todomvc")
    new_todo = page.get_by_placeholder("What needs to be done?")
    new_todo.fill("Temporary task")
    new_todo.press("Enter")
    time.sleep(3)
    page.hover("text=Temporary task")
    time.sleep(2)
    page.locator(".destroy").click()
    expect(page.get_by_text("Temporary task")).not_to_be_visible()