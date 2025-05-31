Feature: Browse Books by Category

  As an anonymous user
  I want to browse books by category
  So that I can find books I'm interested in

  Background:
    Given the following categories exist for browsing:
      | Category Name |
      | Fiction       |
      | Non-Fiction   |
      | Science       |
      | History       |
    And the following books exist:
      | Title                | Categories           |
      | The Smashing Book     | Fiction              |
      | Thinking with Type| Science              |
      | Book Title 1 |  Non-Fiction |
      | Android Wireless Application Development                 | Science, Non-Fiction |

  Scenario: View available categories
    When I visit the home page
    Then I should see a list of all available categories

  Scenario: Select a category to view books
    When I visit the book browsing page
    And I select the "Fiction" category
    Then I should see a list of books in the "Fiction" category
    And the list should include "The Smashing Book"

  Scenario: View books in multiple categories
    When I visit the book browsing page
    And I select the "Non-Fiction" category
    Then I should see a list of books in the "Non-Fiction" category
    And the list should include "Book Title 1"
    And I select the "Science" category
    Then I should see a list of books in the "Science" category
    And the list should include "Android Wireless Application Development"

  Scenario: No books in a category
    When I visit the book browsing page
    And I select the "History" category
    Then I should see a message saying "No books found in this category"
