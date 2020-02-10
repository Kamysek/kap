# Documentation for `kap/frontend`

## Overview

In this file the general contents of the project folders will be explained.  
There are separate files for specific parts of the application.

1. the [app module](modules/app.md) in `/src/app` _also explains the `routing` and `graphQL` modules_
   1. the [services](services.md) in `/src/app/services`
1. the [shared module](modules/shared.md) in `/src/app/shared`
1. the [admin module](modules/admin.md) in `/scr/app/admin`
1. the [doctor module](modules/doctor.md) in `/src/app/doctor`
1. the [lab module](modules/lab.md) in `/src/app/lab`
1. the [patient module](modules/patient.md) in `/src/app/patient`

### Tech stack

This frontend project is a single page application based on the [angular](https://angular.io)
framework using [angular material](https://material.angular.io) for styling the UI. Also
the [apollo client](https://www.apollographql.com/docs/angular/) is used to handle communication
our GraphQL server.

### Important files

Since the project follow default angular conventions only a few important files
and folder will be explained here.

- `package.json` Holds all the projects dependencies needed to compile the application
- `schema.json` Is the GraphQL schema as emitted from the server
  - `schema.json.graphql` is the same schema, transformed into the default format
  - These files are generated as well and should not be manually edited
- `__generated__` Contains the typescript types generated based on the API requests.
  There is no need to ever manually change code in here as it is deleted and
  generated quite frequently.
- `docs` is the location of this documentation
- `e2e` Would contain possible end-to-end tests but doesn't at this point
- `src` Contains the actual application source code
  - Files in this folder are the usual in an angular project
  - `app` Is where the apps code is anf further discussed in modules/[app.md](modules/app.md)
