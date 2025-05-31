Feature: Add books to shopping cart

  As an logged in user,
  I want to add books to my shopping cart
  So that I can purchase them later

  Scenario: Save cart items for logged in user
    Given I am an authenticated user with email "user@gmail.com" and password "password"
    And I am at detail page of a book
    When I click on the "Add to Cart" button
    Then I should see the item in cart detail page
    Then I sign out and log in again
    And I visit cart detail page
    Then I still can see the item in cart detail page
    And I click the remove button

  Scenario: Save anonymous cart items when user logs in
    Given I am an anonymous user at detail page of a book
    When I click on the "Add to Cart" button
    Then I should see the item in cart detail page
    Then I sign in with email "user@gmail.com" and password "password"
    And I visit cart detail page
    Then I still can see the item in cart detail page
    And I click the remove button

  Scenario: Merge anonymous cart items with logged in user's cart items
    Given I am an authenticated user with email "user@gmail.com" and password "password"
    And I am at detail page of a book
    When I click on the "Add to Cart" button
    Then I sign out and add a book to cart as an anonymous user
    And I sign in again
    And I visit cart detail page
    Then I should see items with quantity of 2
    And I click the remove button
