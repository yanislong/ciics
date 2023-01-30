#!/usr/bin/env python3

ll = []
with open('time.txt','r') as f:
    a = f.readlines()
    for i in a:
        try:
            j = float(i.strip())
            ll.append(j)
        except TypeError:
            pass
        except ValueError:
            pass
print(ll)
print(max(ll))
print(min(ll))
print(sum(ll)/len(ll))
