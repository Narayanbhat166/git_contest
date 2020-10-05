# About the application

This application is developed on the flask framework, uses the github api to track the changes to users repositories and codes, updates the score on the leaderboard 

## What a user needs to know
* Enter the contest using your github link, choosing any one of the teams
* There will be checkpoints to cross, each one rewarded with points which helps the user to rise up on the leaderborad and exhibit his skills
* User has to complete some checkpoints in website and others in commandline(quiz questions)
* encourage team members to complete the checkpoints to rise up in team leaderboard

## What a developer needs to know
* The modifications in the repository are checked by the backend logic, which uses github api to pull information about the user
* there is a route for each checkpoint
* quiz questions does not involve the request to api

## Outcomes
* We had the github event in our college(conducted by Linux Campus Club), many users registered(50+) to this contest and completed all the checkpoints.

## Few screenshots
![The final leaderboard](/screenshots/leaderboard1.png)
![Register Page](/screenshots/register_page.png)
![Leaderboard](/screenshots/leaderboard2.png)
![Leaderboard](/screenshots/leaderboard3.png)
