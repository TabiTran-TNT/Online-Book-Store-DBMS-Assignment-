Feature: Edit Personal Information
  As a registered user,
  I want to modify my personal information
  So that I can keep my account details up to date

  Background:
    Given a user with email 'testuser@example.com' and password 'testpassword' exists
    Given the user is logged in

  Scenario: User updates password
    Given the user click "My Profile" page
    When the user chooses to update their password
    And enters the current password along with a new password
    And click the Save button
    Then user will be logged out
    And user can log in again with new password

  Scenario: User updates email
    Given the user click "My Profile" page
    When the user chooses to update their email address with 'modifyuser@example.com'
    And click the Save button
    Then the user's email address will be updated to 'modifyuser@example.com'

  Scenario: User attempts to update with incorrect current password
    Given the user click "My Profile" page
    When the user chooses to update their password
    And enters an incorrect current password
    And click the Save button
    Then the error message "Current password is incorrect"
