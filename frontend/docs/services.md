# Services in `app/services`

Any file ending with `.spec.ts` would have tests for the service of the same name, which are not implemented as of now.  
Most services have private static attributes, which contain the needed GraphQL queries.

## The `AppointmentsService`

Responsible for loading information about appointments from the server and pushing updates as well.  
This service also runs a couple of transformations on the data it receives to make it easier to use in the application.

## The `AuthInterceptor`

Responsible for attaching the authentication token to any http request if the user is currently authenticated.

## The `AuthService`

Responsible for maintaining the authentication state of the application, running the login and providing the credentials to the interceptor.  
The `login()` function tries to authenticate the user with the server and if successful redirects them to the appropriate route based on their group.

## The `StudyPlanService`

Responsible for loading and changing data related to the study plan.

## The `UserService`

Responsible for loading and changing data related to patients and other users of the app as well as providing the data for the currently logged in user.
