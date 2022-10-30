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

It uses the `Django` language to render outputs. You can refer to `Flask-Django` for more information on how to use the `syntax`

For now there is two themes available:
- `vanilla` (default)
- `stock` 

Below will be instructions on how to build your own theme.

When setting your `url` make sure to use `za.linkedin.com/in/<yourprofile>` instead of `www.linkedin.com` or `linkedin.com`.

But for now, i have disabled selenium, therefore you will need to manually get the HTML of your LinkedIn profile and save it as `scrape.html` in the root directory. Below will be instructions on how to do that.

Run the script:

```bash
python3 app.py
```

At the moment for `testing` purposes, the script will generate a `cv.docx` file in the root directory. Using my LinkedIn profile as an example.
The script will generate a `cv.docx` file in the root directory.

### Produced CV output using `vanilla` theme

![image](https://user-images.githubusercontent.com/45560312/198889884-60d7bbbc-0064-4737-9f03-90fafaa89a2d.png)

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

### Building your own theme

Themes are built using `docx` templates. You can use any `docx` template you want, but it must have the following placeholders:

For example consider the following template:
- vanilla.docx

![image](https://user-images.githubusercontent.com/45560312/198889539-402b0d01-284f-4597-a937-11888abca825.png)

You can use that as a reference such that you can engineer your own theme without recoding the core python code.

There are additional parms you may get from the `app.py` i will leave it up to you to find out other parms that can be added.

If you look at `data.json` these are parms that `app.py` generates but not all of them are used in the `vanilla.docx` template.

Let us denote that the template is called `mytheme.docx` and it is located in the `themes` directory.

Then you will need to add the following to your `config.yaml` file:
```

themes:
  - theme: mytheme
    path: themes/mytheme.docx
    default: true

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

Feel free to create themes and share them with the community.

## Issues
There might be issues with some missing .dll files research the libraries and install the missing .dll files you should read the documentation of the libraries that are used in the project.

 


#### Made with ❤️ by ADGSTUDIOS 2022
