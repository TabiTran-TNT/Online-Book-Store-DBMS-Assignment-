Feature: Book List Pagination
  As a user
  I want to see books listed in pages with customizable page sizes
  So that I can browse through a large number of books efficiently

  Background:
    Given there are 100 books in the database

  Scenario: Default pagination
    When I visit the home page for pagination
    Then I should see 10 books listed
    And I should see pagination controls
    And the page should indicate it is page 1 of 10

  Scenario: Custom items per page
    When I visit the home page for pagination
    And I select "10" items per page from the dropdown
    Then I should see 10 books listed
    And the page should indicate it is page 1 of 10
    And I select "20" items per page from the dropdown
    Then I should see 20 books listed
    And the page should indicate it is page 1 of 5
    And I select "30" items per page from the dropdown
    Then I should see 30 books listed
    And the page should indicate it is page 1 of 4
    And I select "40" items per page from the dropdown
    Then I should see 40 books listed
    And the page should indicate it is page 1 of 3
    And the dropdown should show options for 10, 20, 30, and 40 items per page


  Scenario: Navigating to the second page
    When I visit the home page for pagination
    And I click on the "Next" page link
    Then I should see 10 books listed
    And the page should indicate it is page 2 of 10

  Scenario: Navigating to the last page
    When I visit the home page for pagination
    And I click on the "Last" page link
    Then I should see 10 books listed
    And the page should indicate it is page 10 of 10

  Scenario: Invalid page number
    When I visit the home page with a query parameter "page=999"
    Then I should see an error message
