This is a sample web application. It resembles a very simplified version of the atlassian jira ticketing system, where managers can create and assign tickets to workers, and workers can complete them.

I use this project as a playground for learning new technologies, and to demonstrate how I build things.

It is built with a django backend hosting a REST API. A frontend SPA built with Angular 4. And deployment is done with Kubernetes and Docker.

Features:
* Managers can create and assign/reassign tickets to any workers on the system.
* Workers can start and complete tickets. Managers can then verify completed tickets.
* Permission control is implemented. Managers can only modify their own tickets, and workers can only work on tickets assigned to them.
* Websockets is utilized so any changes to your view will be reflected without having to refresh the page.

A demo instance is running at http://sample.leowchan.com
* Login as a manager using manager1@example.com, manager2@example.com … (password is “password”). There are 5 managers on the demo system.
* Login as a worker using worker1@example.com, worker2@example.com … (password is “password”). There are 5 workers on the demo system.

Backend:
* REST API built using django and django rest framework
* Support regular requests and websocket requests (using django-channels)
* Authentication with JWT (using djangorestframework-jwt) and CORS (using django-cors-headers)
* Testcases for django querysets/views/serializers etc. using python mock and patch and factory_boy model factories
* Deployment to different environments can be customized with environment variables using django-environs

Frontend:
* Single page application built with Angular 4 in typescript
* Using JWT to authenticate HTTP requests, and using websockets
* Minimal styling with twitter bootstrap

Deployment:
* The backend and frontend project code will be baked into a docker image. Then the images will be deployed using a kubernetes helm chart.
* Using ConfigMaps to handle different configurations in different deployment environments
* Using nginx-ingress to route different requests to different services

Future Plans:
* Adding monitoring with prometheus.
* Centralized kubernetes logging.
* Kubernetes HTTPS ingress
* Kubernetes aliveness probes so that the containers can heal itself upon failures.
* Moving backing services (postgresql and redis) out of kubernetes and run them standalone.
* Improving how RXJS Observables/Subjects are being used in the angular code.
* Adding testcases for the angular code
