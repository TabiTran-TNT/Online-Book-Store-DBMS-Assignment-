Feature: Add Rating and Comment

  As a registered user,
  I want sign out my account
  So that I can save security for my account

  Scenario: Attempt to add rating and comment to a book when not logged in
    Given I am an authenticated user
    When I click on the "Sign out" button
    Then I should see log out modal pop up
    And I click "Sign out" on the modal
    Then I should be logged out
