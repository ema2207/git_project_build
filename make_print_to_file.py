
def make_print_to_file(path='./'):
    import os 
    import sys
    import datetime

    class Logger(object):

        def __init__(self,filename="d.log",path="./"):
            self.terminal = sys.stdout
            self.path = os.path.join(path,filename)
            self.log = open(self.path,'a',encoding='utf-8',)
            self.dt = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S.%f')
            print("save:",os.path.join(self.path,filename))
        
        def write(self,message):
            message = self.dt + ' ' + message
            self.terminal.write(message)
            self.log.write(message)
        
        def flush(self):
            pass
    fileName = datetime.datetime.now().strftime('day_'+'%Y_%m_%d')
    sys.stdout = Logger(fileName + '.log', path = path)
    print(fileName.center(20, '*'))
            
if __name__ == '__main__':
    make_print_to_file(path='./')
    print("输出到日志文件")