<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1 align="center">Riding API</h1>

  <p align="center">
    API to manage travels, drivers and vehicles.
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

RidingAPI is a REST API for a travel system. You can create a user to create travel requests. You can also with your user become a driver and accept travels. The location of the travels is placed using longitude and latitude. You can list the avaliable travels according to where you are and a radius.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

Technologies used in this project are:

* [![Python][python-shield]][python-url]
* [![PostgreSQL][postgresql-shield]][postgresql-url]
* [![Django][django-shield]][django-url]
* [![Celery][celery-shield]][celery-url]
* [![Redis][redis-shield]][redis-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Before you start, you'll need to make sure you have the following installed:
* Docker
* Docker Compose
* Git

### Installation

1. Clone the repository and access it.
    ```sh
    git clone https://github.com/SSleimann/riding-api.git
    cd riding-api 
    ```
2. Run the following command to build and run the containers in local:
   ```sh
   docker compose -f local.yml up -d
   ```

You can stop the containers by running:
```sh
docker compose -f local.yml down
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

First, you need to create a user to be able to access the other endpoints. A user is a passenger, a user can become a driver as well.

If you become a driver, in order to take travels you need to have vehicles, otherwise your status will be inactive and you will not able to take travels.

When you take a request travel, a Travel object is created, then when you want to end the travel, the driver and the passenger must confirm the confirmation order, when both have done so the travel is ended.

On the other hand, being a user you can create request travels adding your current location in latitude and longitude, when a travel is taken, you will be notified with an email. In local mode, the email backend is `django.core.mail.backends.locmem.EmailBackend`.

You can see the endpoints of the application in the path `/api/docs/schema/swagger-ui/`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

This project is licensed under the GNU General Public License (GPL) version 3. See the [LICENSE](LICENSE) file for more details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Sleiman Orocua - sleimanjose23@hotmail.com

Project Link: [https://github.com/SSleimann/riding-api](https://github.com/SSleimann/riding-api)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- URLS -->

[python-url]: https://www.python.org/
[django-url]: https://www.djangoproject.com/
[celery-url]: https://docs.celeryq.dev/en/stable/
[redis-url]: https://redis.io/
[postgresql-url]: https://www.postgresql.org/

<!-- BADGES -->
[python-shield]: https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue
[celery-shield]:https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4
[redis-shield]: https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white
[postgresql-shield]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[django-shield]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green