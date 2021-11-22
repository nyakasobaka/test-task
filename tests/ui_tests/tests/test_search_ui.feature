# Created by tmilieva at 10/29/2021
Feature: As a User I should be able to search for goods

  Scenario: Search by text
    Given main page opened
    When enter text abc into search field
    Then click search button
    Then search results page contains correct header

  Scenario: Search by existing item and check correct result returned
    Given main page opened
    When enter text Ноутбук MSI Creator Z16 (A11UE-084UA) Grey into search field
    Then click search button
    Then search results page contains correct amount of items

  Scenario: Search by producer and check correct result returned
    Given main page opened
    When enter text Asus into search field
    Then click search button
    And select producers Asus in filter panel
    Then filter Asus is selected in filter panel

  Scenario: Search by multiple producers and check filter functionality
    Given main page opened
    When enter text Ноутбук into search field
    And click search button
    And select producers Asus, Acer in filter panel
    Then filter Asus is selected in filter panel
    Then filter Acer is selected in filter panel

  Scenario: Search by price range and category
    Given main page opened
    When enter text Asus into search field
    And click search button
    When set min price in filter panel to 5000
    And set max price in filter panel to 10000
    And apply search by price
    And select category Ноутбуки
    Then search results page contains correct amount of items


  Scenario: Validate price
    Given main page opened
    When enter text Asus rog g14 into search field
    And click search button
    And select category Ноутбуки
    Then check item price with discount is correct
    Then check item price without discount is correct