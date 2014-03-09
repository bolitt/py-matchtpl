
def mapper(key, value, output=None, reporter=None):
    pass
        
class Counter:
    NUM = 0
    def __init__(self):
        pass
    def __call__(self, s):
        #Counter.NUM += 1
        return "%s&counter=%d" % (s, 1)

# http://hadoop.apache.org/docs/r2.3.0/api/index.html
# https://hadoop.apache.org/docs/r1.2.1/mapred_tutorial.html

# reduce(function, iterable[, initializer])
arr = [1,2,3,4,1]
def add(v):
    return v + 0.1
print map(add, arr)


def collect(x, y):
    print 'x:',x
    x.append(y)
    return x

print reduce(collect, arr, [])

import sys

class Stream:
    def __init__(self, instream=sys.stdin,
                 outstream=sys.stdout,
                 errorstream=sys.stderr):
        self.instream = instream
        self.outstream = outstream
        self.errorstream = errorstream
        
    def read(self):
        return self.instream.read()
    
    def write(self, v):
        self.outstream.write(v)

    def writeln(self, v):
        print >> self.outstream, v

    def error(self, v):
        self.errorstream.write(v)
        
    def errorln(self, v):
        print >> self.errorstream, v

class JobConf(dict):
    def __init__(self):
        pass

job = JobConf()
job['jobid'] = 'jobid_5'
print job.get('jobid')

st = Stream()
st.write('hello')
st.writeln('+world d')
st.error('error1')
st.errorln('+error2')

class Self:
    def self(self):
        return self

class Mapper(Self, Job):
    def __init__(self):
        print '[inside]'
        super(Mapper, self).__init__()

    def __call__(self, key, value, output=None, reporter=None):
        pass

class Reducer(Self):
    def __init__(self):
        pass
    def __call__(self, key, values, output=None, reporter=None):
        pass
Mapper().write('d')
print Reducer().self().self()


