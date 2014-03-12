import os, sys
import warnings
from urllib2 import urlopen as urlopen
import urlparse, urllib

EXOPEN_MINE_TYPE = {
    'file': open,
    'http': urlopen,
    'https': urlopen,
    'ftp': urlopen,
}
EXOPEN_MINE_TYPE_DEFAULT = open

def detect_opener(url):
    ret = urlparse.urlparse(url)
    print ret
    if ret.scheme:
        if EXOPEN_MINE_TYPE.has_key(ret.scheme):
            return EXOPEN_MINE_TYPE[ret.scheme]
    else:
        
        warnings.warn('Cannot detect scheme. Try open as a local file: %s')
        return EXOPEN_MINE_TYPE_DEFAULT
    return None

def exopen(url):
    pass
    

def path2url(path):
    return urlparse.urljoin(
      'file:', urllib.pathname2url(path))
    
def url2path(url):
    parseResult = urlparse.urlparse(url)
    return urllib.url2pathname(parseResult.path)

def test_uopen():
    with open('baidu.html', 'w') as f:
        d = urlopen('http://www.baidu.com').read()
        f.write(d)

    with open('image.jpg', 'wb') as f:
        d = urlopen('http://tp3.sinaimg.cn/1748763110/180/22843245628/1').read()
        f.write(d)

    with open('image2.jpg', 'wb') as f:
        d = urlopen('file:///C:/Projects/py-matchtpl/matchtpl/test/image.jpg').read()
        f.write(d)

    with open('image3.jpg', 'wb') as f:
        path = os.path.abspath('image.jpg')
        url = path2url(path)
        print '[path]', path
        print '[url]', url
        path2 = url2path(url)
        print path2
        print os.listdir(os.path.dirname(path2))

def test_detect():
    print detect_opener('file://www.baidu.com')
    print detect_opener('ftp://www.baidu.com')
    print detect_opener('http://www.baidu.com')
    print detect_opener('https://www.baidu.com')
    print detect_opener('www.baidu.com')
    print detect_opener(urllib.pathname2url('/user/w'))
    print detect_opener(urllib.pathname2url('c:\\user\\w'))

if __name__ == "__main__":
    import mimetypes
    from pprint import pprint
    #print mimetypes.knownfiles
    #print mimetypes.suffix_map
    #print mimetypes.encodings_map
    #pprint(mimetypes.types_map)
    test_detect()
    
