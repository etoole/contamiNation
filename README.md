# contamiNation

## What is this? What does it mean?

This map was created in order to make localized data on lead contamination of United States public water sources available to the public. Such contamination stems from corrosion of old lead and copper plumbing fixtures that may be part of a building’s plumbing or the public water system’s service line.<sup>[[1]](https://www.epa.gov/lead/protect-your-family-exposures-lead#water)</sup> Contamination in a public water system may affect residents of a single building or those of an entire municipality.

Ingestion of lead has been known for millennia to cause serious harm to the neurological system, even in barely detectable amounts.<sup>[[2]](https://www.karger.com/Article/FullText/98100)</sup> The human body does not have a mechanism to process lead and remove it as waste. Instead it bio-accumulates in the brain and causes permanent harm to mental faculties in proportion to the amount present in the body. For this reason, even a miniscule amount in drinking water can have serious effects over a long period of regular consumption.<sup>[[3]](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1497727/pdf/16134575.pdf)</sup> These effects are especially pronounced in children and can cause lifelong damage.<sup>[[4]](https://www.epa.gov/lead/learn-about-lead#effects)</sup><sup>[[5]](https://www.cdc.gov/nceh/lead/ACCLPP/Lead_Levels_in_Children_Fact_Sheet.pdf)</sup> In view of this, the Environmental Protection Agency (EPA) has mandated that a concentration of 15 mg/L (parts-per-billion) of Lead and 1300 mg/L (parts-per-billion) of Copper be deemed an ‘action level’. Detections above this level demand that corrective action be taken in the form of water treatment, replacement of pipes, or in other forms. In addition, regular monitoring of Lead and Copper concentrations are made until the concentration of contaminants falls below the action level.<sup>[[6]](https://www.epa.gov/dwreginfo/lead-and-copper-rule)</sup>

On the map, public water systems are clustered in the blue circular markers with the number of markers printed in black in order to avoid visually cluttering the map. If you zoom in or click on the blue circular marker, you will be able to view individual public water systems. These are represented by color-coded faucet icons. A <span style="color:red"> red faucet</span> indicates that the public water system is out of compliance and that its highest recorded concentration of lead or copper since the system was deemed out of compliance with the Lead and Copper Rule was above the action level. A <span style="color:#f4d742">yellow faucet</span> indicates that the public water system is out of compliance and that lead has been detected in concentrations below the action level since it was deemed out of compliance with the Lead and Copper Rule. A <span style="color:green">green faucet</span> indicates that the public water system has returned to compliance or that Lead or Copper have never been detected. The map was designed to intentionally bring attention to those ‘yellow faucet’ systems where lead has been detected but has not risen above the action level. Because tap water is used in so many ways and so much of it is consumed in the household, no level of lead contamination should be considered safe.

Finally, the contact information for your local public water service administrator is provided. If you are in an area with contaminated public water, please consider contacting these people to voice your outrage and improve the health of your community.
 
 

## How was this made?

The data for this project was compiled from various reports requested through the EPA’s [Safe Drinking Water Information System (SDWIS) Federal Reports Advanced Search](https://ofmpub.epa.gov/apex/sfdw/f?p=108:1:::NO::P1_REPORT:WS).  From this data portal, three types of reports were required to retrieved the complete data. The site data was pulled from Water System Reports; locational information (such as the city and state) and contact information for the manager of the public water system were taken from the Water System Detail Report; and results of chemical analysis for Lead and Copper concentrations were pulled from the Lead and Copper Reports. All of the reports for a sampling period ending on New Years Eve 2014 or later were retrieved, giving an effective coverage date of mid-2014 to the present. 

The data was then compiled with a series of python scripts that joined the data from each reports using the public water systems ID number as a key. Unwanted data was culled and usable data was reformatted in a dictionary container for each of the public water system. Another python script was used to compare the date of each concentration result to the date the system returned to compliance and then to find the highest result that occurred after the return to compliance and code it as <span style="color:green">clean (green)</span>, <span style="color:#f4d742">below action level (yellow)</span>, or <span style="color:red">above action level (red)</span>above action level (red). Because longitude and latitude coordinates were not supplied by the EPA, I geocoded the sites using the available locational information (place name, city, state, zip code) using [GoogleMaps API](https://developers.google.com/maps/). To handle the quantity of data, it was necessary to make API requests through a separate python script. Initially, this did not produce very reliable results because of the poor quality of place name data supplied. In order to introduce some degree of quality control, I compared the first three digits of the EPA-supplied zip code with that returned by GoogleMaps. If there was a match, the geocoded coordinates and address would be used. If no match occurred, I made a separate geocoding request for the coordinates and address of the center of the EPA-supplied zipcode and used these results in the data. The coordinates, concentrations, contact information, public water system name & id, and compliance status were then formatted into a [geoJSON format](http://geojson.org/) which would be readable by the mapping software used on the website. This created a single JSON file which contained all of the data for the **20,066** markers for public water systems. Click [here](https://github.com/etoole/contamiNation) to view the github repository for the data wrangling portion of this project.

The site was created using a [Jekyll](https://jekyllrb.com/) web-page template called Material that was forked from [Alex Carpenter’s Github repository](https://github.com/alexcarpenter/material-jekyll-theme). After stripping the page of content and extraneous pages, I added an empty map using the [Leaflet](http://leafletjs.com/) cartographic JavaScript library and imported a map tileset that included satellite images and streets from [MapBox](https://www.mapbox.com/). I then made a request for the JSON file and pinned a color-coded [Maki icon](https://www.mapbox.com/maki-icons/) for each of the water systems and added the relevant data to a popup. With 20,000+ objects on the map, it was very slow to load and very difficult to visually interpret. So, I used a Leaflet plugin called [MarkerCluster](https://github.com/Leaflet/Leaflet.markercluster) to group proximate markers together and drastically lighten the burden of visual elements displayed on the page. 
