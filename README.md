# Wedding Management Project

This Flask web app is built for the purpose of planning and managing my wedding.
Architeturally, it is divided into two parts:
* an admin interface to allow for myself and my partner to manage guests, costs, invitations and any extras.
* an interface for the wedding guests to have access to information about the wedding, local hotels etc, and additional features for the day itself.


## The project is *currently* a work in progress


# Project Requirements and Considerations

The original intention was for this project to simply be a web application to allow guests to upload photos on the wedding day. Further thought and consideration has led to an extension to allow for myself and my partner (admins) to manage all of the essentials beforehand. Additional features will also be implemented on the user side (guests), notably, utilising the Spotify API for music selection at the wedding (still to be considered, planned and implemented).

Additionally, the wedding will have Romanian guests, so dynamic language selection will later be implemented.


## Architectural Considerations

* The wedding guests can be sub-divided into numerous different 'types'. The database should therefore reflect this, and allow for admins to choose which of these any given guest falls into. For some, the guest type should also be updated by the user (eg their intention to attend):
    * English / Romanian
    * Evening / Day
    * Have / Have Not RSVPed
    * Intention to attend

* Guests may also be invited as part of a group eg a family, or with additional guests (eg a +1). I was unsure how I should store the details of these guests i.e. whether I should have the user register the details of their related guests (in a dictionary for example). Ultimately, I decided that the complexity of doing so would not render sufficient benefit, and would likely make the UX worse anyway. +guests are therefore stored simply as strings in the database. Although I may revisit this later. The related guests are calculated in the costings on the admin side however.

* Aside from guest management, the other major consideration was budget management. The admin dashboard has functionalities to add/edit/delete wedding costs. All of these besides the cost of guests are stored in a single `Expenses` database table, identified by their `cost_type`. All costs are calculated in the admin dashboard.


## UX Considerations

* Some of the guests are of Romanian nationality, so the app will need to allow content to be displayed in that language. This will be implemented by having the guests stored in the database with a 'language' column, and all user-facing pages will be separated by language so that the appropriate page can be easily rendered from the appropriate pages folder, eg: `return render_template('f{current_user.language}/page_name.html')`

* As the web app is a personal endeavour, email should not be relied upon for communication, logging in etc. The app therefore uses (or will use) the Twilio API to send invitations, alerts, and allow users to log in with their mobile phone number, as well as allowing the same via email.

* Currently, I am undecided as to whether or not guests should have to log in before seeing relevant content. Considerations about the privacy of the wedding encourage me to have most content restricted to logged in users, however, this may be a restrictive UX for our guests.

* Guests are divided into evening guests and full-day guests. This information is stored as a `guest_type` column in the `Users` database table. Content should be accordingly relevant (i.e. evening guests should not be informed about the ceremony procedures).


## To Do

### User-Facing

*  Build out the user front-end:

    ~~* login functionality.~~

    ~~* list local hotels (hard-coded).~~

    ~~* contact form.~~ Not necessary as guests can contact us directly.

    ~~* provide details about the wedding itself - times, venue etc.~~

    ~~* photo upload and gallery viewing functionalities (can be added much later)~~

    * Spotify API for song selection (can be added much later)


### Admin

* Clean up and extend the admin front-end:

    * Better styling

    * Rigorously test all functionalities

    ~~* Add contact form to allow communication with guests (a number of variables to determine *which* guests receive messages eg by language, whether they are evening/day, those that are unsure of their attendance etc.)~~


## Project Workflow


* The admin side of the app is built first, allowing myself and my partner to manage guests, budget etc.

* The basis of the communication functionalities have been built, but need extending

* The user-facing front-end is yet to be built and will follow the below flow:

    * User login

    * Functionality to allow guests to gift money instead of wedding gifts

    * Basic information about the wedding - date, times, venue etc

    * Contact Us functionalities

    * List local hotels

    * Photo uploads

    * Spotify API

