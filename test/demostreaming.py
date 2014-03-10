
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'matchtpl'))

from streaming import streaming as streaming
# call as follows:
# streaming(args=args, stdin=sys.stdin, stdout=sys.stdout)
# streaming()

if __name__ == "__main__":
    import timeit
    t = timeit.timeit(stmt='streaming()', setup='from __main__ import streaming', number=1)
    print >> sys.stderr, '[time]', t
