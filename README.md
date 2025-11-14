# Goal Buddy

# Overview

This flask-based web app is designed to help you reach your goals, originally created for a class final project. Now it is being updated for fun as a side project.

Have you ever struggled with achieving a goal, no matter how much you wanted it?
The same way a gym buddy will keep you accountable for showing up for workouts, goal buddy will help you set SMART goals leveraging popular and effective goal-setting frameworks to set you up for goal-reaching success.

SMART goals are Specific, Measurable, Achievable, Relevant, and Time-bound.

Enter your goal and the estimated time to complete it, why you want to achieve it, break the big goal into smaller milestones, and let Goal Buddy help keep you on-track to reach each milestone until the goal is accomplished.

Let Goal Buddy help you reach your goals~

![App Login Page](./images/app-image.png)

## How to Use

1. **Deploy the application** using Docker Compose:

   ```bash
   docker compose up
   ```

2. **Access the app** at `http://localhost:5001`

3. **Register** a new account or log in.

4. **Create your first goal** by clicking "Create Goal" and filling in:

   - What is your goal?
   - Why do you want to achieve it?
   - What does success look like?
   - When do you want to achieve it?
   - Optional: Lock the date for accountability

5. **Add milestones** to break your goal into smaller, achievable steps with rewards.

6. **Track your progress** by marking milestones and goals as complete.

7. **Stay motivated** with inspirational quotes that appear on every page.

# Design

## User Stories

### User Story #1:

As a logged-in user, I want to enter a big goal and goal due date so that I can plan more effectively to reach an intimidating goal within a specific timeframe.

Given that the logged-in user has provided a goal and date, when they click enter then they are taken to a page to explore their goal's why and ensure they have set a goal with a specific/measurable outcome.

### User Story #2:

As a user setting a goal, I want to know what achieving my goal looks like and stay motivated so that I can eventually reach my goal.

Given that the user has set a specific/measurable goal and explained why they want to acheive it, when they click submit they should be prompted with questions to set specific time each day or week to work towards it.

### User Story #3:

As a user setting a goal, I want to break the goal into smaller, achievable milestones with specific milestone due dates and rewards/celebrations so that I can make measurable progress towards the big goal.

Given that the user has provided at least one smaller milestone that will contribute to reaching their big goal and a milestone due date and reward/celebration, when they select 'set goal' they should be redirected to their profile page and see the goal there.

### User Story #4:

As a logged-in user who has set a goal, I want to update/edit my goal progress so that I can stay on track or adjust my goal timeline.

Given that the user has provided a goal, goal due date, why they want to reach that goal, a designated time/day to work towards it, and at least one milestone, when they select edit or update goal then they should be directed to a page where they can edit the goal or update their progress.

### User Story #5:

As a logged-in user who has set a goal, I want to update/edit my goal progress so that I can stay on track or adjust my goal timeline.

Given that the user has provided a goal, when they are on their profile page then they should be able to delete a goal they previously set.

### User Story #6:

As a logged-in user, I want to get motivated so that I can keep working toward my goal.

Given that I go to the motivation page, when I start a chat then I should get motivational quotes and tips generated.

## Sequence Diagram

### New Goal Sequence Diagram

![New Goal Sequence Diagram Image](./uml/diagram-images/new-goal-sequence.png)

### Edit Goal Sequence Diagram

![Edit Goal Sequence Diagram Image](./uml/diagram-images/edit-goal-sequence.png)

## Model

### Class Diagram

![Class Diagram Image](./uml/diagram-images/class-diagram.png)

### Use-Case Diagram

![Use-Case Diagram Image](./uml/diagram-images/use-case.png)

# Development Process

This section should be used to describe how the scrum methodology was used in this project. As a suggestion, include the following table to summarize how the sprints occurred during the development of this project.

There are 6 Phases: (1) Planning, (2) Development, (3) Testing, (4) Polishing, (5) Deployment & Orchestration, (6) DB Migration.

| Sprint# | Goals                               | Start          | End            | Done                                                                                                         | Observations                                                                                                    |
| ------- | ----------------------------------- | -------------- | -------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| 1       | Phase 1 Pt 1: Planning              | 05/03/24       | 05/10/24 15:00 | Readme, dev timeline                                                                                         | Planning seemed like it would be easy, but the relative freedom of the assignment resulted in choice-paralysis. |
| 2       | Phase 1 Pt 2: Diagrams              | 05/03/24 15:00 | 05/10/24 16:00 | Completed class diagram, use-case, new-goal sequence, and edit-sequence diagrams                             | Diagrams complete.                                                                                              |
| 3       | Phase 2 Pt 1: Baseline App          | 05/10/24 16:00 | 05/10/24 18:00 | Baseline App, using SQLite for testing, minimize complexity                                                  | ...                                                                                                             |
| 4       | Phase 2 Pt 2: US#1, US#2, US#3      | 05/10/24 18:00 | 05/10/24 20:00 | US#1, US#2, US#3                                                                                             | ...                                                                                                             |
| 5       | Phase 2 Pt 3:US#4, US#5             | 05/10/24 20:00 | 05/10/24 22:00 | US#4, US#5                                                                                                   | ...                                                                                                             |
| 6       | Phase 2 Pt 4: US#6                  | 05/10/24 22:00 | 05/11/24 00:00 | US#6                                                                                                         | ...                                                                                                             |
| 7       | Phase 3: Testing                    | 05/11/24 08:00 | 05/11/24 10:30 | Implement white box [unit tests] and black box [Selenium] tests, generate testing coverage statement         | ...                                                                                                             |
| 8       | Phase 4: Polishing                  | 05/11/24 10:30 | 05/11/24 13:00 | Refine CSS, pages, and add CSS animations                                                                    | ...                                                                                                             |
| 9       | Phase 5: Deployment & Orchestration | 05/11/24 13:00 | 05/11/24 14:30 | Set up Docker and Docker Compose                                                                             | ...                                                                                                             |
| 10      | Phase 6: DB Migration               | 05/11/24 15:00 | 05/11/24 16:00 | Migrate to postgres, chose to migrate so postgres service being up or down would not impact project progress | ...                                                                                                             |

# Testing

The project includes comprehensive unit and integration tests to ensure code quality and functionality.

## Test Coverage

Current test coverage: **87%**

| Module              | Statements | Missing | Coverage |
| ------------------- | ---------- | ------- | -------- |
| src/app/**init**.py | 30         | 0       | 100%     |
| src/app/config.py   | 5          | 0       | 100%     |
| src/app/forms.py    | 42         | 0       | 100%     |
| src/app/models.py   | 56         | 1       | 98%      |
| src/app/quotes.py   | 4          | 0       | 100%     |
| src/app/routes.py   | 196        | 42      | 79%      |
| **TOTAL**           | **333**    | **43**  | **87%**  |

## Test Suite

The test suite includes 58 tests covering:

### Unit Tests (test_models.py)

- User model: password hashing, user creation, goal queries
- Goal model: creation, date locking, completion toggle
- Milestone model: creation, relationships with goals

### Form Validation Tests (test_forms.py)

- LoginForm: username/password validation
- RegistrationForm: duplicate detection, email validation, password confirmation
- GoalForm: required fields, date locking
- MilestoneForm: required fields validation

### Integration Tests (test_routes.py)

- Authentication: login, logout, registration flows
- Goal CRUD: create, read, update, delete operations
- Milestone CRUD: full lifecycle management
- Error handling: 404 responses for invalid resources

### Additional Tests (test_quotes.py)

- Quote system functionality
- Muhammad Ali quote inclusion verification

## Running Tests

To run the test suite with coverage:

```bash
python3 -m pytest tests/ --cov=src/app --cov-report=term --cov-report=html
```

HTML coverage report is generated in `htmlcov/` directory.
