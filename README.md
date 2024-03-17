# Cinema back-end application

***
## Task Description
The assignment is about creating cinema’s application.
There are different cinema rooms: for example, red, blue, green, etc.
Different movies are shown in each room at the same time.
The schedule is different for each room. Each movie has its name and poster.
There are different available seats for each room. For example, consider row and seats 10 x 8.
User can click on the seat and book it. After refreshing the page that seat should become unavailable
during the period of the movie.
It should work like this:
There is list of rooms։
1. User clicks on a room;
2. User sees available movies (with title, date and time) for the selected room;
3. User clicks on a movie, after which user sees available and not available seats for the selected
movie.

Optional Please consider there should be admin portal for managing mentioned data (CRUD).
1. CRUD for rooms
2. CRUD for movies
Feel free to choose the fields of the CRUDs. Let me know if you need any additional information.

***

# Project description
Project built with FastAPI framework. It is providing REST API and supposed to work with any front-end framework which 
can camunicate with back-end REST API. 

## Project design
All schemas find [here](https://drive.google.com/file/d/1iL4Z97KCpndJmJWjzOTIHgV6RQWpLzcl/view?usp=sharing)

### Project models
Project have 4 models:
![](C:\Users\artyo\Downloads\cinema_application_scheme.svg)
- ROOMS: Rooms of cinema
- MOVIES: Movies would have sessions
- MOVIE_SESSIONS: Sessions of movies registered in cinema
- RESERVATIONS: Reserved places per session

### API structure

![](C:\Users\artyo\Downloads\cinema_application_scheme_api.svg)

### Project
***
### Steps for running service
***
## Installation:
### Local Setup
If you have cloned this repository and created a virtual environment for it. You can install all the dependencies by running:
``` bash
pip3 install -r requirements.txt
```

***
# Usage
## Running services
Run first (Client service)
``` bash
python -m cinema_application.uvicorn main:app --reload
```
Open ```http://127.0.0.1:8000/docs``` in a browser and test API locally

***
## Contributing guidelines
Thank you for following them!

### Branching strategy
Nothing new, nothing fancy:
* "Main" Branch:This is the primary branch that represents the production-ready version of the codebase. Developers 
should aim to keep this branch stable, and it should only contain code that has been fully tested and is ready
for release.

* "Development" Branch:This branch is used to integrate new code changes and features that are not yet production-ready.
Developers work on this branch to implement new functionality, fix bugs, and make improvements to the codebase. 
Once the changes are tested and validated, they are merged into the main branch for release.

* "Features" Branch:Feature branches are used to develop new features or major changes to the codebase. These 
branches are created off the development branch and allow developers to work independently on specific features 
without interfering with the development of other features.

* "Hotfixes" Branch:Hotfix branches are used to quickly address critical issues or bugs in the codebase that require
immediate attention. These branches are created off the main branch and allow developers to fix issues without
disrupting the development of new features on the development branch. Once the fix is complete, the hotfix branch is
merged back into the main branch.

### New features or refactorings
- Create a branch from development branch.
- Describe the changes you made and why you made them. If there is a JIRA task associated, please  write its reference.
- Implement your changes
- Ensure that the code is properly formatted and passes all existing tests. Create new tests for new methods or classes.
- Make sure to update the documentation if necessary
- Ask for a merge request to the development branch as soon as possible to avoid differences overlapping.

### CI/CD
#### Coverage
In this repo we are using coverage to check the code coverage of the tests. You can test it by running
``` bash
 coverage run -m pytest 
```
Then you can visualize the coverage report with:
``` bash
 coverage report
```
The highest the coverage the better! Also, make sure that every file is being covered.
Personally, if you are using Pycharm-Pro I recommend use the function "Run Python tests in tests with coverage" as it 
will allow you to see which lines are not under coverage.

## Future Work
- Add more unit and integration tests (by mocking requests and databases)
- Add more functionality for admins
- Optimize database queries