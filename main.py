from os.path import expanduser
import markdown, sys, hashlib
import random
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
import oss2, json


def ParseConfig(path):
    file = open(path)
    return json.loads(file.read())


class AliyunOss():
    def __init__(self, conf):
        self.auth = oss2.Auth(conf['AccessKeyId'], conf['AccessKeySecret'])
        self.bucket = oss2.Bucket(self.auth, conf['EndPoint'], conf['Bucket'])

    def uploadImage(self, key, localPath):
        result = self.bucket.put_object_from_file(key, localPath)
        return result


class ImagePreprocessor(Treeprocessor):
    def run(self, root):
        self.md.images = []

        for image in root.findall('.//img'):
            self.md.images.append(image.get('src'))


class ImageExtractExtension(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.treeprocessors.register(ImagePreprocessor(md), 'tree', 15)


if __name__ == '__main__':
    random.seed()
    conf = ParseConfig(expanduser('~/.ossconfig'))
    oss_manager = AliyunOss(conf)
    md5 = hashlib.md5()
    md = markdown.Markdown(extensions=[ImageExtractExtension()])
    data = open(sys.argv[1], mode='r', encoding='utf-8').read()
    md.convert(data)
    images = md.images
    for index in range(len(images)):
        img = images[index]
        print('Processing img ', index, img, '...')
        if img.startswith('http'):
            print('No need to process! Continue...')
        else:
            md5.update(open(img, mode='rb').read())
            key = md5.hexdigest()
            result = oss_manager.uploadImage(key, img)
            if result.status == 200:
                url = conf['UrlPrefix'] + '/' + str(key)
                print('Upload successfully! url:', url)
                data = data.replace(img, url)
            else:
                print('Upload error, result: ', result.__str__())
    open(sys.argv[1]+'.convert', mode='w', encoding='utf-8').write(data)