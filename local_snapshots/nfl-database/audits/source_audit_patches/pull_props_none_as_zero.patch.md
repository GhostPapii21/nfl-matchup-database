# Proposed patch: week8/lines/pull_props.py diff() None-as-0 (diagnostic print only; not applied)
`dl=float(n['line'] or 0)-float(o['line'] or 0)` turns a missing line into 0, printing a fake move of +/-line.
```diff
-        try: dl=float(n['line'] or 0)-float(o['line'] or 0)
-        except: dl=0
+        if not n['line'] or not o['line']: print('NOLINE ',k[0],n['player'],n['market'],o['line'],'->',n['line']); continue
+        dl=float(n['line'])-float(o['line'])
```
