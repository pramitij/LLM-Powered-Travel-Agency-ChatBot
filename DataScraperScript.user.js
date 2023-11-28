// ==UserScript==
// @name         Enhanced Cruise Data Scraper
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://cruises.bestcruiserates.com/*
// @icon         none
// @grant        GM_getValue
// @grant        GM_setValue
// ==/UserScript==

(function() {
    'use strict';
    // Function to extract data from the HTML structure
 console.log("Script loaded");
    function extractData() {
            var cruises = document.querySelectorAll('.crCruiseBox');
            var data = [];

            cruises.forEach(function(cruise) {
                var cruiseData = {};

                // Extracting Star Rating
                var starRatingEl = cruise.querySelector('.crShipImage .stars');
                var starRating = starRatingEl ? starRatingEl.getAttribute('title').match(/[0-9.]+/)[0] : '3';
                cruiseData.starRating = starRating;

                // Extracting Cruise Line and Ship Name
                var vendorCruiseEl = cruise.querySelector('.crVendorCruise');
                if (vendorCruiseEl) {
                    var parts = vendorCruiseEl.textContent.split('•').map(part => part.trim());
                    cruiseData.cruiseLine = parts[0];
                    cruiseData.shipName = parts[1] || 'N/A';
                } else {
                    cruiseData.cruiseLine = 'N/A';
                    cruiseData.shipName = 'N/A';
                }

                // Extracting Ports Covered and Start/End City
                var portsEl = cruise.querySelector('.crPortList');
                var ports = portsEl ? portsEl.textContent.trim() : 'N/A';
                cruiseData.portsCovered = ports.replace(/, /g, ' | ');
                cruiseData.startEndCity = ports.split(',')[0].trim();

                // Extracting Departure Dates
                var departureDatesEl = cruise.querySelector('.crSailingDates');
                var departureDates = departureDatesEl ? departureDatesEl.textContent.trim().replace(/, /g, ' | ') : 'N/A';
                cruiseData.departureDates = departureDates;
                var insidePriceEl = cruise.querySelector('.cabinType.I .price');
                cruiseData.insidePrice = insidePriceEl ? insidePriceEl.textContent.trim() : 'N/A';

                var oceanViewPriceEl = cruise.querySelector('.cabinType.O .price');
                cruiseData.oceanViewPrice = oceanViewPriceEl ? oceanViewPriceEl.textContent.trim() : 'N/A';

                var balconyPriceEl = cruise.querySelector('.cabinType.B .price');
                cruiseData.balconyPrice = balconyPriceEl ? balconyPriceEl.textContent.trim() : 'N/A';

                var suitePriceEl = cruise.querySelector('.cabinType.S .price');
                cruiseData.suitePrice = suitePriceEl ? suitePriceEl.textContent.trim() : 'N/A';
                // Extracting Bonus Offers
                var bonusOffersEl = cruise.querySelector('.crBonusOffers ul');
                if (bonusOffersEl) {
                    var offers = Array.from(bonusOffersEl.querySelectorAll('li')).map(li => li.textContent.trim()).join(' | ');
                    cruiseData.bonusOffers = '"' + offers + '"';
                } else {
                    cruiseData.bonusOffers = '"Reduced Rates for Military Personnel and Seniors!"';
                }

                data.push(cruiseData);
            });

            return data;
        }

    // Function to save data to local storage
    function saveData(data) {
        var existingData = GM_getValue('cruiseData', []);
        existingData = existingData.concat(data);
        GM_setValue('cruiseData', existingData);
    }

    // Function to navigate to the next page
    function navigateToNextPage(currentPageNumber) {
        console.log("Step 3 next page")
        var nextPageNumber = currentPageNumber + 1;

        // If we haven't reached page 66 yet, navigate to the next page
        if (currentPageNumber >= 1 && currentPageNumber < 66) {
            var nextPageUrl = 'https://cruises.bestcruiserates.com/cs/forms/CruiseResultPage.aspx?skin=747&sort=10&nr=y&len=0%7c999&did=-1&mon=-1&pg=' + nextPageNumber;
            window.location.href = nextPageUrl; // Redirect to the next page URL
            GM_setValue('currentPage', nextPageNumber);
        } else if (currentPageNumber >= 66) {
            // If we've reached page 66, download the CSV and reset
            downloadCSV(GM_getValue('cruiseData', []));
            GM_setValue('cruiseData', []); // Reset data
            GM_setValue('currentPage', 1); // Reset to page 1
        }
    }


    // Function to initiate the scraping process
    function initiateScraping(currentPageNumber) {
        console.log("Step 2")
       var data = extractData();
    saveData(data);
    navigateToNextPage(currentPageNumber);
    }

    // Function to convert data to CSV
     function convertToCSV(arr) {
        const array = [Object.keys(arr[0])].concat(arr);
        return array.map(it => {
            return Object.values(it).toString();
        }).join('\n');
    }


    // Function to download CSV file
    function downloadCSV(data) {
        var csv = convertToCSV(data);
        var downloadLink = document.createElement('a');
        downloadLink.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
        downloadLink.download = 'cruise_data.csv';

        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
    }

    function delayInitiation() {
        const regex = /pg=(\d+)/;
        const found = window.location.href.match(regex);
        const currentPageNumber = found ? parseInt(found[1], 10) : 1;

        GM_setValue('currentPage', currentPageNumber); // Save the current page number

        console.log("Current Page:", currentPageNumber);
        initiateScraping(currentPageNumber);
    }

        window.addEventListener('load', function() {
            console.log("Page loaded");
            setTimeout(delayInitiation, 5000);
        });

})();
