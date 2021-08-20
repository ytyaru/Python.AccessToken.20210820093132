#!/usr/bin/env python3
# coding: utf8
import os, sys, csv, json, datetime, locale
from string import Template
from collections import namedtuple
def valid(*args):
    for arg in args:
        if arg is not None: return arg
def exept_null(f):
    def _wrapper(*args, **kwargs):
        try: return f(*args, **kwargs)
        except: return None
    return _wrapper
class Path:
    @classmethod
    def current(cls, path): # カレントディレクトリからの絶対パス
        return cls.__expand(os.path.join(os.getcwd(), path))
    @classmethod
    def here(cls, path): # このファイルからの絶対パス
        return cls.__expand(os.path.join(os.path.dirname(os.path.abspath(__file__)), path))
    @classmethod
    def name(cls, path): # このファイル名
        return os.path.basename(path)
    @classmethod
    def this_name(cls): # このファイル名
        return os.path.basename(__file__)
    @classmethod
    def __expand(cls, path): # homeを表すチルダや環境変数を展開する
        return os.path.expandvars(os.path.expanduser(path))
class FileReader:
    @classmethod
    @exept_null
    def text(self, path):
        with open(path, mode='r', encoding='utf-8') as f: return f.read().rstrip('\n')
    @classmethod
    def json(self, path):
        with open(path, mode='r', encoding='utf-8') as f: return json.load(f)
class This:
    def __init__(self):
        self.__Names = namedtuple('Names' , 'parent name ext')
        self.__make_this()
    def __make_this(self):
        name, ext = os.path.splitext(os.path.basename(__file__))
        parent = os.path.abspath(os.path.dirname(__file__))
        self.__this = self.__Names(parent, name, ext)
    @property
    def Names(self): return self.__this
This = This()
class CsvTokenReader:
    @property
    def Path(self): return os.path.join(This.Names.parent, 'token.tsv')
    def get(self, domain, username, scopes=None):
        if not os.path.isfile(self.Path): return None
        rows = self.__get_rows()
        if scopes is None:
            f = filter(lambda r: r[0] == domain and r[1] == username, rows)
        else:
            f = filter(lambda r: r[0] == domain and r[1] == username and all(s in r[2].split(',') for s in scopes), rows)
        l = list(f)
        if 0 < len(l): return l[0][3]
    def __get_rows(self):
        with open(self.Path) as f:
            rows = list(csv.reader(f, delimiter='\t'))
            headers = ['domain', 'username', 'scopes', 'token']
            if rows[0] == headers: rows = rows[1:]
            return rows
class Token:
    def __init__(self):
        self.__reader = CsvTokenReader()
    def get(self, domain, username, scopes=None):
        return self.__reader.get(domain, username, scopes=scopes)
class Command:
    def __init__(self):
        self.__meta = None
        self.__meta = FileReader.json(Path.here('meta.json'))
        self.__meta['readme'] = self.__meta['ja']['readme'] if 'ja_JP' == locale.getlocale()[0] else self.__meta['en']['readme']
    @property
    def Version(self): return self.__meta['version'] if self.__meta else '0.0.1'
    @property
    def Summary(self): return self.__meta['readme']['summary'] if self.__meta else 'アクセストークンを返す。'
    @property
    def Details(self): return self.__meta['readme']['details'] if self.__meta else '所定のファイルにトークンを保存しておく。コマンド引数で指定されたドメインとユーザ名で絞り込む。最初に見つかったトークンを返す。見つからなかったらなにも返さない。'
    @property
    def Description(self): return '\n'.join((self.Summary, 
                                            self.Details, 
                                            self.SystemArchitecture, 
                                            '特徴' if 'ja_JP' == locale.getlocale()[0] else 'Features', 
                                            self.Features, 
                                            '注意' if 'ja_JP' == locale.getlocale()[0] else 'Notes', 
                                            self.Notes))
    @property
    def Usage(self): return f'{This.Names.name}{This.Names.ext} DOMAIN USER [SCOPES]...'
    @property
    def Help(self):
        path = os.path.join(This.Names.parent, 'help.txt')
        with open(path, mode='r', encoding='utf-8') as f:
            t = Template(f.read().rstrip('\n'))
            return t.substitute(summary=self.Summary, 
                                usage=self.Usage, 
                                this=f'{This.Names.name}{This.Names.ext}', 
                                version=self.Version,
                                csv=CsvTokenReader().Path)
    @property
    def Meta(self):
        path = os.path.join(This.Names.parent, 'meta.txt')
        with open(path, mode='r', encoding='utf-8') as f:
            t = Template(f.read().rstrip('\n'))
            return t.substitute(description=self.Description, 
                                url=self.Url,
                                license_name=self.License['name'], 
                                license_url=self.License['url'], 
                                since=f'{self.Since:%Y-%m-%dT%H:%M:%S%z}', 
                                copyright=self.Copyright,
                                author_name=self.Author['name'],
                                author_sites='\n'.join(self.Author['sites']))

    @property
    def Since(self):
        return datetime.datetime.fromisoformat(self.__meta['since'] if self.__meta else '2021-08-12T00:00:00+09:00')
    @property
    def Author(self):
        return self.__meta['author'] if self.__meta else {'name': 'ytyaru',
            'sites': [
                'https://github.com/ytyaru',
                'https://twitter.com/ytyaru1',
                'https://mstdn.jp/@ytyaru',
                'https://profile.hatena.ne.jp/ytyaru/'
            ]}
    @property
    def Copyright(self): return f'© {self.Since.year} {self.Author["name"]}'
    @property
    def License(self):
        return self.__meta['license'] if self.__meta else {'name': 'CC0-1.0', 'url': 'https://creativecommons.org/publicdomain/zero/1.0/legalcode'}
    @property
    def Url(self): return self.__meta['url'] if self.__meta else 'https://github.com/ytyaru/Python.AccessToken.20210820093132'
    @property
    def SystemArchitecture(self): return valid(FileReader.text(Path.here('system_architecture.txt')), '''Terminal---------------------------------------+
|    TOKEN                                     |
|      |                                       |
| Python3.7--+                                 |
| | token.py | DOMAIN USERNAME [SCOPE] ...     |
| +----------+                                 |
|      |                                       |
| tokens.tsv---------------------------------+ |
| | domain    username  scopes      token    | |
| | mstdn.jp  ytyaru    read,write  xxxxx... | |
| | ...       ...       ...         ...      | |
| +------------------------------------------+ |
+----------------------------------------------+''')
    @property
    def Features(self):
        text = ''
        if self.__meta and self.__meta['readme']['features']:
            for feature in self.__meta['readme']['features']:
                text += f'* {feature[0]}\n  {feature[1]}\n'
        return text.rstrip('\n')
    @property
    def Notes(self):
        text = ''
        if self.__meta and self.__meta['readme']['notes']:
            for note in self.__meta['readme']['notes']:
                text += f'* {note[0]}\n  {note[1]}\n'
        return text.rstrip('\n')
class App(Command):
    def token(self, *args, **kwargs): return Token().get(*args, **kwargs)
class SubCmdParser:
    def __init__(self):
        self.__SubCmd = namedtuple('SubCmd' , 'candidate text')
        self.__candidates  = []
    def __cmd(self, text):
        print(text)
        sys.exit(0)
    def __sub_cmd(self, arg, candidate, text):
        if arg in candidate: self.__cmd(text)
    def add(self, candidate, text):
        self.__candidates.append(self.__SubCmd(candidate, text))
    def parse(self):
        for c in self.__candidates:
            self.__sub_cmd(sys.argv[1], c.candidate, c.text)
class Cli:
    def __cmd(self, text):
        if text is not None: print(text)
        sys.exit(0)
    def __get_args(self): return sys.argv[1:]
    def __parse(self):
        if 2 == len(sys.argv):
            parser = SubCmdParser()
            parser.add(['-h', '--help', 'h', 'help'], App().Help)
            parser.add(['-v', '--version', 'v', 'version'], App().Version)
            parser.add(['m', 'meta', 'metadata'], App().Meta)
            parser.add(['d', 'desc', 'description'], App().Description)
            parser.add(['u', 'url'], App().Url)
            parser.add(['a', 'author'], '\n'.join([App().Author['name'], *App().Author['sites']]))
            parser.add(['s', 'since'], App().Since.isoformat())
            parser.add(['c', 'copyright'], App().Copyright)
            parser.add(['l', 'license'], '\n'.join([App().License['name'], App().License['url']]))
            parser.parse()
            self.__cmd(App().Help)
        elif 2 < len(sys.argv):
            self.__cmd(App().token(sys.argv[1], sys.argv[2], scopes=sys.argv[3:] if 3 < len(sys.argv) else None))
        else: self.__cmd(App().Help)
    def run(self): self.__parse()

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
#    locale.setlocale(locale.LC_ALL, '')
    Cli().run()

