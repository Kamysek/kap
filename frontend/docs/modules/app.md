# The `src/app` folder

## The `AppModule`

Sets up the application and has all application level imports and configuration.  
This `AppComponent` is also part of this, it includes the highest level template.

### The folder `src/app/login` contains the `LoginComponent`

This is the template and logic for the `/login` route

## The `AppRoutingModule`

Registers any application level routes, in our case the `/login` route, that shows the login form

## The `GraphQLModule`

Imports and configures the apollo services
