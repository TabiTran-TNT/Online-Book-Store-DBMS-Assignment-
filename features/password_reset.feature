Feature: Password Reset
  As a user,
  I want to reset my password
  So that I can regain access to my account if I forget it

  Scenario: User requests password reset with valid email
    Given the user is on homepage
    And the user open the login modal and click "Forgot your password"
    Then the password reset modal should be pop up
    And the user fill the valid email address and click submit button
    Then the success modal should be popped up

  Scenario: User requests password reset with invalid email
    Given the user is on homepage
    And the user open the login modal and click "Forgot your password"
    Then the password reset modal should be pop up
    And the user fill the invalid email address and click submit button
    Then the user should the error message "Invalid email"
