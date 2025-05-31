Feature: View Book Comments
  As a user
  I want to view all comments for a specific book
  So that I can read other users' opinions about the book

  Background:
    Given the following users exist in the database:
      | Email             | Name      | Phone        | Birthday   |
      | user1@example.com | User One  | +1234567890  | 1990-01-01 |
      | user2@example.com | User Two  | +2345678901  | 1985-05-05 |
      | user3@example.com | User Three| +3456789012  | 1995-10-10 |
    And there is a book in the database with the following details:
      | Title     | Author   | Publisher | Published Date | Price  |
      | Test Book | John Doe | ABC Press | 2023-01-01     | 100.00 |
    And the book "Test Book" has the following comments:
      | User Email        | Rating | Content             | Date       |
      | user1@example.com | 5      | Great read!         | 2023-05-20 |
      | user2@example.com | 4      | Very informative    | 2023-05-19 |
      | user3@example.com | 3      | It was okay         | 2023-05-18 |

  Scenario: Navigate to book comments page
    Given I am on the book details page for "Test Book"
    When I click on the link to the rating page
    Then I should be on the comments page for "Test Book"

  Scenario: View all comments for the book
    Given I am on the comments page for "Test Book"
    Then I should see the title "Test Book"
    And I should see 3 comments

  Scenario: Comment details and rating
    Given I am on the comments page for "Test Book"
    Then each comment should display:
      | Information |
      | User name   |
      | Rating      |
      | Content     |
      | Date        |
