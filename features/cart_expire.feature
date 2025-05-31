Feature: Login notification when session expires

    As a user,
    I want to be notified when my session expires
    So that I can log back in and continue using the application

    Scenario: Show login modal and change UI
        Given I am at the home page as anonymous user
        And I have added items to my shopping cart
        When there is only 15 minutes left in my session
        Then I should see login modal pops up
        And I should see the UI change to indicate the session is about to expire
