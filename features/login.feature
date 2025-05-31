Feature: Login with created account
  As a user,
  I want to login to my account
  So that I can access the platform's features

  Scenario: User succeeds to login
    Given I am an anonymous user on homepage and I visit sign in page
    Then I should see a form with following information: User name, Password
    When I fill in correct username/password combination
    | Field       | Value                          |
    | username    | binh.tran0611csbk@hcmut.edu.vn |
    | password    | 06112003                       |
    Then I will be directed to current page

  Scenario: User fails to login with unverified account
    Given I am an anonymous user on homepage and I visit sign in page
    When I fill in unverified username/password combination
    | Field       | Value                          |
    | username    | binh.tran0611csbk@hcmut.edu.vn |
    | password    | 06112003                       |
    Then the pop up modal should appear informing the user to verify their email

  Scenario: User fails to login with wrong credentials
    Given I am an anonymous user on homepage and I visit sign in page
    When I fill in incorrect username/password combination
    | Field       | Value                          |
    | username    | binh.tran0611csbk@hcmut.edu.vn |
    | password    | Tabi0611@                      |
    Then the user should be see the message "Invalid username and/or password"
