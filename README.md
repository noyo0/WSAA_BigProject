# WSAA 2024 - End of Semester Project (Truckwash) Author: Norbert Antal

## online version hosted on pythonanywhere.com: <br> https://noyo0.pythonanywhere.com/

Assignment brief:<br>*"Write a program that demonstrates that you understand creating and consuming RESTful APIs."*

# Truckwash Admin Web Application Project

Welcome to my **WSAA final project**, aimed at demonstrating my understanding of creating and consuming RESTful APIs.
Using Flask, HTML, JavaScript, AJAX, and Python, I've developed a simple yet functional web application for managing the activities of a Truckwash service.

## Key Features

This application aims to assist in managing truck washing records, offering the following basic features:

- Providing cost summaries by customers and equipment types complemented by simple data visualizations.
- Adding new wash records from a fleet list or from a separate form for third-party equipment.
- Viewing and editing wash history.
- Deleting outdated entries.
- Access to a simple fleet list.

## Under the Hood

This application operates using a combination of powerful technologies and methodologies:

- **Backend:** Handled by Flask, the Python backend manages HTML routing and CRUD operations
- **Database Integration:** A Python based Data Access Object manages the interactions with a MySQL database.
- **Frontend:** With a simple four-page structure, built with HTML, JavaScript, and AJAX, using Bootstrap components and SweetAlert2 popup boxes and Plotly.js data visualization the frontend provides a dynamic user interface.

## User interface
All pages have a top and bottom menu to navigate between the pages.

+ **Home**
    - The home page has a data visualization section with a bar chart for cost summary per customer per month. The same is also rendered in a date table. A *Details* button toggles a more detailed cost summary visible/hidden. The *Trends* button changes the bar chart to a line chart and the *Cost* button back to bar chart. 
+ **Wash history**
    - This is a list of all recorded washes complete with the appropriate rates pulled from a separate *rates* data table. Each row has a Change and Delete function with a popup verification. Paginated list, arranged by Date, displaying 20 rows each time with a Prev/Next button.
+ **Add Wash**
    - This page is designed for the main function of the web application, providing easy access for the user to review and manipulate truckwash data. The top section *Recently Added* contains the last 5 entries added to the *truckwash* data table. This view refreshes with each change, so the user can prevent double/false entry. Each row has a Change and Delete function with a popup verification. <br>The bottom section *Add from fleet* has a reads in a fleet list from SQL data table with a dynamic search box that filters the contents of the fleet list based on FleetNumber. Each row has an *Add Wash* function which opens a popup where the wash date can be verified before saving the new wash entry. There is a *Not in Fleet* button for equipment that is not on the fleet list. This button toggles the *Add Third Party* section visible where the user can manually add the Date, FleetNumber, Reg and equipment type. 
+ **Fleet List**
    - This is a paginated fleet list, 20 rows each time with a Prev/Next button.
