# CV Generator From LinkedIn Profile

This is a simple script to generate a CV from your LinkedIn profile.

## Usage

Have at least `Python 3.8` installed.

Install the dependencies:

```bash
pip install -r requirements.txt
```

Configure `config.yaml` with your LinkedIn profile URL and personal information.

`config.yaml` should be setup like this 
```
# ADGSTUDIOS 2022 - config.yaml
themes:
  - theme: vanilla
    path: themes/vanilla.docx
    # This is the default theme, so it will be used if no theme is specified
    default: true

linkedin_profile:  
  # LinkedIn profile URL
  url: https://za.linkedin.com/in/adgsenpai

info:  
  phone: +27605224922
  email: adg@adgstudios.co.za
  location: Somerset West, Western Cape, South Africa
  discord: adgsenpai#2940
  instant: +27605224922
  website: https://adgstudios.co.za
  headline: Mathematican and Computer Scientist
```

Notice that you can set a theme in the `config.yaml` file. If you don't specify a theme, the default theme will be used.

For now there is two themes available:
- `vanilla` (default)
- `stock` 

Below will be instructions on how to build your own theme.

When setting your `url` make sure to use `za.linkedin.com/in/<yourprofile>` instead of `www.linkedin.com` or `linkedin.com`.

But for now, i have disabled selenium, therefore you will need to manually get the HTML of your LinkedIn profile and save it as `scrape.html` in the root directory. Below will be instructions on how to do that.

### Getting the HTML bypassed

For now selenium is disabled, so you will need to manually get the HTML of your LinkedIn profile and save it as `scrape.html` in the root directory. The LinkedIn `AuthWall` is a pain to get around, so i have disabled it for now.

Go to https://search.google.com/test/mobile-friendly set your linkedin profile url

for example i will use mine `https://za.linkedin.com/in/adgsenpai`

![image](https://user-images.githubusercontent.com/45560312/198889388-22a7e30b-3d53-42e8-8538-8977b681bbfa.png)

Then click `TEST URL`

Complete the `CAPTCHA` if required...

Then wait a few minutes ... to process

![image](https://user-images.githubusercontent.com/45560312/198889429-5f4e1bc0-dabe-4545-bc17-cd28e12415e5.png)


Once done click `View Tested Page`

![image](https://user-images.githubusercontent.com/45560312/198889443-06c758ca-36b9-47b9-9ee2-aee159d04d4d.png)

`Copy the HTML payload` and save it in `scrape.html` in the directory of the software.






 


