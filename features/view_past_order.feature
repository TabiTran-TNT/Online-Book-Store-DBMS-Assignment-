Feature: View Past Orders
  As a registered user
  I want to view all past orders I have made

  Scenario: View past orders
    Given I am a registered user with one order in the past
    When I visit the order history page
    Then I should see the order
    And I click the chevron icon
    Then I should see the order details
    And I navigate to homepage and make a purchase
    And I navigate to order history page
    Then I should see the new order
