
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'matchtpl'))

from streaming import streaming as streaming

# streaming(args=args, stdin=sys.stdin, stdout=sys.stdout)
streaming()
