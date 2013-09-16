# -*- coding: utf-8 -*-

import json
import re
import os

import config
import renren

class Wall(renren.Renren):
    def __init__(self, wall_id):
        super(Wall, self).__init__()
        
        self.wall_id = wall_id
        self.url = config.WALLURL + wall_id
        self.title = self.people = self.status = ''
        self.all_status = []
        
        self.title_re = re.compile(r'<h2 class="a-sname" title="(?u)(\w+)">')
        self.people_re = re.compile(ur'<span class="a-statu">(\d+)人参加')
        self.status_re = re.compile(ur'(\d+)条状态</span>')
        self.sms_re = re.compile(r'sms_(\d+)')
        
    def get_wall(self):
        self.operate = self._get_response(self.url)
        mainpage = self.operate.read().decode('utf-8')
  
        self.title = self.title_re.search(mainpage).group(1)
        self.people = self.people_re.search(mainpage).group(1)
        self.status = self.status_re.search(mainpage).group(1)

        # Get pagecount
        raw_wall = self._get_response(self.url + '/wallDoing/1').read()
        json_wall = json.loads(raw_wall)
        pagecount = json_wall['pagecount']
        
        # Get status
        for page in range(1, pagecount + 1):
            print 'Reading Page %d of %d ...' % (page, pagecount)
            
            raw_wall = self._get_response(self.url + '/wallDoing/' + str(page)).read()
            json_wall = json.loads(raw_wall)

            try:
                for each in json_wall['wallDoingArray']:
                    status_info = {
                               'time': each['time'],
                               'userName': each['userName'],
                               'userId': each['userId'],
                               'content': each['content'],
                    }
                    self.all_status.append(status_info)
            except:
                None

        self._write_file('wall_' + self.wall_id + '.html', self.__format_output())

    def __format_output(self):
        output = [
                  '<!DOCTYPE HTML>', '<html lang=zh-cn>', '<head>', '<meta charset=utf-8>',
                  '<title>' + self.title + '</title>', '</head>', '<body>',
                  '<h1>' + self.title + '（<a href=' + self.url + '>原始地址</a>）</h1>',
                  '<h2>' + self.people + '人参加  |  ' + self.status + '条状态</h2>',
        ]

        for each_status in self.all_status:
            # 判断手机用户
            sms_number = self.sms_re.search(each_status['userId'])
            if not sms_number:
                formated_status = '<p><a href="http://www.renren.com/' + each_status['userId'] + '/profile">'
                formated_status += each_status['userName'] + '</a>    '
            else:
                formated_status = '<p>' + each_status['userName'] + '    '
            
            formated_status += each_status['time'] + '<br />'
            formated_status += each_status['content'] + '</p><hr />'
            output.append(formated_status)
        
        output += ['</body>', '</html>',]
        
        return [line + os.linesep for line in output]
    
if __name__ == '__main__':
    wall_getter = Wall('256593238')
    wall_getter.get_wall()
