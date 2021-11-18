# Created by tmilieva at 10/26/2021
Feature: As a User
  I should be able to search for goods on platform

  Scenario: Search by text and verify response code is correct
    When Searching by text abc
    Then response code is 200

  Scenario: Search by text and verify correct items returned
    When search by text Asus rog g14 in category Ноутбуки
    Then all items have category Ноутбуки


