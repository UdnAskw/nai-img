import os
import re
import sys
import pprint
import argparse
import configparser
import datetime
import time

from asyncio import run

from boilerplate import API

from novelai_api.ImagePreset import ImageModel, ImagePreset, ImageResolution, UCPreset

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(SCRIPT_DIR, '../config')
SAVE_DIR = os.path.join(SCRIPT_DIR, '../artifact')

MODEL_MAPPING = {
    'anime_curated': ImageModel.Anime_Curated,
    'anime_full': ImageModel.Anime_Full,
    'furry': ImageModel.Furry
}

#RESOLUTION_MAPPING = {
#    'normal_portrait': ImageResolution.Normal_Portrait,   # 512x768
#    'normal_langscape': ImageResolution.Normal_Landscape, # 768x512
#    'normal_square': ImageResolution.Normal_Square,       # 640x640
#    'large_portrait': ImageResolution.Large_Portrait,     # 512x1024
#    'large_langscape': ImageResolution.Large_Landscape,   # 1024x512
#    'large_square': ImageResolution.Large_Square          # 1024x1024)
#}

TYPE_MAPPING = {
    "quality_toggle": bool,
    "resolution": str,
    "n_samples": int,
    "seed": int,
    "scale": float,
    "steps": int,
    "uc": str,
}


def get_args():
    parser = argparse.ArgumentParser(description='Description')
    parser.add_argument('-p', '--prompt', type=str, default='', help='Prompt')
    parser.add_argument('-f', '--prompt-file', type=str, default='prompt_default.txt', help='Prompt file name')
    parser.add_argument('-m', '--model', type=str, choices=MODEL_MAPPING.keys(), default='anime_full', help='ImageModel')
    parser.add_argument('-F', '--preset-file', type=str, default='preset_default.ini', help='Preset file name')
    parser.add_argument('-e', '--seed', type=int, help='Seed')
    parser.add_argument('-n', '--n-samples', type=int, help='Numer of images')
    parser.add_argument('-q', '--quality-toggle', type=bool, help='Add quality tags')
    #parser.add_argument('-r', '--resolution', type=str, choices=RESOLUTION_MAPPING.keys(), help='Image resolution')
    parser.add_argument('-R', '--resolution', type=str, help='Resolution (ex. 512,768)')
    #parser.add_argument('-U', '--uc-preset', help='Negative prompt preset')
    parser.add_argument('-u', '--uc', type=str, help='Negative prompt')
    parser.add_argument('-S', '--scale', type=float, help='Scale')
    parser.add_argument('-s', '--steps', type=int, help='Steps')
    parser.add_argument('-i', '--interval', type=float, default=5, help='Generate images interval (sec)')
    parser.add_argument('-r', '--repeat', type=float, default=1, help='Repeat count')
    parser.add_argument('-d', '--save-dir', type=str, default=SAVE_DIR, help='Save directory')
    #parser.add_argument('--strength')
    #parser.add_argument('--noise')
    #parser.add_argument('--sampling')
    return parser.parse_args()


def get_settings(args):
    interval = args.interval
    repeat = args.repeat
    save_dir = args.save_dir
    prompt = get_prompt_from_file(args.prompt_file) + args.prompt
    model = MODEL_MAPPING[args.model]
    preset = get_preset_from_file(args.preset_file)
    preset['uc'] = preset['uc'] + args.uc if args.uc is not None else preset['uc']
    del (
        args.repeat,
        args.interval,
        args.prompt_file,
        args.model,
        args.preset_file,
        args.uc,
        args.save_dir,
    )

    d_args = args.__dict__
    for key in d_args.keys():
        if d_args[key]:
            preset[key] = d_args[key]
    
    tuple_res = tuple(preset['resolution'].split(','))    
    if len(tuple_res) != 2:
        raise SyntaxError('resolution option expected "XXX,YYY"')
    else:
        preset['resolution'] = tuple_res

    return {
        'prompt': prompt,
        'model': model,
        'preset': preset,
        'interval': interval,
        'repeat': repeat,
        'save_dir': save_dir,
    }


def get_prompt_from_file(filename):
    prompt = ''
    with open(os.path.join(CONFIG_DIR, filename), 'r') as f:
        for line in f:
            prompt = f"{prompt}{line.rstrip()},"
    return prompt


def get_preset_from_file(filename):
    config = configparser.ConfigParser()
    config.read(os.path.join(CONFIG_DIR, filename))
    raw_preset = dict(config['default'])
    return raw_preset_type_conv(raw_preset)


def raw_preset_type_conv(raw_preset):
    preset = {}
    for key in raw_preset.keys():
        value = raw_preset[key]
        try:
            preset[key] = TYPE_MAPPING[key](value)
        except KeyError:
            pass
    return preset


async def main():
    settings = get_settings(get_args())
    os.makedirs(settings['save_dir'], exist_ok=True)

    async with API() as api_handler:
        api = api_handler.api

        preset = ImagePreset(**settings['preset'])
        pprint.pprint(settings)

        count = 0
        while count < settings['repeat']:
            async for img in api.high_level.generate_image(settings['prompt'], settings['model'], preset):
                now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
                with open(os.path.join(SAVE_DIR, f"{now}.png"), "wb") as f:
                    f.write(img)
                count += 1
                if count < settings['repeat']:
                    time.sleep(settings['interval'])


run(main())