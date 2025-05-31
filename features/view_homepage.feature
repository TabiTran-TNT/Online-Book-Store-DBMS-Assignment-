Feature: View home page
    Scenario: View home page
        When I visit "/"
        Then I should see the navbar with the link to home

    Scenario: As a user, I should see a list of books with their images, titles, authors, unit prices, and ratings
        Given there are books in the database
        When I visit "/"
        Then I should see a list of books with their images, titles, authors, unit prices, and ratings
