# Solutions

## Finding the resources
As the description sugests, use the command `sherlock` for the given username.
`sherlock laurajohnsonbusiness`

Test the returned links: Instagram and Pastebin are valid users. From Instagram bio, find the X account.
Tasks: https://x.com/LauraJohns22375
Resources: https://pastebin.com/u/laurajohnsonbusiness

## Time Traveller
Reverse search the image and find the other pictures taken there. From the background (8 lane street, Place de la Concorde) and the advertisements in French => street is Champs-Elysees.
Also using reverse search, we can find the car brand and date in 1966. Some sources suggest other dates (like 1950 or 1962) but don't specify a date, or give incorrect information (such as, the date is 1950 and the author is Henri Roger-Viollet - deceased in 1946 https://www.facebook.com/Prpr28/posts/homme-poussant-une-vache-dans-un-bus-paris-1950photo-henri-roger-viollet/1085824063586031/).
Example sources:
https://www.retrochap.fr/site/2021/02/le-bus-la-vache/
https://www.bridgemanimages.com/en/noartistknown/cow-in-the-bus-in-paris-april-27-1966-advertisement-for-mailk-b-w-photo/black-and-white-photograph/asset/1655582
https://granger.com/0161751-vache-cow-in-the-bus-in-paris-april-27-1966--advertisement--image.html
https://www.gettyimages.com/detail/news-photo/pierrette-la-vache-ambassadrice-de-la-marque-de-lait-yolait-news-photo/1264066653

## GEOINT Specialist
The landmarks are: cinema (left hand side of the picture), station (right hand side of the picture and the story - "Going for a ride", task description) and hospital or clinic (from the story - "doctor's appointment").
Using Overpass Turbo (found in the Pastebin resources) under "GEOINT" category, we can query stations from Tokyo close to cinemas and hospitals.
For example, this script returns the correct station.
```
[out:json][timeout:300];

area["wikidata"="Q1490"]->.searchArea;

node[amenity=hospital](area.searchArea)->.hospitals;
node(around.hospitals:100)[amenity=cinema](area.searchArea)->.cinemas;
node(around.cinemas:200)[railway=station](area.searchArea)->.stations;

.stations out geom;
```
Similar scripts (using clinics or larger distance restrictions) reduce the number of candidates, which we can test using Google Streetview.
The location is 35.6661345 / 139.6415946 (lat/lon).

## Property Investigator
On https://osintframework.com/ in the Public Records section (as suggested by the comment hint) there is a Property Records section.

First, the cheapest condo for sale can be found using Zillow and a price filter.
https://www.zillow.com/homedetails/34-Cathedral-Ave-APT-5C-Hempstead-NY-11550/2076386384_zpid/

Searching for the zip code, we can find convicted offenders in that area. One of them is a resident of 34 Cathedral Avenue.
https://www.homefacts.com/zip-code/New-York/Nassau-County/Hempstead/11550.html
https://www.homefacts.com/offender-detail/NY29609/Andrew-Rose.html

From here, we can find the public offender registry, where the license plates are listed.
https://www.criminaljustice.ny.gov/SomsSUBDirectory/offenderDetails.jsp?offenderid=29609&lang=EN