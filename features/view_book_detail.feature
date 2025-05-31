Feature: View Book Details
  As an anonymous user,
  I want to view detailed information about a book
  So that I can learn more about it and decide whether to add it to my shopping cart

  Background:
    Given the following categories exist:
      | Category Name |
      | Fiction       |

    And the following books exist:
      | Title                | Categories           |
      | The Smashing Book     | Fiction              |

    Scenario: View detailed book information
        Given I am on the home page
        When I click on the book title to visit its detail
        Then I should see all information about the book

