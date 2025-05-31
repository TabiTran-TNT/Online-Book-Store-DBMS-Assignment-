Feature: Add books to shopping cart

  As an (logged in or anonymous) user,
  I want to add books to my shopping cart
  So that I can purchase them later

  Scenario: Add books to shopping cart
    Given I am an user at detail page of a book
    When I click on the "Add to Cart" button
    Then I should see the cart display number 1
    When I visit cart detail page
    Then I should see the order of the book I added
    And I click the remove button

  Scenario: Remove books from shopping cart
    Given I am an user at detail page of a book
    When I click on the "Add to Cart" button
    And I visit cart detail page
    When I click the remove button
    Then order should be deleted
    And the number should be disappeared on the cart icon

  Scenario: Increase quantity of books in shopping cart
    Given I am an user at detail page of a book
    When I click on the "Add to Cart" button
    And I visit cart detail page
    When I click the increase button
    Then the quantity should be 2
    And the total price should be updated
    And the number should be updated on the cart icon
    And I click the remove button

  Scenario: Decrease quantity of books in shopping cart
    Given I am an user at detail page of a book
    When I click on the "Add to Cart" button
    When I click on the "Add to Cart" button
    And I visit cart detail page
    When I click the decrease button
    Then the quantity should be 1
    And I click the remove button

  Scenario: Visit cart when there is no order
    When I visit cart detail page
    Then I should see the message "Your cart is currently empty"
