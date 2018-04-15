# slackphoto
A randam photo uploader for Slack. This Script post your photos to Slack randomly.
You will discover unexpected discoveries when used between families.

## Requirements
tested with Linux (Raspberry pi) and macOSX 10.13

* Slack Account
* Slack Token
  + Token has chat:write:bot, files:read, files:write:user
* python 2.7.x

## How to Install
* Clone this repository.

```bash
> git clone https://github.com/thesaitama/slackphoto.git
```

* Install PIP.
* Install dependencies.

```bash
> cd slackphoto
> pip install -r requirements.txt
```

* Configure JSON Settings file.
  + Rename sample JSON File.

  ```bash
  > mv slackphoto.sample.json slackphoto.json
  ```

  + Edit slackphoto.json

  ```json
  {
    "slackToken" : "<YOUR_SLACK_TOKEN>",
    "slackChannelID" : "<YOUR_SLACK_CHANNEL_ID>",
    "slackRemoveLimitDay" : 15,
    "repeatCount" : 1,
    "dirs" : [
        "<YOUR_PHOTO_DIR_PATH>"
    ]
  }
  ```

+ slackRemoveLimitDay: uploaded files delete after specified days.
+ repeatCount: repeat times. (optional)
+ dirs: multiple folders can be set.
+ dirsIgnore: ignore path list, also multiple floders can be set. (optional)

* Set crontab

```
# m h  dom mon dow   command
0 12 * * * python /<APP_DIR>/slackphoto.py > /dev/null
```

## Links
* Create New App (obtein token)
 https://api.slack.com/apps

## License
MIT

## Maintainer
* Kazuhiro Komiya

