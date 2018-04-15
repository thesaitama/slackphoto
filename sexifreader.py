#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sexifreader.py

# PIL Image Info
from PIL import Image
from PIL.ExifTags import TAGS

def getExifInfo(filePath, debugMode=False):
    """ obtatin exif information
    """
    i = Image.open(filePath)
    exif = i._getexif()

    # check exist Exif data
    if (exif is None):
        return 'no Exif data.'

    output_str = ''  # output string

    raw_date = ''
    date_str = ''
    time_str = ''
    maker = ''
    model = ''
    software = ''

    for tag, value in exif.items():
        #  TIFF Tag MakerNote is 37500
        if (tag != 37500):
            tag_name = TAGS.get(tag)

            # for Debug mode
            if(debugMode):
                print str(tag_name) + ': ' + str(value)

            if (tag_name == 'DateTimeOriginal'):
                raw_date = ''.join(map(str, value)).split(' ')
                date_str = raw_date[0].replace(':', '/')
                time_str = raw_date[1]
            elif (tag_name == 'Make'):
                maker = str(value).strip()
            elif (tag_name == 'Model'):
                model = str(value).strip().strip('\x00')
            elif (tag_name == 'Software'):
                software = str(value).strip().strip('\x00')

    # reformat model name
    model = model.replace(maker, '').strip()

    output_str = 'Date: %s %s\nCamera: %s %s' % (date_str, time_str, maker, model)

    # reformat software name
    if(software != ''):
        software = software.replace(model, '').strip()
        output_str += ' (%s)' % software

    return output_str


if __name__ == '__main__':
    print getExifInfo('test/test.jpg', True)
