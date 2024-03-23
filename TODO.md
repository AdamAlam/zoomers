# LetterBoxd Clone

## Frontend

- [ ] Create and add component to movie detail to show all reviews for that movie/tv show
- [x] Create stars component to submit rating (should replace select component)
- [ ] If review has been submitted for a specific movie, we should change `Submit New Review` to `Edit Review` and POST/PUT to a different route
- [ ] Create login page
- [x] Hook up sign up page to make correct request to backend for creating new user
- [x] Configure form validation with Zod

## Backend

- [ ] Create backend routes pertaining to movies
  - [ ] Search for a specific movie
  - [ ] Search for a specific TV Show
  - [x] Follow User
  - [x] Unfollow User
  - [ ] Get all reviews of followed users
  - [ ] Get all of own reviews
  - [x] Get all reviews of specific movie/tv show
  - [x] Create backend route to get the average rating for a movie/tv show
  - [x] Create validation function that accepts JWT and validates users

## Misc

- [] Determine which user is logged in after auth. We should consider not using OAuth for now so that we have more control over user auth
- [ ] Integrate ESLint into project for better standardization.
- [ ] Create TS Docs and Python Docstrings for all functions
