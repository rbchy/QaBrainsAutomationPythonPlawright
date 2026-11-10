"""Login, logout, registration and forgot-password steps."""
import time

from behave import given, then, when

from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from utils.base_test import BaseTest
from utils.config_reader import ConfigReader


def _login():
    return LoginPage(BaseTest.get_page())


def _registration():
    return RegistrationPage(BaseTest.get_page())


def _forgot():
    return ForgotPasswordPage(BaseTest.get_page())


# ---------- login / logout ----------

@given("User is on the login page")
def step_on_login_page(context):
    _login().open()


@when("User enters valid username and password")
def step_valid_login(context):
    _login().login(ConfigReader.get("valid_email"), ConfigReader.get("valid_password"))


@when("User enters invalid username and password")
def step_invalid_login(context):
    _login().login("wrong@test.com", "wrongpass")


@then("User should be logged in successfully")
def step_logged_in(context):
    _login().expect_logged_in()


@then('Error message "{message}" should be displayed')
def step_login_error(context, message):
    _login().expect_invalid_login_error(message)


@given("User is logged in")
def step_is_logged_in(context):
    page = _login()
    page.login(ConfigReader.get("valid_email"), ConfigReader.get("valid_password"))
    page.expect_logged_in()


@when("User clicks on logout button")
def step_logout(context):
    _login().logout()


@then("User should be logged out successfully")
def step_logged_out(context):
    _login().expect_logged_out()


# ---------- registration ----------

@given("User is on the registration page")
def step_on_registration_page(context):
    _registration().open()


def _register(email):
    page = _registration()
    page.fill("Ranajit Chowdhury", "United States", "Engineer", email, "Password123", "Password123")
    page.submit()


@when("User registers with a unique email")
def step_register_unique(context):
    _register(f"rbtest{int(time.time() * 1000)}@mailtest.com")


@when('User registers with email "{email}"')
def step_register_with(context, email):
    _register(email)


@then("User should be registered successfully")
def step_registered(context):
    _registration().expect_registered()


@then("Email validation error message should be displayed")
def step_email_rejected(context):
    _registration().expect_email_rejected()


# ---------- forgot password ----------

@given("User is on Forgot Password page")
def step_on_forgot_page(context):
    _forgot().open()


@when('User requests a password reset for "{email}"')
def step_request_reset(context, email):
    _forgot().request_reset(email)


@then('User should see success message "{expected}"')
def step_reset_success(context, expected):
    _forgot().expect_success(expected)


@then('User should see error message "{expected}"')
def step_reset_error(context, expected):
    _forgot().expect_validation_error(expected)
