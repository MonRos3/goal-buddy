# Goal Buddy

# Overview

This flask-based web app is designed to help you reach your goals. 

Have you ever struggled with achieving a goal, no matter how much you wanted it? 
The same way a gym buddy will keep you accountable for showing up for workouts, goal buddy will help you set SMART goals leveraging popular and effective goal-setting frameworks to set you up for goal-reaching success. 

Enter your goal, the estimated time to complete it, break the big goal into smaller milestones, and let goal buddy help keep you on-track to reach each milestone until the goal is accomplished. 

Have multiple goals? No problem! Goal buddy enables you to prioritize and re-prioritize.

Use this section to outline the vision for the product to be developed, including a use case diagram that shows the main user interactions with the product, in order to provide readers with an overview of the project.

# Design

## User Stories

Describe the user stories designed for the project, including clear acceptance criteria and point estimate for each of them. User stories must be consistent with the use case diagram. Refer to the user stories using US#1, US#2, etc. At least one of the user stories, not related to user creation or authentication, must be detailed by a sequence diagram. 

US#1: As a logged-in user, I want to enter a big goal and goal completion date so that I can plan more effectively to reach an intimidating goal within a specific timeframe. 

Given that the logged-in user has provided a goal and date, when they click enter then they are taken to a page to help break the big goal down into smaller milestones.

US#2: As a user setting a big goal, I want to dafs so that I can [achieve some goal].

Given that [context], when [some action is carried out] then [a set of observable outcomes should occur].

US#3: As a logged in user who has entered a goal and date, I want to break the goal into smaller, achievable milestons so that I can make measurable progress towards the big goal.

Given that [context], when [some action is carried out] then [a set of observable outcomes should occur].

US#4: As a logged-in user, I want to [perform some task] so that I can [achieve some goal].

Given that [context], when [some action is carried out] then [a set of observable outcomes should occur].

US#5: As a logged-in user, I want to [perform some task] so that I can [achieve some goal].

Given that [context], when [some action is carried out] then [a set of observable outcomes should occur].

US#6: As a [type of user], I want to [perform some task] so that I can [achieve some goal].

Given that [context], when [some action is carried out] then [a set of observable outcomes should occur].

## Sequence Diagram

At least one user story, not related to user creation or authentication, must be detailed using a sequence diagram.

## Model 

At a minimum, this section should have a class diagram that succinctly describes the model classes used in the project, including their associations.

# Development Process 

This section should be used to describe how the scrum methodology was used in this project. As a suggestion, include the following table to summarize how the sprints occurred during the development of this project.

|Sprint#|Goals|Start|End|Done|Observations|
|---|---|---|---|---|---|
|1|US#1, US#2, ...|mm/dd/23|mm/dd/23|US#1|...|

Use the observations column to report problems encountered during a sprint and/or to reflect on how the team has continuously improved its work. If you prefer, you can use the same format used in the project 2 (sprint markdown files). 

# Testing 

Share in this section the results of the tests performed to attest to the quality of the developed product, including the coverage of the tests in relation to the written code. There is no minimum code coverage expectation for your tests, other than expecting "some" coverage through at least one white-box and one black-box test.

# Deployment 

The final product must demonstrate the integrity of at least 5 of the 6 planned user stories. The final product must be packaged in the form of a docker image. The project should be able to be deployed using: 

```
docker compose up
```
