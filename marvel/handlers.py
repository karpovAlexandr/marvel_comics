import hashlib
import re
import string
import random

from marvel.models import Characters, Creators, Stories, Images


ID_PATTERN = r'(\d*)$'


def ts_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_hash_string(*args):
    _string = ''.join(args)
    return hashlib.md5(_string.encode()).hexdigest()


def create_character(character_data):

    characters = []
    for character in character_data:
        cleaned_character = dict()
        result = re.findall(ID_PATTERN, character['resourceURI'])
        character_id = int(result[0])

        if not Characters.objects.filter(id=character_id):
            cleaned_character['id'] = character_id
            cleaned_character['name'] = character['name']
            cleaned_character['resource_uri'] = character['resourceURI']
            characters.append(Characters.objects.create(**cleaned_character))
    return characters


def create_image(images_data):
    images = []
    for image in images_data:
        url = f"{image['path']}.{image['extension']}"
        images.append(Images.objects.create(image_url=url))
    return images


def create_creator(creator_data):

    creators = []
    for creator in creator_data:
        cleaned_creator = dict()
        result = re.findall(ID_PATTERN, creator['resourceURI'])
        creator_id = int(result[0])

        if not Creators.objects.filter(id=creator_id):
            cleaned_creator['id'] = creator_id
            cleaned_creator['name'] = creator['name']
            cleaned_creator['role'] = creator['role']
            cleaned_creator['resource_uri'] = creator['resourceURI']
            creators.append(Creators.objects.create(**cleaned_creator))
            # print(f"объект создатель {creator_id} создан")
    return creators


def create_story(story_data):

    stories = []
    for story in story_data:
        cleaned_story = dict()
        result = re.findall(ID_PATTERN, story['resourceURI'])
        story_id = int(result[0])

        if not Stories.objects.filter(id=story_id):
            cleaned_story['id'] = story_id
            cleaned_story['name'] = story['name']
            cleaned_story['type'] = story['type']
            cleaned_story['resource_uri'] = story['resourceURI']
            stories.append(Stories.objects.create(**cleaned_story))
            # print(f"объект истории {story_id} создан")
    return stories


def prepare_comics_data(comics_data):
    """подготваливаем dict для создания комикса"""
    cleaned_data = dict()

    stories = create_story(comics_data['stories']['items'])
    creators = create_creator(comics_data['creators']['items'])
    characters = create_character(comics_data['characters']['items'])
    images = create_image(comics_data['images'])

    cleaned_data['comics_id'] = comics_data['id']
    cleaned_data['digital_id'] = comics_data['digitalId']
    cleaned_data['title'] = comics_data['title']
    cleaned_data['issue_number'] = comics_data['issueNumber']
    cleaned_data['variant_description'] = comics_data['variantDescription']
    cleaned_data['description'] = comics_data['description']
    cleaned_data['modified'] = comics_data['modified']
    cleaned_data['isbn'] = comics_data['isbn']
    cleaned_data['upc'] = comics_data['upc']
    cleaned_data['diamond_code'] = comics_data['diamondCode']
    cleaned_data['ean'] = comics_data['ean']
    cleaned_data['issn'] = comics_data['issn']
    cleaned_data['format'] = comics_data['format']
    cleaned_data['page_count'] = comics_data['pageCount']
    cleaned_data['text_objects'] = comics_data['textObjects']
    cleaned_data['resource_uri'] = comics_data['resourceURI']
    cleaned_data['urls'] = comics_data['urls']
    cleaned_data['series_resource_uri'] = comics_data['series']['resourceURI']
    cleaned_data['series_name'] = comics_data['series']['name']
    cleaned_data['variants'] = comics_data['variants']
    cleaned_data['collections'] = comics_data['collections']
    cleaned_data['collected_issues'] = comics_data['collectedIssues']
    cleaned_data['dates'] = comics_data['dates']
    cleaned_data['prices'] = comics_data['prices']
    cleaned_data['thumbnail'] = f"{comics_data['thumbnail']['path']}.{comics_data['thumbnail']['extension']}"
    cleaned_data['events'] = comics_data['events']

    return cleaned_data, stories, characters, creators, images
