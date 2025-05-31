Feature: Login with no Captcha Validation
  As a developer,
  I want to add Captcha Validation feature to login page
  So that I can validate user

  Scenario: User fails to login three times
    Given the user open the login modal
    When the user enters incorrect username/password combination three times
    Then the user should be prompted to validate with a Captcha
