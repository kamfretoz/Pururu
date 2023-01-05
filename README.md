<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/kamfretoz/XJ9">
    <img src="images/logo.svg" alt="Logo" width="128" height="128">
  </a>

<h1 align="center">XJ9</h1>

  <p align="center">
    A Multi-Purpose bot written with Hikari + Lightbulb!
  </p>
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
    <li><a href="#usage">Running The Bot</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
<p>
This is a Multi-Purpose Bot written in Python and built with Hikari and Lightbulb. 
A project that serves as a way for me to learn Python Programming.
Feel free to explore it by yourself!
</p>



### Built With

* [`hikari`](https://github.com/hikari-py/hikari) - An opinionated, static typed Discord microframework for Python3 and asyncio that supports Discord's V10 REST API and Gateway.
* [`Lightbulb`](https://github.com/tandemdude/hikari-lightbulb/) - A flexible command framework designed to extend Hikari.




<!-- GETTING STARTED -->
## Getting Started

To get the bot up and running, there are few steps that are need to be taken. Please follow these steps below carefully.

* You will need Python >= 3.8  so install it first!
* Install `screen` with `sudo apt install screen` or `sudo pacman -S screen` depending on your distro.

### Prerequisites

You will need to configure the bot with the `.env` file. This is needed to store some configuration data that are needed by the bot.

* As the bot uses few publicly available API (and Discord itself!), it needs a token to access them and you will have to provide them yourself, get the keys here:
  * [Discord](https://discord.com/developers/applications)
  * [OpenWeatherMap](https://openweathermap.org/api)
  * [Currency API](https://currency.getgeoapi.com/)
  * [Spotify](https://developer.spotify.com/dashboard/)

* You will also need a Lavalink nodes for music functionality. There are 2 options, either you self-host your own or you use the readily available Free Lavalink Nodes. Here are some recommendation:
  * [Lavalink Hosting](https://lavalink.darrennathanael.com/)

* Configure your `.env` as you please and put your token here.

  ```sh
  cd XJ9/
  cp .env.example .env
  nano .env
  ```

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/kamfretoz/XJ9.git
   cd XJ9/
   ```

2. Create a Virtual Enviroment and activate it
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Follow the steps from <a href="#prerequisites">Prerequisites</a>

4. Install the required dependencies
   ```sh
   python3 -m pip install -r requirements.txt
   ```

5. Run the bot 
   ```sh
   chmod +x run.sh
   ./run.sh
   ```


<!-- USAGE EXAMPLES -->
## Running the bot (continued)

There are few notes in regards to run the bot:
* If you'd like to run the bot (Or when you want to restart it), you will have to re-activate the Virtual Environment if you haven't done so:
  ```sh
    source .venv/bin/activate
    ./run.sh
  ```
* After you have successfully run the bot, you will have to Minimize the "screen" to let the bot run in the background.
    * Press `CTRL + A, D` to Minimize the screen
    * Type in `screen -r bot` to restore the screen

### Enjoy! :D

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/kamfretoz/XJ9.svg?style=for-the-badge
[contributors-url]: https://github.com/kamfretoz/XJ9/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/kamfretoz/XJ9.svg?style=for-the-badge
[forks-url]: https://github.com/kamfretoz/XJ9/network/members
[stars-shield]: https://img.shields.io/github/stars/kamfretoz/XJ9.svg?style=for-the-badge
[stars-url]: https://github.com/kamfretoz/XJ9/stargazers
[issues-shield]: https://img.shields.io/github/issues/kamfretoz/XJ9.svg?style=for-the-badge
[issues-url]: https://github.com/kamfretoz/XJ9/issues
[license-shield]: https://img.shields.io/github/license/kamfretoz/XJ9.svg?style=for-the-badge
[license-url]: https://github.com/kamfretoz/XJ9/blob/master/LICENSE
[product-screenshot]: images/screenshot.png
