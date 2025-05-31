Feature: Search for Books
  As an anonymous user
  I want to search for books by title or author name
  So that I can find books matching my interests

  Background:
    Given the following books exist for searching:
      | title                   | author      | category    |
      | Python Programming      | John Doe    | Fiction     |
      | Data Science Basics     | Jane Smith  | Non-fiction |
      | Python for Data Science | John Doe    | Non-fiction |
  Scenario: Search for books by title
    Given I am on the homepage
    When I enter "Python" in the search bar
    Then I should see a list of books whose title contains "Python"

  Scenario: Search for books by author
    Given I am on the homepage
    When I enter "Jane Smith" in the search bar
    Then I should see a list of books written by the author whose name is "Jane Smith"

  Scenario: Search for books by both title and author
    Given I am on the homepage
    When I enter "Python Programming John Doe" in the search bar
    Then I should see a list of books whose title is "Python Programming" and author is "John Doe"

  Scenario: Search for books in a specific category
    Given I am on the homepage
    When I select a category "Non-fiction"
    And I enter "John Doe" in the search bar
    Then I should see a list of books in the "Non-fiction" category whose author is "John Doe"
