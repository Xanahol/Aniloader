# Aniloader
Update your Anime-Library with one command!

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#About-Aniloader">About Aniloader</a>
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
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About Aniloader

As a frequent Anime-watcher and Series-Collector, who wants to stay up to Date with the newest releases in an hourly fashion,
I had to find a solution to the constant *"Downloading all Episodes released that day in the evening".* So I automated it. 
I really hope that this Programm can lighten your day, even if just by a bit.

Here's why:
* Your time to browse the **NEW** Anime of the day and downloading every single Episodes manually can be used for much more important activities. Like watching more Anime!
* You shouldn't have to organizing your entire library manually just so Daddy-Plex is happy. It's a hassel. Let Aniloader take care of it for you.
* You should just be able to enjoy the latest Anime right when it comes out. Let Aniloader do the delivery :mailbox_with_mail:

Of course, this is only one of the possible functions. So you can expect me to be adding more features in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue.

### Built With

* [Selenium](https://www.selenium.dev/)
* [qBittorrent](https://www.qbittorrent.org/)
* [SubsPlease](https://subsplease.org/)
* [Plex](https://www.plex.tv/)



<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

* Plex</br>
Though not a necesity, I very much recommend the media-Player due to its versitillity.
[Official Site](https://www.plex.tv/)

* qBittorrent</br>
This Application uses the **qBittorrent Web UI** to manage the Magnet-Links found on SubsPlease. After installing it from the [official site](https://www.qbittorrent.org/), 
make sure that the *options->Web UI* match this Picture:</br>
PIC</br>
**IP address:** Type your IPv4-address. You can find it by typing *ipconfig* in your console
**Port:** Make sure this number matches with the *torrent_port* you defined in Aniloaders `config.py`
**Authentication:** Define a username and password

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Xanahol/Aniloader.git
   ```
3. Install requirements
   ```sh
   pip install -r .\requirements.txt
   ```
4. Enter your settings in `config.py`
   ```python
   #Example
   ip_4 = "192.168.4.162" 
   torrent_port = "8080"
   directories = ['C:\Example\Plex\Anime', 'D:\Example\Path\To\Plex\Anime']
   ```



<!-- USAGE EXAMPLES -->
## Usage




<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/Xanahol/Aniloader/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- CONTACT -->
## Contact

Noël B. - [@_noel_br](https://www.instagram.com/_noel_br/?hl=en)

Project Link: [https://github.com/Xanahol/Aniloader](https://github.com/Xanahol/Aniloader)

