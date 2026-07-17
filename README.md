# Hi, I'm Khayllane Nyambir

Software developer from Mozambique building practical web applications, Python tools, and community-focused products.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="./light.svg" />
    <img alt="Khayllane Nyambir terminal profile" src="./dark.svg" width="100%" />
  </picture>
</p>

## About Me

I care about software that solves clear problems and remains useful under real-world constraints. My current work spans responsive web applications, offline-first experiences, and maintainable Python automation.

- Based in Mozambique and interested in locally relevant technology
- Focused on accessible interfaces, reliable workflows, and clean implementation
- Open to collaborating on useful web products and developer tools

## Featured Projects

### [AjudaCheia](https://github.com/nyambirkhayllane-svg/ajuda-cheia)

Mobile-first flood-response application designed for communities in Mozambique. It connects people requesting urgent help with volunteers and supports family reunification when connectivity is limited.

- SOS requests with location, urgency, contact details, and specific needs
- Volunteer filtering and end-to-end help confirmation
- Missing-person registration and family search
- Installable PWA with offline caching and local persistence

`React` · `Vite` · `PWA` · `Responsive Design` · `Offline-first`

### [Terminal Profile](https://github.com/nyambirkhayllane-svg/nyambirkhayllane-svg)

Python tooling that converts a photograph into ASCII art and generates compact, accessible SVG profile banners with automatic light and dark themes.

`Python` · `Pillow` · `SVG` · `GitHub Profile`

## Tech Stack

**Application development**

![React](https://img.shields.io/badge/React-0d1117?style=flat-square&logo=react&logoColor=61dafb)
![JavaScript](https://img.shields.io/badge/JavaScript-0d1117?style=flat-square&logo=javascript&logoColor=f7df1e)
![HTML5](https://img.shields.io/badge/HTML5-0d1117?style=flat-square&logo=html5&logoColor=e34f26)
![CSS3](https://img.shields.io/badge/CSS3-0d1117?style=flat-square&logo=css3&logoColor=1572b6)
![Vite](https://img.shields.io/badge/Vite-0d1117?style=flat-square&logo=vite&logoColor=646cff)

**Tools and workflow**

![Python](https://img.shields.io/badge/Python-0d1117?style=flat-square&logo=python&logoColor=58a6ff)
![Git](https://img.shields.io/badge/Git-0d1117?style=flat-square&logo=git&logoColor=f05032)
![GitHub](https://img.shields.io/badge/GitHub-0d1117?style=flat-square&logo=github&logoColor=ffffff)

## GitHub Activity

<p align="center">
  <img height="150" src="https://github-readme-stats.vercel.app/api?username=nyambirkhayllane-svg&show_icons=true&hide_border=true&theme=transparent" alt="Khayllane's GitHub statistics" />
  <img height="150" src="https://github-readme-stats.vercel.app/api/top-langs/?username=nyambirkhayllane-svg&layout=compact&hide_border=true&theme=transparent" alt="Khayllane's most used languages" />
</p>

## Contact

[GitHub](https://github.com/nyambirkhayllane-svg) · [Email](mailto:nyambirkhayllane@gmail.com) · Mozambique

<details>
<summary>How the terminal banner is generated</summary>

The banner is generated locally with Python and Pillow:

```bash
python photo_to_ascii.py
python generate_profile.py
```

The first command converts `photo.jpg` into `portrait.txt`. The second generates `dark.svg`, `light.svg`, and the backward-compatible `profile.svg`. Profile text can be overridden with `PROFILE_NAME`, `PROFILE_USERNAME`, `PROFILE_ROLE`, `PROFILE_LOCATION`, and `PROFILE_EMAIL` environment variables.

</details>
