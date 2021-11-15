# Created by tmilieva at 10/29/2021
Feature: Factory Pattern: As a User I should be able to search for goods

  Scenario: Search by text
    Given main page opened
    When search by text abc
    Then search results page contains correct header

  Scenario: Search by existing item and check correct result returned
    Given main page opened
    When search by text Ноутбук MSI Creator Z16 (A11UE-084UA) Grey
    Then search results page contains correct amount of items

  Scenario: Search by producer and check correct result returned
    Given main page opened
    When search by text Asus
    Then filter Asus is selected in filter panel

  Scenario: Search by multiple producers and check filter functionality
    Given main page opened
    When search by text Ноутбук
    And select filters Asus, Acer in filter panel
    Then filter Asus is selected in filter panel
    Then filter Acer is selected in filter panel

  Scenario: Search by price range and category
    Given main page opened
    When search by text Asus
    When set min price in filter panel to 5000
    And set max price in filter panel to 10000
    And apply search by price
    And select category Ноутбуки
    Then search results page contains correct amount of items


  Scenario: Validate price
    Given main page opened
    When search by text Asus rog g14
    And select category Ноутбуки
    Then check item price with discount is correct
    Then check item price without discount is correct