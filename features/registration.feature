Feature: Account Registration
    As a user,
    I want to register an account
    So that I can access the platform's features

    Scenario: Successful registration
        Given I am an anonymous user and I open sign up modal
        Then I should see a form with following information: Email, Password, Phone, Full name, Birthday

        When I fill in necessary and valid information
        | Field       | Value                          |
        | email       | binh.tran0611csbk@hcmut.edu.vn |
        | password1   | Tabi0611@                      |
        | password2   | Tabi0611@                      |
        | phone       | 0859007204                     |
        | full name   | Tran Nguyen Thai Binh          |
        | birth_year  | 2003                           |
        | birth_month | 11                             |
        | birth_day   | 06                             |

        Then the pop up modal inform verification email has been sent
        And my information should be stored in the system

    Scenario: Wrong format input in registration
        Given I am an anonymous user and I open sign up modal
        When I fill in some invalid fields
        | Field       | Value                          |
        | email       | binh.tran0611csbk@hcmut        |
        | password1   | Tabi0611@                      |
        | password2   | Tabri0611@                     |
        | phone       | 032165498                      |
        | full name   | Tran Nguyen Thai Binh          |
        | birth_year  | 2003                           |
        | birth_month | 11                             |
        | birth_day   | 55                             |
        Then I should see the error messages and the format it should be

    Scenario: Email has already been used
        Given I am an anonymous user and I open sign up modal
        When I fill in an already used email
        | Field       | Value                          |
        | email       | binh.tran0611csbk@hcmut.edu.vn |
        | password1   | hello1234@                     |
        | password2   | hello1234@                     |
        | phone       | 0321654987                     |
        | full name   | Tran Nguyen Thai Tuan          |
        | birth_year  | 2003                           |
        | birth_month | 11                             |
        | birth_day   | 06                             |
        Then I should see the error messages "A user is already registered with this email address."
