# Goal Buddy

# Overview

This flask-based web app is designed to help you reach your goals. 

Have you ever struggled with achieving a goal, no matter how much you wanted it? 
The same way a gym buddy will keep you accountable for showing up for workouts, goal buddy will help you set SMART goals leveraging popular and effective goal-setting frameworks to set you up for goal-reaching success. 

SMART goals are Specific, Measurable, Achievable, Relevant, and Time-bound. 

Enter your goal and the estimated time to complete it, why you want to achieve it, break the big goal into smaller milestones, and let Goal Buddy help keep you on-track to reach each milestone until the goal is accomplished. 

Have multiple goals? No problem! Goal Buddy enables you to prioritize and re-prioritize.

Let Goal Buddy help you reach your goals~

# Design

## User Stories

Describe the user stories designed for the project, including clear acceptance criteria and point estimate for each of them. User stories must be consistent with the use case diagram. Refer to the user stories using US#1, US#2, etc. At least one of the user stories, not related to user creation or authentication, must be detailed by a sequence diagram. 

### User Story #1: 
As a logged-in user, I want to enter a big goal and goal completion date so that I can plan more effectively to reach an intimidating goal within a specific timeframe. 

Given that the logged-in user has provided a goal and date, when they click enter then they are taken to a page to help break the big goal down into smaller milestones.

### User Story #2:
As a user setting a goal, I want to succeed on taking steps toward my goal even when the motivation isn't there so that I can eventually reach my goal.

Given that I am setting a big goal, when I set a goal and goal date then I should be prompted with questions to better connect with why I want this goal and set a specific time each day or week to work towards it.

### User Story #3: 
As a user setting a big goal, I want to break the goal into smaller, achievable milestones so that I can make measurable progress towards the big goal.

Given that I have provided a goal and goal time and why, when I proceed in setting my goal then I should be prompted to set smaller milestones, set goal dates for each milestone, and rewards for when they are achieved.

### User Story #4:
As a logged-in user who has set a goal, I want to update my goal progress so that I can stay on track or adjust my goal timeline.

Given that I am on my goals page, when I select edit or update goal then I should be directed to a page where I can edit the goal or update my progress.

### User Story #5:
As a logged-in user who has set multiple goals, I want to re-prioritize so that I can keep focused on the most important goal while [hopefully] making some progress towards the less-important goals.

Given that [context], when [some action is carried out] then [a set of observable outcomes should occur].

### User Story #6: 
As a logged-in user, I want to [perform some task] so that I can [achieve some goal].

Given that [context], when [some action is carried out] then [a set of observable outcomes should occur].

## Sequence Diagram

At least one user story, not related to user creation or authentication, must be detailed using a sequence diagram.

## Model 

At a minimum, this section should have a class diagram that succinctly describes the model classes used in the project, including their associations.

# Development Process 

This section should be used to describe how the scrum methodology was used in this project. As a suggestion, include the following table to summarize how the sprints occurred during the development of this project.

There are 6 Phases: (1) Planning, (2) Development, (3) Testing, (4) Polishing, (5) Deployment & Orchestration, (6) DB Migration.

|Sprint#|Goals|Start|End|Done|Observations|
|---|---|---|---|---|---|
|1|Phase 1 Pt 1: Planning |05/03/24|05/10/24 15:00|Readme, dev timeline |Planning seemed like it would be easy, but the relative freedom of the assignment resulted in choice-paralysis.|
|2|Phase 1 Pt 2: Diagrams |05/03/24 15:00|05/10/24 16:00|...|
|3|Phase 2 Pt 1: Baseline App |05/10/24 16:00|05/10/24 18:00|Baseline App, using SQLite for testing, minimize complexity|...|
|4|Phase 2 Pt 2: US#1, US#2, US#3 |05/10/24 18:00|05/10/24 20:00|US#1, US#2, US#3|...|
|5|Phase 2 Pt 2:US#4, US#5 |05/10/24 20:00|05/10/24 22:00|US#4, US#5|...|
|6|Phase 2 Pt 2: US#6 |05/10/24 22:00|05/11/24 00:00|US#6|...|
|7|Phase 3: Testing |05/11/24 08:00|05/11/24 10:30|Implement white box [unit tests] and black box [Selenium] tests, generate testing coverage statement|...|
|8|Phase 4: Polishing |05/11/24 10:30|05/11/24 13:00|Refine CSS, pages, and add CSS animations |...|
|9|Phase 5: Deployment & Orchestration |05/11/24 13:00|05/11/24 14:30|Set up Docker and Docker Compose|...|
|10|Phase 6: DB Migration |05/11/24 15:00|05/11/24 16:00|Migrate to postgres, chose to migrate so postgres service being up or down would not impact project progress |...|

Use the observations column to report problems encountered during a sprint and/or to reflect on how the team has continuously improved its work. If you prefer, you can use the same format used in the project 2 (sprint markdown files). 

# Testing 

Share in this section the results of the tests performed to attest to the quality of the developed product, including the coverage of the tests in relation to the written code. There is no minimum code coverage expectation for your tests, other than expecting "some" coverage through at least one white-box and one black-box test.

# Deployment 

The final product must demonstrate the integrity of at least 5 of the 6 planned user stories. The final product must be packaged in the form of a docker image. The project should be able to be deployed using: 

```
docker compose up
```
