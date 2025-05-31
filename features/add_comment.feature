Feature: Add Rating and Comment

  As a registered user,
  I want to add a rating and comment to a book
  So that I can share my feedback and experiences with other users

  Scenario: Add rating and comment to a book
    Given a user with email 'testuser@example.com' and password 'testpassword' exists
    And there is a book in the database with the following details for comment test
      | Title       | Author        | Publisher      | Published Date | Price |
      | Test Book 1 | Test Author 1 | Test Publisher | 2023-01-01    | 19.99 |
    And I am logged in as "testuser@example.com" with password "testpassword"
    And I am on the book comment page for "Test Book 1" for comment test
    And I click on the "Write a review" button
    When I add a rating of "4" and a comment "This book is amazing!"
    Then I should see my comment 'This book is amazing!' with rating '4'

  Scenario: Attempt to add multiple ratings and comments to the same book
    Given a user with email 'testuser@example.com' and password 'testpassword' exists
    And there is a book in the database with the following details for comment test
      | Title       | Author        | Publisher      | Published Date | Price |
      | Test Book 2 | Test Author 2 | Test Publisher | 2023-01-01    | 19.99 |
    And I am logged in as "testuser@example.com" with password "testpassword"
    And I am on the book comment page for "Test Book 2" for comment test
    And I click on the "Write a review" button
    When I add a rating of "3" and a comment "Decent read."
    And I try to add a rating and a comment again
    Then I should see pop up modal informing I can only comment once

  Scenario: Add rating and comment on book detail page
    Given a user with email 'testuser@example.com' and password 'testpassword' exists
    And there is a book in the database with the following details for comment test
      | Title       | Author        | Publisher      | Published Date | Price |
      | Test Book 2 | Test Author 2 | Test Publisher | 2023-01-01     | 19.99 |
    And I am logged in as "testuser@example.com" with password "testpassword"
    And I am on the book details page for "Test Book 2"
    And I click on the "Write a review" button
    When I add a rating of "5" and a comment "This book is a must-read!"
    Then I should see my comment 'This book is a must-read!' with rating '5'

  Scenario: Attempt to add rating and comment to a book when not logged in
    Given I am an unauthenticated user
    And there is a book in the database with the following details for comment test
      | Title       | Author        | Publisher      | Published Date | Price |
      | Test Book 2 | Test Author 2 | Test Publisher | 2023-01-01    | 19.99 |
    And I am on the book comment page for "Test Book 2" for comment test
    When I click on the "Write a review" button for anonymous users
    Then I should see the login modal appear with notification to log in to comment
