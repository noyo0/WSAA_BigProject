# WSAA 2024 - End of Semester Project (Truckwash)  
**Author:** Norbert Antal  

**Assignment brief:**  
*"Write a program that demonstrates that you understand creating and consuming RESTful APIs."*  

# Truckwash Admin Web Application Project  

This **WSAA final project** aims to demonstrate my understanding of creating and consuming RESTful APIs. Using Flask, HTML, JavaScript, AJAX, and Python, I've developed a simple but functional web application for managing the activities of a HGV wash service.

## *(🤞) This project has an online version hosted on [pythonanywhere.com](https://noyo0.pythonanywhere.com/).*

## Key Features  

The Truckwash web application is designed to assist in managing washing records for an HGV wash service, offering the following basic features:

- Providing monthly cost summaries by customers and equipment types along with simple data visualization.
- Recording wash activities from a fleet list or from a custom form for third-party equipment.
- Viewing and editing wash history.
- Deleting entries.
- Access to a simple fleet list.

## Under the Hood  

This web application operates with a combination of multiple programming environments to view and manipulate a database of multiple data tables: *eq_table* contains a static fleet list, *rates* contains the various prices assigned to each equipment type in the fleet, and *truckwash* as the main data table to record wash activities as per user interactions.

- **Backend:** Handled by Flask, a Python backend manages HTML routing and CRUD operations.
- **Database Integration:** A Python-based Data Access Object manages the interactions with the MySQL database.
- **Frontend:** With a simple four-page structure, built with HTML, JavaScript, and AJAX, using Bootstrap components, SweetAlert2 popup boxes, and Plotly.js data visualization, the frontend provides a dynamic user interface.

## User interface  

All pages have a top and bottom menu to navigate between the pages.

- **Home**:  
  - The home page has a data visualization section from a combined MySQL query accessing entries in the *truckwash* and *rates* data tables summarized and grouped by month and customer with a bar chart for cost summary. The same is also rendered in a data matrix. A *Details* button toggles a more detailed cost summary visible/hidden that extends the summary with a breakdown by equipment type. The *Trends* button changes the bar chart to a line chart and the *Cost* button back to a bar chart.
  
- **Wash history**:  
  - This is a list of all recorded washes from the *truckwash* data table complete with the appropriate rates pulled from the *rates* data table. Each row has a Change and Delete function with a SweetAlert2 popup verification. Displayed as a paginated list, arranged by Date, rendering 20 rows each time with a Prev/Next button.
  
- **Add Wash**:  
  - This page is designed for the main function of the web application, providing easy access for the user to review and manipulate truckwash data. The top *Recently Added* section contains the last 5 entries added to the *truckwash* data table. This view refreshes with each change, so the user can prevent double/false entry. Each row has a Change and Delete function with a popup verification.  
  - The bottom section *Add from fleet* reads in a fleet list from *eq_table* with a dynamic search box that filters the contents of the fleet list based on FleetNumber. Each row has an *Add Wash* function which opens a SweetAlert2 popup where the wash data can be verified before saving the new wash entry. Next to the filter located a *Not in Fleet* button for equipment that is not on the fleet list. This button toggles the *Add Third Party* section visible where the user can manually add the Date, FleetNumber, Reg, and equipment type. The valid equipment types are selected from a dropdown so the appropriate rates can be assigned.
  
- **Fleet List**:  
  - This is a paginated fleet list, 20 rows each time with a Prev/Next button.

## Requirements/Dependencies  

### Server dependencies
- Flask==3.0.3 - https://flask.palletsprojects.com/en/3.0.x/
- mysql-connector-python==8.4.0 - https://dev.mysql.com/doc/connector-python/en/
*Full list of Python dependencies stored in requirements.txt.*

Alternatively, a virtual environment for managing server-side dependencies is also included (run: venv/bin/activate).

### Online dependencies (*This web app requires an internet connection*)
- Bootstrap CSS - https://getbootstrap.com/
- Roboto Font - https://fonts.google.com/specimen/Roboto
- jQuery(AJAX) - https://api.jquery.com/jQuery.ajax/
- SweetAlert2 - https://sweetalert2.github.io/
- Plotly.js - https://plotly.com/javascript/


## The online version of this project is hosted at [noyo0.pythonanywhere.com](https://noyo0.pythonanywhere.com/).