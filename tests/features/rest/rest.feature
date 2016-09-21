Feature: REST requests
    In order to play with Lettuce
    As beginners
    We'll implement factorial

    Scenario: Request groups from REST
        Given I query /groups/
        I receive result

    Scenario: Request groups from REST
        Given I query /repositories/
        I receive result
        And I have the following in results:
        | name           |
        | testing        |
        | gitolite-admin |
