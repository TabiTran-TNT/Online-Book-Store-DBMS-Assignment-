Feature: Checkout and Confirm Order without payment

  As a user,
  I want to checkout and confirm my order
  So that I can proceed with the purchase and have the order details saved in history

  Scenario: Checkout from shopping cart page
    Given I am a registered user
    And I have added items to my shopping cart
    When I navigate to the shopping cart page
    And I choose to checkout
    Then I should be directed to the checkout page
    And I fill the following information
        | Field              |             Value                   |
        | shipping_address   | 123 Pham Duc Thang, District 10.    |
        | zip_code           |             70000                   |
        | city               |           Ho Chi Minh               |
        | country            |          Viet Nam                   |
    And I click Proceed button
    And I click Place Order button
    Then the order details should be stored into the database

 Scenario: Checkout from shopping cart page
    Given I am an anonymous user
    And I have added items to my shopping cart
    When I navigate to the shopping cart page
    And I choose to checkout
    Then the login modal will pop up
    And I see the message "Only signed member can checkout." on the modal
